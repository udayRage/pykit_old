import time
import pandas as pd
import os
import os.path
import psutil

startTime = float
endTime = float


class Apriori:
    """ main apriori class"""


    def __init__(self, iFile, minSup):
        self.iFile = iFile
        self.minSup = minSup
        self.transaction = []
        self.finalFps = {}

    def cList2FpList(self, cList):
        """Generates frequent item sets from the candidate item sets

        :param cList: Candidate item sets will be given as input
        :type cList: list
        :return: returning set of all frequent item sets
        :rtype: dict
        """

        c2FList = {}
        for i in self.transaction:
            dictionary = {frozenset(j): int(c2FList.get(frozenset(j), 0)) + 1 for j in cList if j.issubset(i)}
            c2FList.update(dictionary)
        c2FList = {key: value for key, value in c2FList.items() if value >= self.minSup}
        return c2FList

    def fpList2CList(self, fpList, length):
        """Generates candidate item sets from the frequent item sets

        :param fpList: set of all frequent item sets to generate candidate item sets of each of size is length
        :type fpList: dict
        :param length: size of each candidate item sets to be generated
        :type length: int
        :return: set of candidate item sets in sorted order
        :rtype: list
        """

        fp2CList = []
        # list = []
        # fp2CList = [set(c) for c in combinations(a,length) if c not in fp2CList]
        for i in fpList:
            nextList = [i | j for j in fpList if len(i | j) == length and (i | j) not in fp2CList]
            fp2CList.extend(nextList)
        return sorted(fp2CList)

    def startMine(self):
        """ frequent pattern mining process will start from here"""

        global startTime, endTime
        startTime = time.time()
        fileName = self.iFile
        with open(fileName, 'r') as f:
            self.transaction = [set(line.split(',')) for line in f]
            f.close()

        itemsList = sorted(list(set.union(*self.transaction)))  # because transaction is list
        items = [{i} for i in itemsList]
        itemsCount = len(items)

        for i in range(1, itemsCount):
            fpSet = self.cList2FpList(items)
            if len(fpSet) == 0:
                print("No frequent sets")
            for li in fpSet:
                print(sorted(li), "Support Count = ", fpSet[li])
            self.finalFps.update(fpSet)
            items = self.fpList2CList(fpSet, i + 1)
            if len(items) == 0:
                print("End of Frequent Item Sets")
                break  # finish apriori'''
        endTime = time.time()

    def getMemory(self):
        """Calculating the amount of memory consumed by the Apriori algorithm"""

        # import psutil
        # global minSup
        process = psutil.Process(os.getpid())
        memory = process.memory_full_info().uss  # process.memory_info().rss
        memoryInMb = memory / (1024 * 1024)
        return memoryInMb
        # print(memoryInMb)  # in bytes
        # print("Total Memory is:", memoryInMb)

    def getRuntime(self):
        """Calculating the total amount of execution time taken by the Apriori algorithm"""

        global endTime, startTime
        return endTime - startTime

    def getPatternInDf(self):
        """Storing final frequent item sets in a dataframe and converting it to .csv file"""

        df = {}
        data = []
        for a, b in self.finalFps.items():
            data.append([a, b])
            df = pd.DataFrame(data, columns=['Patterns', 'Support'])
        return df

    def getPatternsInFile(self, oFile):
        """Main apriori function receiving input file path, list of minimum support values, nodes, and nonLeaf

        :param oFile: .csv output file name
        :type oFile: file
        """

        writer = open(oFile, 'w+')
        for x, y in self.finalFps.items():
            # s = "output" + str(x)
            s1 = str(x) + ":" + str(y)
            writer.write("%s \n" % s1)
        # InFile()

    def getFPs(self):
        """ Function to send the set of frequent item sets after completion of the mining process

        :return: returning frequent item sets
        :rtype: dict
        """

        return self.finalFps
