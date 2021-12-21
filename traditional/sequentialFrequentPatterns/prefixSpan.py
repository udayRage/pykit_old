import sys
import time
import math
import resource
from collections import defaultdict as dd


def minSupAbs(file, sup):
    """
    converting the percentage value into absolute value
    :param file: the input data file
    :param sup: the percentage support value
    :return: returns an absolute integer value
    """
    global minimumSupport
    with open(file, 'r') as f:
        read = f.readlines()

    minimumSupport = int(math.ceil(sup * len(read)) / 100)
    return minimumSupport


def save(item, supp):
    """
    save the frequent sequential patterns into the 'output.txt' file
    :param item: frequent sequential pattern
    :param supp:support of the sequential frequent pattern
    """
    global patternCount
    patternCount += 1
    with open("output.txt", 'a+') as f:
        a = ""
        a += str(item)
        a += " -1 #SUP: "
        a += str(supp)
        f.write(a)
        f.write("\n")
    f.close()


def save1(lastBufPos, psudoSeq):
    """
    saves the sequential frequent pattern into the 'output.txt' file
    :param lastBufPos: index position in the pattern buffer
    :param psudoSeq:sequences in which the pattern present
    :return:
    """
    global patternCount
    patternCount += 1
    with open("output.txt", 'a+') as f:
        i = 0
        a = ""
        while i <= lastBufPos:
            a += str(patternBuffer[i])
            a += " "
            i += 1
        if patternBuffer[lastBufPos] != -1:
            a += str(-1)
        a += "#SUP: "
        a += str(len(psudoSeq))
        f.write(a)
        f.write("\n")
    f.close()


def scanDataBase(file):
    """
    scan the database and returns the all the data in the form of the list
    :param file: input file
    :return: returns the data in the form of the list
    """
    with open(file, 'r') as f:
        read = f.readlines()
        lis = []
        for i in read:
            li = list(map(int, i.split()))
            lis.append(li)
    return lis


def PseudoSequence(seqId, indFirItem):
    """
    takes the item and its index and returns it in the form of the list
    :param seqId: item
    :param indFirItem: index of the item
    :return: return the list of them
    """
    return [seqId, indFirItem]


def findSequenceContainItems(data):
    """
    takes the data as input and returns the single items and their count in the form of the dictionary
    :param data:input data
    :return: returns the dictionary containing single items
    """
    global containsItemSetsWithMultipleItems
    sequenceID = dd(list)
    for i in range(len(data)):
        sequence = data[i]
        itemCount = 0
        for j in sequence:
            if j >= 0:
                sequenceIDs = sequenceID[j]
                if len(sequenceIDs) == 0 or sequenceIDs[len(sequenceIDs) - 1] != i:
                    sequenceIDs.append(i)
                itemCount += 1
                if itemCount > 1:
                    containsItemSetsWithMultipleItems = True
            elif j == -1:
                itemCount = 0
    return sequenceID


def prefixSpanWithSingleItems(seqId, data, file):
    """
    mining of the patterns containing single items starts from here
    :param seqId: dictionary containing single items and their sequences
    :param data: input data in the form of the list
    :param file: input file
    """
    global patternCount
    for i in range(len(data)):
        seq = data[i]
        curPos = 0
        lis = []
        for j in seq:
            if j >= 0:
                isFreq = len(seqId[j]) >= minimumSupport
                if isFreq:
                    lis.append(j)
                    curPos += 1
            elif j == -2:
                if curPos > 0:
                    lis.append(-2)
                    data[i] = lis
                    continue
                else:
                    data[i] = []
    for i in list(sorted(seqId)):
        if len(seqId[i]) >= minimumSupport:
            save(i, len(seqId[i]))
            patternBuffer[0] = i
            projDataB = buildProjectedDatabaseSingleItems(i, seqId[i], data)
            recursionSingleItems(data, patternBuffer, projDataB, 2, 0)


def prefixSpanWithMultipleItems(seqId, data, file):
    """
    mining of the patterns containing multiple items starts from here
    :param seqId: dictionary containing single items and their sequences
    :param data: input data in the form of the list
    :param file: input file
    """
    global patternCount
    for i in range(len(data)):
        seq = data[i]
        curPos = 0
        curItemCount = 0
        lis = []
        for j in seq:
            if j >= 0:
                isFreq = len(seqId[j]) >= minimumSupport
                if isFreq:
                    lis.append(j)
                    curPos += 1
                    curItemCount += 1
            elif j == -1:
                if curItemCount > 0:
                    lis.append(-1)
                    curPos += 1
                    curItemCount = 0
            elif j == -2:
                if curPos > 0:
                    lis.append(-2)
                    data[i] = lis
                    continue
                else:
                    data[i] = []
    for i in list(sorted(seqId)):
        if len(seqId[i]) >= minimumSupport:
            save(i, len(seqId[i]))
            patternBuffer[0] = i
            projDataB = buildProjectedDatabaseFirstTimeMultipleItems(i, seqId[i], data)
            recursion(data, patternBuffer, projDataB, 2, 0)


