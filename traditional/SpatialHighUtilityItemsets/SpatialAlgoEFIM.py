import sys
import time
from functools import cmp_to_key
from Transaction import Transaction
from SpatialDataset import Dataset
import psutil


class SpatialAlgoEFIM:
    # set of high utility itemsets
    highUtilityItemsets = []
    startTimestamp = 0
    endTimestamp = 0
    minUtil = 0
    candidateCount = 0
    # an dictionary to hold the twu values of the items in database
    utilityBinArrayLU = {}
    # an dictionary to hold the subtree utility values of the items is database
    utilityBinArraySU = {}
    # an dictionary to store the new name corresponding to old name
    oldNamesToNewNames = {}
    # an dictionary to store the old name corresponding to new name
    newNamesToOldNames = {}
    # a dictionary to store the neighbours of a item
    Neighbours = {}
    # a temporary buffer
    temp = []
    # maximum memory used by this program for runnning
    maxMemory = 0
    for i in range(5000):
        temp.append(0)

    def __init__(self, inputPath, outputPath, NeighbourFile):
        self.patternCount = 0
        self.inputPath = inputPath
        self.outputPath = outputPath
        self.NeighbourFile = NeighbourFile
        self.f = open(outputPath, 'w')

    def runAlgorithm(self, minUtil):
        self.startTimestamp = time.time()
        with open(self.NeighbourFile, 'r') as o:
            lines = o.readlines()
            for line in lines:
                line_split = line.split()
                self.Neighbours[int(line_split[0])] = [int(x) for x in line_split[1:]]
        o.close()
        dataset = Dataset(self.inputPath)
        self.minUtil = minUtil
        # reset the maxMemory used
        InitialMemory = psutil.virtual_memory()[3]
        # scan the database using utility bin array to caluclate the pmus
        self.useUtilityBinArrayToCalculateLocalUtilityFirstTime(dataset)
        # now we keep only the promising items ie items having twu >= minUtil
        itemsToKeep = []
        for key in self.utilityBinArrayLU.keys():
            if self.utilityBinArrayLU[key] >= minUtil:
                itemsToKeep.append(key)
        # sort the promising items according to increasing order of their pmus
        itemsToKeep = sorted(itemsToKeep, key=lambda x: self.utilityBinArrayLU[x])
        # print(itemsToKeep)
        # we will give the new names for all promising items starting from 1
        currentName = 1
        for idx, item in enumerate(itemsToKeep):
            self.oldNamesToNewNames[item] = currentName
            self.newNamesToOldNames[currentName] = item
            itemsToKeep[idx] = currentName
            currentName += 1
        # loop over every transaction in database to remove the unpromising items
        for transaction in dataset.getTransactions():
            transaction.removeUnpromisingItems(self.oldNamesToNewNames)
        # now we will sort the transactions according to proposed total order on transaction
        self.sortDatabase(dataset.getTransactions())
        # after removing the unimportant items from the database some items become empty
        # so remove those transactions
        emptyTransactionCount = 0
        for transaction in dataset.getTransactions():
            if len(transaction.getItems()) == 0:
                emptyTransactionCount += 1
        dataset.transactions = dataset.transactions[emptyTransactionCount:]
        # use utilitybinarraysu to caluclate the neighbourhood subtree utility of each item
        self.useUtilityBinArrayToCalculateSubtreeUtilityFirstTime(dataset)
        # prune the items which do not satisfy subtree utility conditions
        itemsToExplore = []
        for item in itemsToKeep:
            if self.utilityBinArraySU[item] >= minUtil:
                itemsToExplore.append(item)
        # print(itemsToExplore)
        # print(itemsToKeep)
        # print(self.oldNamesToNewNames)
        # print(self.newNamesToOldNames)
        self.backtrackingEFIM(dataset.getTransactions(), itemsToKeep, itemsToExplore, 0)
        finalMemory = psutil.virtual_memory()[3]
        memory = (finalMemory - InitialMemory) / 10000
        if memory > self.maxMemory:
            self.maxMemory = memory
        self.endTimestamp = time.time()
        self.f.close()

    def backtrackingEFIM(self, transactionsOfP, itemsToKeep, itemsToExplore, prefixLength):
        self.candidateCount += len(itemsToExplore)
        for idx, e in enumerate(itemsToExplore):
            initialMemory = psutil.virtual_memory()[3]
            # caluclate the transactions containing p U {e}
            # at the same time project transactions to keep what appears after e
            transactionsPe = []
            # variable to caluclate the utility of Pe
            utilityPe = 0
            # merging transactions
            previousTransaction = transactionsOfP[0]
            consecutiveMergeCount = 0
            for transaction in transactionsOfP:
                items = transaction.getItems()
                if e in items:
                    # if e was found in the transaction
                    positionE = items.index(e)
                    if transaction.getLastPosition() == positionE:
                        utilityPe += transaction.getUtilities()[positionE] + transaction.prefixUtility
                    else:
                        projectedTransaction = transaction.projectTransaction(positionE)
                        utilityPe += projectedTransaction.prefixUtility
                        if previousTransaction == transactionsOfP[0]:
                            # if it is the first transactoin
                            previousTransaction = projectedTransaction
                        elif self.is_equal(projectedTransaction, previousTransaction):
                            if consecutiveMergeCount == 0:
                                # if the first consecutive merge
                                items = previousTransaction.items[previousTransaction.offset:]
                                utilities = previousTransaction.utilities[previousTransaction.offset:]
                                itemsCount = len(items)
                                positionPrevious = 0
                                positionProjection = projectedTransaction.offset
                                while positionPrevious < itemsCount:
                                    utilities[positionPrevious] += projectedTransaction.utilities[positionProjection]
                                    positionPrevious += 1
                                    positionProjection += 1
                                previousTransaction.prefixUtility += projectedTransaction.prefixUtility
                                sumUtilities = previousTransaction.prefixUtility
                                previousTransaction = Transaction(items, utilities, previousTransaction.transactionUtility + projectedTransaction.transactionUtility)
                                previousTransaction.prefixUtility = sumUtilities
                            else:
                                positionPrevious = 0
                                positionProjected = projectedTransaction.offset
                                itemsCount = len(previousTransaction.items)
                                while positionPrevious < itemsCount:
                                    previousTransaction.utilities[positionPrevious] += projectedTransaction.utilities[
                                        positionProjected]
                                    positionPrevious += 1
                                    positionProjected += 1
                                previousTransaction.transactionUtility += projectedTransaction.transactionUtility
                                previousTransaction.prefixUtility += projectedTransaction.prefixUtility
                            consecutiveMergeCount += 1
                        else:
                            transactionsPe.append(previousTransaction)
                            previousTransaction = projectedTransaction
                            consecutiveMergeCount = 0
                    transaction.offset = positionE
            if previousTransaction != transactionsOfP[0]:
                transactionsPe.append(previousTransaction)
            self.temp[prefixLength] = self.newNamesToOldNames[e]
            if utilityPe >= self.minUtil:
                self.output(prefixLength, utilityPe)
            # caluclate the set which is intersection of all the neighbours of items present in P U {e}
            neighbourhoodList = self.caluclateNeighbourIntersection(prefixLength)
            # caluclate the local utility and subtree utility
            self.useUtilityBinArraysToCalculateUpperBounds(transactionsPe, idx, itemsToKeep, neighbourhoodList)
            newItemsToKeep = []
            newItemsToExplore = []
            for l in range(idx + 1, len(itemsToKeep)):
                itemk = itemsToKeep[l]
                if self.utilityBinArraySU[itemk] >= self.minUtil:
                    if itemk in neighbourhoodList:
                        newItemsToExplore.append(itemk)
                        newItemsToKeep.append(itemk)
                elif self.utilityBinArrayLU[itemk] >= self.minUtil:
                    if itemk in neighbourhoodList:
                        newItemsToKeep.append(itemk)
            self.backtrackingEFIM(transactionsPe, newItemsToKeep, newItemsToExplore, prefixLength + 1)
            finalMemory = psutil.virtual_memory()[3]
            memory = (finalMemory - initialMemory) / 10000
            if self.maxMemory < memory:
                self.maxMemory = memory


    def intersection(self, lst1, lst2):
        # Use of hybrid method
        temp = set(lst2)
        lst3 = [value for value in lst1 if value in temp]
        return lst3

    def caluclateNeighbourIntersection(self, prefixLength):
        intersectionList = self.Neighbours[self.temp[0]]
        for i in range(1, prefixLength+1):
            intersectionList = self.intersection(self.Neighbours[self.temp[i]], intersectionList)
        finalIntersectionList = []
        for item in intersectionList:
            if item in self.oldNamesToNewNames:
                finalIntersectionList.append(self.oldNamesToNewNames[item])
        return finalIntersectionList

    def useUtilityBinArraysToCalculateUpperBounds(self, transactionsPe, j, itemsToKeep, neighbourhoodList):
        for i in range(j + 1, len(itemsToKeep)):
            item = itemsToKeep[i]
            self.utilityBinArrayLU[item] = 0
            self.utilityBinArraySU[item] = 0
        for transaction in transactionsPe:
            length = len(transaction.getItems())
            i = length - 1
            while i >= transaction.offset:
                item = transaction.getItems()[i]
                if item in itemsToKeep:
                    remainingUtility = 0
                    if self.newNamesToOldNames[item] in self.Neighbours:
                        item_neighbours = self.Neighbours[self.newNamesToOldNames[item]]
                        for k in range(i, length):
                            transaction_item = transaction.getItems()[k]
                            if self.newNamesToOldNames[transaction_item] in item_neighbours and transaction_item in neighbourhoodList:
                                remainingUtility += transaction.getUtilities()[k]

                    remainingUtility += transaction.getUtilities()[i]
                    self.utilityBinArraySU[item] += remainingUtility + transaction.prefixUtility
                    self.utilityBinArrayLU[item] += transaction.transactionUtility + transaction.prefixUtility
                i -= 1

    def output(self, tempPosition, utility):
        self.patternCount += 1
        for i in range(0, tempPosition+1):
            self.f.write(str(self.temp[i]))
            if i != tempPosition:
                self.f.write(' ')
        self.f.write(' #UTIL: ')
        self.f.write(str(utility))
        self.f.write('\n')

    def is_equal(self, transaction1, transaction2):
        length1 = len(transaction1.items) - transaction1.offset
        length2 = len(transaction2.items) - transaction2.offset
        if length1 != length2:
            return False
        position1 = transaction1.offset
        position2 = transaction2.offset
        while position1 < len(transaction1.items):
            if transaction1.items[position1] != transaction2.items[position2]:
                return False
            position1 += 1
            position2 += 1
        return True

    def useUtilityBinArrayToCalculateSubtreeUtilityFirstTime(self, dataset):
        for transaction in dataset.getTransactions():
            items = transaction.getItems()
            utilities = transaction.getUtilities()
            for idx, item in enumerate(items):
                if item not in self.utilityBinArraySU:
                    self.utilityBinArraySU[item] = 0
                if self.newNamesToOldNames[item] not in self.Neighbours:
                    self.utilityBinArraySU[item] += utilities[idx]
                    continue
                i = idx + 1
                sumSu = utilities[idx]
                while i < len(items):
                    if self.newNamesToOldNames[items[i]] in self.Neighbours[self.newNamesToOldNames[item]]:
                        sumSu += utilities[i]
                    i += 1
                self.utilityBinArraySU[item] += sumSu

    def sortDatabase(self, transactions):
        cmp_items = cmp_to_key(self.sort_transaction)
        transactions.sort(key=cmp_items)

    def sort_transaction(self, trans1, trans2):
        trans1_items = trans1.getItems()
        trans2_items = trans2.getItems()
        pos1 = len(trans1_items) - 1
        pos2 = len(trans2_items) - 1
        if len(trans1_items) < len(trans2_items):
            while pos1 >= 0:
                sub = trans2_items[pos2] - trans1_items[pos1]
                if sub != 0:
                    return sub
                pos1 -= 1
                pos2 -= 1
            return -1
        elif len(trans1_items) > len(trans2_items):
            while pos2 >= 0:
                sub = trans2_items[pos2] - trans1_items[pos1]
                if sub != 0:
                    return sub
                pos1 -= 1
                pos2 -= 1
            return 1
        else:
            while pos2 >= 0:
                sub = trans2_items[pos2] - trans1_items[pos1]
                if sub != 0:
                    return sub
                pos1 -= 1
                pos2 -= 1
            return 0

    def useUtilityBinArrayToCalculateLocalUtilityFirstTime(self, dataset):
        for transaction in dataset.getTransactions():
            for idx, item in enumerate(transaction.getItems()):
                if item in self.utilityBinArrayLU:
                    self.utilityBinArrayLU[item] += transaction.getPmus()[idx]
                else:
                    self.utilityBinArrayLU[item] = transaction.getPmus()[idx]

    def printStats(self):
        print('EFIM STATS')
        print('Min Util = ' + str(self.minUtil))
        print(' High utility Itemsets count : ' + str(self.patternCount))
        print('Total Time : ' + str(self.endTimestamp - self.startTimestamp))
        print('Max memory used : ' + str(self.maxMemory))
        print('Candidate Count : ' + str(self.candidateCount))


if __name__ == '__main__':
    inputFile = sys.argv[1]
    neighbourFile = sys.argv[2]
    outputFile = sys.argv[3]
    minUtil = int(sys.argv[4])
    q = SpatialAlgoEFIM(inputFile, outputFile, neighbourFile)
    q.runAlgorithm(minUtil)
    q.printStats()
