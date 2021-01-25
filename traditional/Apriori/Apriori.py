from abstract import *


def fpList2CList(fpList, length):
    """Generates candidate item sets from the frequent item sets

    :param fpList: set of all frequent item sets to generate candidate item sets of each of size is length
    :type fpList: dict
    :param length: size of each candidate item sets to be generated
    :type length: int
    :return: set of candidate item sets in sorted order
    :rtype: list
    """

    fp2CList = []
    for i in fpList:
        nextList = [i | j for j in fpList if len(i | j) == length and (i | j) not in fp2CList]
        fp2CList.extend(nextList)
    return sorted(fp2CList)


class Apriori(frequentPatterns):
    """ Apriori main class

        ...

        Attributes
        ----------
        iData: str or pandas.DataFrame
            Input file name or path of the input file
        minSup : float
            UserSpecified minimum support value
        startTime :float
            To record the start time of the algorithm
        endTime:float
            To record the completion time of the algorithm
        finalPatterns : dict
            Storing the complete set of patterns in a dictionary variable
        oFile : str
            Name of the output file to store complete set of frequent patterns
        transaction : list
            To store the complete set of transactions

        Methods
        -------
        cList2FpList(self, cList)
            Candidate list to frequent item sets generation function
        startMine()
            Mining process will start from here
        getFrequentPatterns()
            Complete set of patterns will be retrieved with this function
        storePatternsInFile(oFile)
            Complete set of frequent patterns will be loaded in to a output file
        getPatternsInDataFrame()
            Complete set of frequent patterns will be loaded in to data frame
        getMemory()
            Total amount of memory consumed by the program will be retrieved from this function
        getRuntime()
            Total amount of runtime taken by the program will be retrieved from this function
    """

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

        c2FList = {}
        for i in self.transaction:
            dictionary = {frozenset(j): int(c2FList.get(frozenset(j), 0)) + 1 for j in cList if j.issubset(i)}
            c2FList.update(dictionary)
        c2FList = {key: value for key, value in c2FList.items() if value >= self.minSup}

        return c2FList

    def startMine(self):
        """ frequent pattern mining process will start from here"""

        self.startTime = time.time()
        with open(self.iData, 'r') as f:
            self.transaction = [set(line.split(',')) for line in f]
            f.close()

        itemsList = sorted(list(set.union(*self.transaction)))  # because transaction is list
        items = [{i} for i in itemsList]
        itemsCount = len(items)

        for i in range(1, itemsCount):
            fpSet = self.cList2FpList(items)
            if len(fpSet) == 0:
                print("No frequent sets")
            self.finalPatterns.update(fpSet)
            items = fpList2CList(fpSet, i + 1)
            if len(items) == 0:
                print("End of Frequent Item Sets")
                break  # finish apriori
        self.endTime = time.time()

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

        return self.endTime - self.startTime

    def getPatternsInDataFrame(self):
        """Storing final frequent item sets in a dataframe and converting it to .csv file"""

        df = {}
        data = []
        for a, b in self.finalPatterns.items():
            data.append([a, b])
            df = pd.DataFrame(data, columns=['Patterns', 'Support'])
        return df

    def storePatternsInFile(self, outFile):
        """Main apriori function receiving input file path, list of minimum support values, nodes, and nonLeaf

        :param outFile: .csv output file name
        :type outFile: file
        """
        self.oFile = outFile
        writer = open(self.oFile, 'w+')
        for x, y in self.finalPatterns.items():
            s1 = str(x) + ":" + str(y)
            writer.write("%s \n" % s1)

    def getFrequentPatterns(self):
        """ Function to send the set of frequent item sets after completion of the mining process

        :return: returning frequent item sets
        :rtype: dict
        """

        return self.finalPatterns
