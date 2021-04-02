import sys
from itertools import combinations
from abstractP import *

maxPer = float()
minSup = float()
lno = 0
rank = {}
rank2 = {}
finalPatterns = {}


class Interval(object):
    def __init__(self, start, end, per, sup):
        self.start = start
        self.end = end
        self.per = per
        self.sup = sup


class Nodesummaries(object):
    def __init__(self):
        self.summ = []

    def insert(self, tid):
        k = self.summ[-1]
        diff = tid-k.end
        if diff <= maxPer:
            k.end = tid
            k.per = max(diff, k.per)
            k.sup += 1
        else:
            self.summ.append(Interval(tid, tid, 0, 1))
        return self.summ


class Node(object):
    """
            A class used to represent the node of frequentPatternTree

                ...

                Attributes
                ----------
                item : int
                    storing item of a node
                timeStamps : list
                    To maintain the timestamps of transaction at the end of the branch
                parent : node
                    To maintain the parent of every node
                children : list
                    To maintain the children of node

                Methods
                -------

                addChild(itemName)
                    storing the children to their respective parent nodes
            """
    def __init__(self, item, children):
        self.item = item
        self.children = children
        self.parent = None
        self.timeStamps = Nodesummaries()

    def addChild(self, node):
        self.children[node.item] = node
        node.parent = self