def buildProjectedDatabaseSingleItems(item, seqId, data):
    """
    finds out the projected database of each item
    :param item: item
    :param seqId: item containing sequences
    :param data: input data in the form of the list
    :return:
    """
    proDataBase = []
    for i in seqId:
        k = data[i]
        for j in range(len(k)):
            token = k[j]
            if token != -2:
                if token == item:
                    if k[j+1] != -2:
                        proData = PseudoSequence(i, j + 1)
                        proDataBase.append(proData)
                        continue
    return proDataBase


def buildProjectedDatabaseFirstTimeMultipleItems(item, seqId, data):
    """
        finds out the projected database of each item
        :param item: item
        :param seqId: item containing sequences
        :param data: input data in the form of the list
        :return:
        """
    proDataBase = []
    for i in seqId:
        k = data[i]
        for j in range(len(k)):
            token = k[j]
            if token != -2:
                if token == item:
                    isEndOfSeq = (k[j + 1] == -1 and k[j + 2] == -2)
                    if not isEndOfSeq:
                        proData = PseudoSequence(i, j + 1)
                        proDataBase.append(proData)
                        continue
    return proDataBase


def findAllFrequentPairsSingleItems(dataBase, lastBufPos, data):
    """
    find out the pattern pairs
    :param dataBase: projected database
    :param lastBufPos: last buffer of the pattern buffer
    :param data: input data
    :return: return the list containing items and their sequences
    """
    mapItemPseudoSeq = dd(list)
    for i in range(len(dataBase)):
        seqId = dataBase[i][0]
        seq = data[seqId]
        for j in range(dataBase[i][1], len(seq)):
            token = seq[j]
            if token >= 0:
                listSeq = mapItemPseudoSeq[token]
                ok = True
                if len(listSeq) > 0:
                    ok = listSeq[len(listSeq)-1][0] != seqId
                if ok:
                    listSeq.append(PseudoSequence(seqId, j + 1))
    return mapItemPseudoSeq


def findAllFrequentPairs(dataBase, lastBufPos, data):
    """
        find out the pattern pairs
        :param dataBase: projected database
        :param lastBufPos: last buffer of the pattern buffer
        :param data: input data
        :return: return the list containing items and their sequences
    """
    pseudoSeqMP = {}
    pseudoSeqMPIP = {}
    mapsPairs = dd(list)
    mapPairsInPostfix = dd(list)
    firstPosOfLasItemBuf = lastBufPos
    while lastBufPos > 0:
        firstPosOfLasItemBuf -= 1
        if firstPosOfLasItemBuf < 0 or patternBuffer[firstPosOfLasItemBuf] == -1:
            firstPosOfLasItemBuf += 1
            break    # print(data)

    posToMatch = firstPosOfLasItemBuf
    for i in range(len(dataBase)):
        seqId = dataBase[i][0]
        seq = data[seqId]
        prevItem = seq[dataBase[i][1] - 1]
        curItemSetIsPostfix = (prevItem != -1)
        isFirstItemSet = True
        for j in range(dataBase[i][1], len(seq)):
            token = seq[j]
            if token >= 0:
                pair = token
                if curItemSetIsPostfix:
                    if pair not in list(pseudoSeqMPIP):
                        pseudoSeqMPIP[pair] = []
                else:
                    if pair not in list(pseudoSeqMP):
                        pseudoSeqMP[pair] = []
                if curItemSetIsPostfix:
                    oldPair = mapPairsInPostfix[pair]
                else:
                    oldPair = mapsPairs[pair]
                if not oldPair:
                    if curItemSetIsPostfix:
                        mapPairsInPostfix[pair] = pair
                    else:
                        mapsPairs[pair] = pair
                else:
                    pair = oldPair
                ok = True
                if curItemSetIsPostfix:
                    if len(pseudoSeqMPIP[pair]) > 0:
                        ok = pseudoSeqMPIP[pair][len(pseudoSeqMPIP[pair]) - 1][0] != seqId
                    if ok:
                        pseudoSeqMPIP[pair].append(PseudoSequence(seqId, j + 1))
                else:
                    if len(pseudoSeqMP[pair]) > 0:
                        ok = pseudoSeqMP[pair][len(pseudoSeqMP[pair]) - 1][0] != seqId
                    if ok:
                        pseudoSeqMP[pair].append(PseudoSequence(seqId, j + 1))
                if curItemSetIsPostfix and not isFirstItemSet:
                    pair = token
                    oldPair = mapsPairs[pair]
                    if not oldPair:
                        mapsPairs[pair] = pair
                    else:
                        pair = oldPair
                    ok = True
                    if pair not in list(pseudoSeqMP):
                        pseudoSeqMP[pair] = []
                    if len(pseudoSeqMP[pair]) > 0:
                        ok = pseudoSeqMP[pair][len(pseudoSeqMP[pair]) - 1][0] != seqId
                    if ok:
                        pseudoSeqMP[pair].append(PseudoSequence(seqId, j + 1))
                if curItemSetIsPostfix is False and patternBuffer[posToMatch] is token:
                    posToMatch += 1
                    if posToMatch > lastBufPos:
                        curItemSetIsPostfix = True
            elif token is -1:
                isFirstItemSet = False
                curItemSetIsPostfix = False
                posToMatch = firstPosOfLasItemBuf
    return [mapsPairs, mapPairsInPostfix, pseudoSeqMP, pseudoSeqMPIP]


