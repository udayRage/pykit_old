from abstract import *

class Apriori(frequentPatterns):
    """ Apriori main class"""

    minSup = float()
    startTime = float()
    endTime = float()
    finalPatterns = {}
    iData = " "
    oFile = " "
    transaction = []

    def cList2FpList(self, cList):
        """Generates frequent item sets from the candidate item sets

        :param cList: Candidate item sets will be given as input
        :type cList: list
        :return: returning set of all frequent item sets
        :rtype: dict
        """

        global minSup, transaction
        minSup = float(self.minSup)
        c2FList = {}
        for i in transaction:
            dictionary = {frozenset(j): int(c2FList.get(frozenset(j), 0)) + 1 for j in cList if j.issubset(i)}
            c2FList.update(dictionary)
        c2FList = {key: value for key, value in c2FList.items() if value >= minSup}
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

        global startTime, endTime, iData, transaction

        # count = 0
        # numberOfFrequent = []
        startTime = time.time()
        iData = self.iData
        with open(iData, 'r') as f:
            transaction = [set(line.split(',')) for line in f]
            f.close()

        itemsList = sorted(list(set.union(*transaction)))  # because transaction is list
        items = [{i} for i in itemsList]
        itemsCount = len(items)

        for i in range(1, itemsCount):
            fpSet = self.cList2FpList(items)
            if len(fpSet) == 0:
                print("No frequent sets")

            for li in fpSet:
                print(sorted(li), "Support Count = ", fpSet[li])
            self.finalPatterns.update(fpSet)
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

    def getRuntime(self):
        """Calculating the total amount of execution time taken by the Apriori algorithm"""

        global endTime, startTime
        return endTime - startTime

    def getPatternsInDataFrame(self):
        """Storing final frequent item sets in a dataframe and converting it to .csv file"""

        # finalPatterns = self.finalPatterns
        global finalPatterns
        df = {}
        data = []
        for a, b in finalPatterns.items():
            data.append([a, b])
            df = pd.DataFrame(data, columns=['Patterns', 'Support'])
        return df

    def storePatternsInFile(self, outFile):
        """Main apriori function receiving input file path, list of minimum support values, nodes, and nonLeaf

        :param outFile: .csv output file name
        :type outFile: file
        """
        global oFile, finalPatterns
        oFile = outFile
        writer = open(oFile, 'w+')
        for x, y in finalPatterns.items():
            # s = "output" + str(x)
            s1 = str(x) + ":" + str(y)
            writer.write("%s \n" % s1)
        # InFile()

    def getFrequentPatterns(self):
        """ Function to send the set of frequent item sets after completion of the mining process

        :return: returning frequent item sets
        :rtype: dict
        """
        global finalPatterns

        return self.finalPatterns