class Tree(object):
    """
                A class used to represent the frequentPatternGrowth tree structure

                ...

                Attributes
                ----------
                root : Node
                    Represents the root node of the tree
                summaries : dictionary
                    storing the nodes with same item name
                info : dictionary
                    stores the support of items


                Methods
                -------
                add_transaction(transaction)
                    creating transaction as a branch in frequentPatternTree
                addTransaction(prefixPaths, supportOfItems)
                    construct the conditional tree for prefix paths
                condition_patterns(Node)
                    generates the conditional patterns from tree for specific node
                cond_trans(prefixPaths,Support)
                    takes the prefixPath of a node and support at child of the path and extract the frequent items from
                    prefixPaths and generates prefixPaths with items which are frequent
                remove(Node)
                    removes the node from tree once after generating all the patterns respective to the node
                generate_patterns(Node)
                    starts from the root node of the tree and mines the frequent patterns

            """
    def __init__(self):
        self.root = Node(None, {})
        self.summaries = {}
        self.info = {}

    def addTransaction(self, transaction, tid):
        """
        adding transaction into tree

                :param transaction : it represents the one transactions in database
                :type transaction : list
                :param tid : represents the timestamp of transaction
                :type tid : int
        """

        currentNode = self.root
        for i in range(len(transaction)):
            if transaction[i] not in currentNode.children:
                newNode = Node(transaction[i], {})
                currentNode.addChild(newNode)
                if transaction[i] in self.summaries:
                    self.summaries[transaction[i]].append(newNode)
                else:
                    self.summaries[transaction[i]] = [newNode]
                currentNode = newNode
            else:
                currentNode = currentNode.children[transaction[i]]
        if len(currentNode.timeStamps.summ) != 0:
            currentNode.timeStamps.insert(tid)
        else:
            currentNode.timeStamps.summ.append(Interval(tid, tid, 0, 1))

    def addConditionalPatterns(self, transaction, tid):
        """
               adding conditional transaction into conditional tree

                    :param transaction : it represents the one transactions in database
                    :type transaction : list
                    :param tid : represents the timestamp of transaction
                    :type tid : int
               """
        currentNode = self.root
        for i in range(len(transaction)):
            if transaction[i] not in currentNode.children:
                newNode = Node(transaction[i], {})
                currentNode.addChild(newNode)
                if transaction[i] in self.summaries:
                    self.summaries[transaction[i]].append(newNode)
                else:
                    self.summaries[transaction[i]] = [newNode]
                currentNode = newNode
            else:
                currentNode = currentNode.children[transaction[i]]
        if len(currentNode.timeStamps.summ) != 0:
            currentNode.timeStamps.summ = self.merge(currentNode.timeStamps.summ, tid)
        else:
            currentNode.timeStamps.summ = tid

    def getConditionalTransactions(self, alpha):
        """ It generates the conditional patterns of a node

                :param alpha : the name of particular node
                :type alpha : node
                        """
        finalPatterns = []
        finaltimeStamps = []
        for i in self.summaries[alpha]:
            set1 = i.timeStamps.summ
            set2 = []
            while i.parent.item != None:
                set2.append(i.parent.item)
                i = i.parent
            if len(set2) > 0:
                set2.reverse()
                finalPatterns.append(set2)
                finaltimeStamps.append(set1)
        finalPatterns, finaltimeStamps, info = self.conditionalTransactions(finalPatterns, finaltimeStamps)
        return finalPatterns, finaltimeStamps, info
    
    def removeNode(self, nodeValue):
        """removing the node from tree

                                :param nodeValue : it represents the node in tree
                                :type nodeValue : node
                                """
        for i in self.summaries[nodeValue]:
            if len(i.parent.timeStamps.summ) != 0:
                i.parent.timeStamps.summ = self.merge(i.parent.timeStamps.summ, i.timeStamps.summ)
            else:
                i.parent.timeStamps.summ = i.timeStamps.summ
            del i.parent.children[nodeValue]
            del i
        del self.summaries[nodeValue]

    def getTimestamps(self, alpha):
        timstamps = []
        for i in self.summaries[alpha]:
            timstamps += i.timeStamps
        return timstamps

    def check(self):
        k = self.root
        while len(k.children) != 0:
            if len(k.children) > 1:
                return 1
            if len(k.children) != 0 and len(k.timeStamps.summ) > 0:
                return 1
            for j in k.children:
                v = k.children[j]
            k = v
        return -1

    def getSupportAndPeriod(self, timeStamps):
        """
                   calculates the support and periodicity with list of timestamps

                   :param timeStamps : timestamps of a pattern
                   :type timeStamps : list


                           """
        global minSup, maxPer
        cur = 0
        per = 0
        sup = 0
        for j in range(len(timeStamps)):
            per = max(per, timeStamps[j].start - cur)
            per = max(per, timeStamps[j].per)
            if per > maxPer:
                return [0, 0]
            cur = timeStamps[j].end
            sup += timeStamps[j].sup
        per = max(per, lno - cur)
        return [sup, per]

    def conditionalTransactions(self, conditionalPatterns, conditionalTimestamps):
        """ It generates the conditional patterns with periodic frequent items

            :param conditionalPatterns : conditional_patterns generated from condition_pattern method for
                                            respective node
            :type conditionalPatterns : list
            :param conditionalTimestamps : represensts the timestamps of conditional patterns of a node
            :type conditionalTimestamps : list
            """
        global minSup, maxPer
        pat = []
        timeStamps = []
        data1 = {}
        for i in range(len(conditionalPatterns)):
            for j in conditionalPatterns[i]:
                if j in data1:
                    data1[j] = self.merge(data1[j], conditionalTimestamps[i])
                else:
                    data1[j] = conditionalTimestamps[i]

        updatedDict = {}
        for m in data1:
            updatedDict[m] = self.getSupportAndPeriod(data1[m])
        updatedDict = {k: v for k, v in updatedDict.items() if v[0] >= minSup and v[1] <= maxPer}
        count = 0
        for p in conditionalPatterns:
            p1 = [v for v in p if v in updatedDict]
            trans = sorted(p1, key=lambda x: (updatedDict.get(x)[0], -x), reverse=True)
            if len(trans) > 0:
                pat.append(trans)
                timeStamps.append(conditionalTimestamps[count])
            count += 1
        return pat, timeStamps, updatedDict

    def merge(self, summaries1, summaries2):
        global minSup, maxPer
        iter1 = 0
        iter2 = 0
        mergedSummaries = []
        l1 = len(summaries1)
        l2 = len(summaries2)
        while 1:
            if summaries1[iter1].start < summaries2[iter2].start:
                if summaries1[iter1].end < summaries2[iter2].start:
                    diff = summaries2[iter2].start - summaries1[iter1].end
                    if diff > maxPer:
                        mergedSummaries.append(Interval(summaries1[iter1].start, summaries1[iter1].end, summaries1[iter1].per, summaries1[iter1].sup))
                        iter1 += 1
                        if iter1 >= l1:
                            ck = 1
                            break
                    else:
                        per1 = max(diff, summaries1[iter1].per)
                        per1 = max(per1, summaries2[iter2].per)
                        mergedSummaries.append(
                            Interval(summaries1[iter1].start, summaries2[iter2].end, per1, summaries1[iter1].sup + summaries2[iter2].sup))
                        iter1 += 1
                        iter2 += 1
                        if iter1 >= l1:
                            ck = 1
                            break

                        if iter2 >= l2:
                            ck = 2
                            break

                else:
                    if summaries1[iter1].end > summaries2[iter2].end:
                        mergedSummaries.append(Interval(summaries1[iter1].start, summaries1[iter1].end, summaries1[iter1].per,
                                               summaries1[iter1].sup + summaries2[iter2].sup))
                    else:
                        per1 = max(summaries1[iter1].per, summaries2[iter2].per)
                        mergedSummaries.append(
                            Interval(summaries1[iter1].start, summaries2[iter2].end, per1, summaries1[iter1].sup + summaries2[iter2].sup))
                    iter1 += 1
                    iter2 += 1
                    if iter1 >= l1:
                        ck = 1
                        break

                    if iter2 >= l2:
                        ck = 2
                        break
            else:
                if summaries2[iter2].end < summaries1[iter1].start:
                    diff = summaries1[iter1].start - summaries2[iter2].end
                    if diff > maxPer:
                        mergedSummaries.append(
                            Interval(summaries2[iter2].start, summaries2[iter2].end, summaries2[iter2].per, summaries2[iter2].sup))
                        iter2 += 1
                        if iter2 >= l2:
                            ck = 2
                            break
                    else:
                        per1 = max(diff, summaries2[iter2].per)
                        per1 = max(per1, summaries1[iter1].per)
                        mergedSummaries.append(
                            Interval(summaries2[iter2].start, summaries1[iter1].end, per1, summaries2[iter2].sup + summaries1[iter1].sup))
                        iter2 += 1
                        iter1 += 1
                        if iter2 >= l2:
                            ck = 2
                            break

                        if iter1 >= l1:
                            ck = 1
                            break

                else:
                    if summaries2[iter2].end > summaries1[iter1].end:
                        mergedSummaries.append(Interval(summaries2[iter2].start, summaries2[iter2].end, summaries2[iter2].per,
                                               summaries2[iter2].sup + summaries1[iter1].sup))
                    else:
                        per1 = max(summaries2[iter2].per, summaries1[iter1].per)
                        mergedSummaries.append(
                            Interval(summaries2[iter2].start, summaries1[iter1].end, per1, summaries2[iter2].sup + summaries1[iter1].sup))
                    iter2 += 1
                    iter1 += 1
                    if iter2 >= l2:
                        ck = 2
                        break

                    if iter1 >= l1:
                        ck = 1
                        break
        if ck == 1:
            while iter2 < l2:
                mergedSummaries.append(summaries2[iter2])
                iter2 += 1
        else:
            while iter1 < l1:
                mergedSummaries.append(summaries1[iter1])
                iter1 += 1
        mergedSummaries = self.update(mergedSummaries)
        return mergedSummaries

    def update(self, mergedSummaries):
        global minSup, maxPer
        outsumm = [mergedSummaries[0]]
        cur = mergedSummaries[0]
        for i in range(1, len(mergedSummaries)):
            v = (mergedSummaries[i].start - cur.end)
            if cur.end > mergedSummaries[i].start or v <= maxPer:
                cur.end = max(mergedSummaries[i].end, cur.end)
                cur.sup += mergedSummaries[i].sup
                cur.per = max(cur.per, mergedSummaries[i].per)
                cur.per = max(cur.per, v)
            else:
                outsumm.append(mergedSummaries[i])
            cur = outsumm[-1]
        return outsumm

    def subLists(self, myList):
        subs = []
        for i in range(1, len(myList) + 1):
            temp = [list(x) for x in combinations(myList, i)]
            if len(temp) > 0:
                subs.extend(temp)
        return subs

    def generatePatterns(self, prefix):
        """generates the patterns

                        :param prefix : forms the combination of items
                        :type prefix : list
                        """
        for i in sorted(self.summaries, key=lambda x: (self.info.get(x)[0], -x)):
            pattern = prefix[:]
            pattern.append(pfList[i])
            yield pattern, self.info[i]
            patterns, timeStamps, info = self.getConditionalTransactions(i)
            conditionalTree = Tree()
            conditionalTree.info = info.copy()
            for pat in range(len(patterns)):
                conditionalTree.addConditionalPatterns(patterns[pat], timeStamps[pat])
            find = conditionalTree.check()
            if find == 1:
                del patterns, timeStamps, info
                for cp in conditionalTree.generatePatterns(pattern):
                    yield cp
            else:
                if len(conditionalTree.info) != 0:
                    j = []
                    for r in timeStamps:
                        j += r
                    inf = self.getSupportAndPeriod(j)
                    patterns[0].reverse()
                    upp = []
                    for jm in patterns[0]:
                        upp.append(pfList[jm])
                    allsub = self.subLists(upp)
                    for pa in allsub:
                        yield pattern + pa, inf
                del patterns, timeStamps, info
                del conditionalTree
            self.removeNode(i)


