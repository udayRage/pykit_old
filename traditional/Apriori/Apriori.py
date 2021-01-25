from traditional.abstractClass.abstractFrequentPatterns import *


class Apriori(frequentPatterns):
    """ Apriori main class

        ...

        Attributes
        ----------
        iFile : str
            Input file name or path of the input file
        minSup: float
            UserSpecified minimum support value and needs to be specified in the interval (0, 100)
        startTime:float
            To record the start time of the algorithm
        endTime:float
            To record the completion time of the algorithm
        finalPatterns: dict
            Storing the complete set of patterns in a dictionary variable
        oFile : str
            Name of the output file to store complete set of frequent patterns
        memoryUSS : float
            To store the total amount of USS memory consumed by the program
        memoryRSS : float
            To store the total amount of RSS memory consumed by the program

        Methods
        -------
        startMine()
            Mining process will start from here
        getFrequentPatterns()
            Complete set of patterns will be retrieved with this function
        storePatternsInFile(oFile)
            Complete set of frequent patterns will be loaded in to a output file
        getPatternsInDataFrame()
            Complete set of frequent patterns will be loaded in to data frame
        getMemoryUSS()
            Total amount of USS memory consumed by the program will be retrieved from this function
        getMemoryRSS()
            Total amount of RSS memory consumed by the program will be retrieved from this function
        getRuntime()
            Total amount of runtime taken by the program will be retrieved from this function
    """

    minSup = float()
    startTime = float()
    endTime = float()
    finalPatterns = {}
    iFile = " "
    oFile = " "
    memoryUSS = float()
    memoryRSS = float()
    transaction = []

    def candidate2Frequent(self, candidateList):
        """Generates frequent item sets from the candidate item sets

        :param candidateList: Candidate item sets will be given as input
        :type candidateList: list
        :return: returning set of all frequent item sets
        :rtype: dict
        """

        candidate2FrequentList = {}
        for i in self.transaction:
            dictionary = {frozenset(j): int(candidate2FrequentList.get(frozenset(j), 0)) + 1 for j in candidateList if
                          j.issubset(i)}
            candidate2FrequentList.update(dictionary)
        candidate2FrequentList = {key: value for key, value in candidate2FrequentList.items() if value >= self.minSup}

        return candidate2FrequentList

    @staticmethod
    def frequent2Candidate(frequentList, length):
        """Generates candidate item sets from the frequent item sets

        :param frequentList: set of all frequent item sets to generate candidate item sets of each of size is length
        :type frequentList: dict
        :param length: size of each candidate item sets to be generated
        :type length: int
        :return: set of candidate item sets in sorted order
        :rtype: list
        """

        frequent2CandidateList = []
        for i in frequentList:
            nextList = [i | j for j in frequentList if len(i | j) == length and (i | j) not in frequent2CandidateList]
            frequent2CandidateList.extend(nextList)
        return sorted(frequent2CandidateList)

    def startMine(self):
        """ frequent pattern mining process will start from here"""

        self.startTime = time.time()
        with open(self.iFile, 'r') as f:
            self.transaction = [set([i.rstrip() for i in line.split(',')]) for line in f]
            f.close()
        self.minSup = int(math.ceil(self.minSup * len(self.transaction)) / 100)
        itemsList = sorted(list(set.union(*self.transaction)))
        items = [{i} for i in itemsList]
        itemsCount = len(items)
        for i in range(1, itemsCount):
            frequentSet = self.candidate2Frequent(items)
            if len(frequentSet) == 0:
                print("No frequent sets")
            self.finalPatterns.update(frequentSet)
            items = self.frequent2Candidate(frequentSet, i + 1)
            if len(items) == 0:
                print("End of Frequent Item Sets")
                break  # finish apriori
        self.endTime = time.time()
        process = psutil.Process(os.getpid())
        self.memoryUSS = process.memory_full_info().uss
        self.memoryRSS = process.memory_info().rss

    def getMemoryUSS(self):
        """Total amount of USS memory consumed by the program will be retrieved from this function

        :return: returning total memory consumed in USS
        :rtype: float
        """

        return self.memoryUSS

    def getMemoryRSS(self):
        """Total amount of RSS memory consumed by the program will be retrieved from this function

        :return: returning total memory consumed in RSS
        :rtype: float
        """

        return self.memoryRSS

    def getRuntime(self):
        """Calculating the total amount of execution time taken by the Apriori algorithm

        :return: returning total runTime
        :rtype: float
        """

        return self.endTime - self.startTime

    def getPatternsInDataFrame(self):
        """Storing final frequent item sets in a dataFrame, column names as Patterns and support respectively

        :return: returning frequent item sets in a dataFrame
        :rtype: pandas data frame
        """

        dataFrame = {}
        data = []
        for a, b in self.finalPatterns.items():
            data.append([a, b])
            dataFrame = pd.DataFrame(data, columns=['Patterns', 'Support'])
        return dataFrame

    def storePatternsInFile(self, outFile):
        """Main apriori function receiving input file path, list of minimum support values, nodes, and nonLeaf

        :param outFile: .csv output file name
        :type outFile: file
        """

        self.oFile = outFile
        writer = open(self.oFile, 'w+')
        for x, y in self.finalPatterns.items():
            itemsAndSupport = str(x) + ":" + str(y)
            writer.write("%s \n" % itemsAndSupport)

    def getFrequentPatterns(self):
        """ Function to send the set of frequent item sets after completion of the mining process

        :return: returning frequent item sets
        :rtype: dict
        """

        return self.finalPatterns