def recursionSingleItems(da, patternBuff, dataBase, k, lastBuffPo):
    """
    recursion of the item and finding out the patterns with that sequence
    :param da: input data
    :param patternBuff: pattern buffer which we have taken
    :param dataBase: projected database
    :param k: length of the pattern
    :param lastBuffPo: last buffer position in the pattern buffer
    :return: returns the list containing items and their sequences
    """
    itemPseudoSeq = findAllFrequentPairsSingleItems(dataBase, lastBuffPo, da)
    if itemPseudoSeq:
        for i in list(sorted(itemPseudoSeq)):
            if len(itemPseudoSeq[i]) >= minimumSupport:
                patternBuff[lastBuffPo+1] = -1
                patternBuff[lastBuffPo+2] = i
                save1(lastBuffPo+2, itemPseudoSeq[i])
                recursionSingleItems(da, patternBuff, itemPseudoSeq[i], k+1, lastBuffPo+2)


def recursion(da, patternBuff, dataBase, k, lastBuffPo):
    """
        recursion of the item and finding out the patterns with that sequence
        :param da: input data
        :param patternBuff: pattern buffer which we have taken
        :param dataBase: projected database
        :param k: length of the pattern
        :param lastBuffPo: last buffer position in the pattern buffer
        :return: returns the list containing items and their sequences
    """
    global patternCount
    mapsPairs = findAllFrequentPairs(dataBase, lastBuffPo, da)
    if mapsPairs:
        for i in list(sorted(mapsPairs[1])):
            if len(mapsPairs[3][i]) >= minimumSupport:
                newBufferPos = lastBuffPo
                newBufferPos += 1
                patternBuff[newBufferPos] = i
                save1(newBufferPos, mapsPairs[3][i])
                recursion(da, patternBuff, mapsPairs[3][i], k + 1, newBufferPos)
        for i in list(sorted(mapsPairs[0])):
            if len(mapsPairs[2][i]) >= minimumSupport:
                newBufferPos = lastBuffPo
                newBufferPos += 1
                patternBuff[newBufferPos] = -1
                newBufferPos += 1
                patternBuff[newBufferPos] = i
                save1(newBufferPos, mapsPairs[2][i])
                recursion(da, patternBuff, mapsPairs[2][i], k + 1, newBufferPos)


if __name__ == '__main__':
    path = sys.argv[1]
    minSup = float(sys.argv[2])
    patternBuffer = [None] * 25
    minimumSupport = minSupAbs(path, minSup)
    patternCount = 0
    containsItemSetsWithMultipleItems = False
    file = open('output.txt', 'w')
    file.truncate()
    file.close()
    start = int(round(time.time()*1000))
    dat = scanDataBase(path)
    seq = findSequenceContainItems(dat)
    if containsItemSetsWithMultipleItems:
        prefixSpanWithMultipleItems(seq, dat, path)
    else:
        prefixSpanWithSingleItems(seq, dat, path)
    end = int(round(time.time()*1000))
    print(patternCount)
    print("Time is {} ms ".format(end - start))
    print("Memory Space is {} KB".format(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss))