class Psgrowth():

    rank = {}
    iFile = str()
    oFile = str()
    minSup = float()
    maxPer = float()
    finalPatterns = {}

    def periodicFrequentOneItem(self):
        """
                    calculates the support of each item in the dataset and assign the ranks to the items
                    by decreasing support and returns the frequent items list

                    """
        global rank, lno, minSup, maxPer
        data = {}
        with open(self.iFile, 'r') as f:
            for line in f:
                lno += 1
                tr = line.split()
                for i in range(1, len(tr)):
                    if tr[i] not in data:
                        data[tr[i]] = [int(tr[0]), int(tr[0]), 1]
                    else:
                        data[tr[i]][0] = max(data[tr[i]][0], (int(tr[0]) - data[tr[i]][1]))
                        data[tr[i]][1] = int(tr[0])
                        data[tr[i]][2] += 1
        for key in data:
            data[key][0] = max(data[key][0], lno - data[key][1])
        minSup = (self.minSup * lno)
        maxPer = (self.maxPer * lno)
        data = {k: [v[2], v[0]] for k, v in data.items() if v[0] <= maxPer and v[2] >= minSup}
        genList = [k for k, v in sorted(data.items(), key=lambda x: (x[1][0], x[0]), reverse=True)]
        rank = dict([(index, item) for (item, index) in enumerate(genList)])
        return data, genList

    def buildTree(self, info, dict1):
        """it takes the transactions and support of each item and construct the main tree with setting root
                            node as null

            :param info : it represents the support of each item
            :type info : dictionary
            :param dict1 : it represents the one transactions in database
            :type dict1 : list
            """
        rootNode = Tree()
        rootNode.info = info.copy()
        with open(self.iFile, 'r') as f:
            for line in f:
                tr = line.split()
                list2 = [int(tr[0])]
                for i in range(1, len(tr)):
                    if tr[i] in dict1:
                        list2.append(rank[tr[i]])
                if len(list2) >= 2:
                    basket = list2[1:]
                    basket.sort()
                    list2[1:] = basket[0:]
                    rootNode.addTransaction(list2[1:], list2[0])
        return rootNode

    def startMine(self):
        """
                    Main method where the patterns are mined by constructing tree.

                """
        self.startTime = time.time()
        global pfList, lno, rank2, minSup, maxPer, finalPatterns
        generatedDict, pfList = self.periodicFrequentOneItem()
        info = {rank[k]: v for k, v in generatedDict.items()}
        Tree = self.buildTree(info, generatedDict)
        z = Tree.generatePatterns([])
        for k in z:
            self.finalPatterns[tuple(str(k[0]))]=str(k[1])
        self.endTime = time.time()
        process = psutil.Process(os.getpid())
        self.memoryUSS = process.memory_full_info().uss
        self.memoryRSS = process.memory_info().rss
        print("Frequent patterns were generated successfully using Pfgrowth algorithm ")

    def getMemoryUSS(self):
        """Total amount of USS memory consumed by the mining process will be retrieved from this function

        :return: returning USS memory consumed by the mining process
        :rtype: float
        """

        return self.memoryUSS

    def getMemoryRSS(self):
        """Total amount of RSS memory consumed by the mining process will be retrieved from this function

        :return: returning RSS memory consumed by the mining process
        :rtype: float
        """

        return self.memoryRSS

    def getRuntime(self):
        """Calculating the total amount of runtime taken by the mining process


        :return: returning total amount of runtime taken by the mining process
        :rtype: float
        """

        return self.endTime - self.startTime

    def getPatternsInDataFrame(self):
        """Storing final frequent patterns in a dataframe

        :return: returning frequent patterns in a dataframe
        :rtype: pd.DataFrame
        """

        dataFrame = {}
        data = []
        for a, b in self.finalPatterns.items():
            data.append([a, b])
            dataFrame = pd.DataFrame(data, columns=['Patterns', 'Support'])
        return dataFrame

    def storePatternsInFile(self, outFile):
        """Complete set of frequent patterns will be loaded in to a output file

        :param outFile: name of the output file
        :type outFile: file
        """
        self.oFile = outFile
        writer = open(self.oFile, 'w+')
        for x, y in self.finalPatterns.items():
            s1 = str(x) + ":" + str(y)
            writer.write("%s \n" % s1)

    def getFrequentPatterns(self):
        """ Function to send the set of frequent patterns after completion of the mining process

        :return: returning frequent patterns
        :rtype: dict
        """
        return self.finalPatterns

if __name__ == "__main__":
    ap = Psgrowth()
    ap.iFile = sys.argv[1]
    ap.oFile = sys.argv[2]
    ap.minSup = float(sys.argv[3])
    ap.maxPer = float(sys.argv[4])
    ap.startMine()
    frequentPatterns = ap.getFrequentPatterns()
    print("Total number of Frequent Patterns:", len(frequentPatterns))
    ap.storePatternsInFile(sys.argv[2])
    memUSS = ap.getMemoryUSS()
    print("Total Memory in USS:", memUSS)
    memRSS = ap.getMemoryRSS()
    print("Total Memory in RSS", memRSS)
    run = ap.getRuntime()
    print("Total ExecutionTime in seconds:", run)
