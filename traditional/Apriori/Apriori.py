from traditional.abstractClass.abstractFrequentPatterns import *


class Apriori(frequentPatterns):
    """ Apriori main class

        ...

        Attributes
        ----------
        iFile : str
            Input file name or path of the input file
        minSup: float
            UserSpecified minimum support value. It has to be given in terms of percentage within the interval (0, 100)
        startTime:float
            To record the start time of the mining process
        endTime:float
            To record the completion time of the mining process
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
            Complete set of frequent patterns will be loaded in to a dataframe
        getMemoryUSS()
            Total amount of USS memory consumed by the mining process will be retrieved from this function
        getMemoryRSS()
            Total amount of RSS memory consumed by the mining process will be retrieved from this function
        getRuntime()
            Total amount of runtime taken by the mining process will be retrieved from this function
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
        """Generates frequent patterns from the candidate patterns

        :param candidateList: Candidate patterns will be given as input
        :type candidateList: list
        :return: returning set of all frequent patterns
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
        """Generates candidate patterns from the frequent patterns

        :param frequentList: set of all frequent patterns to generate candidate patterns of each of size is length
        :type frequentList: dict
        :param length: size of each candidate patterns to be generated
        :type length: int
        :return: set of candidate patterns in sorted order
        :rtype: list
        """

        frequent2CandidateList = []
        for i in frequentList:
            nextList = [i | j for j in frequentList if len(i | j) == length and (i | j) not in frequent2CandidateList]
            frequent2CandidateList.extend(nextList)
        return sorted(frequent2CandidateList)

    def startMine(self):
        """ Frequent pattern mining process will start from here"""

        self.startTime = time.time()
        with open(self.iFile, 'r') as f:
            self.transaction = [set([i.rstrip() for i in line.split(',')]) for line in f]
            f.close()
        self.minSup = int(math.ceil(self.minSup * len(self.transaction)) / 100)

        itemsList = sorted(list(set.union(*self.transaction)))  # because transaction is list
        items = [{i} for i in itemsList]
        itemsCount = len(items)

        for i in range(1, itemsCount):
            frequentSet = self.candidate2Frequent(items)
            # if len(frequentSet) == 0:
            #   print("No frequent sets")
            self.finalPatterns.update(frequentSet)
            items = self.frequent2Candidate(frequentSet, i + 1)
            if len(items) == 0:
                # print("End of frequent patterns")
                break  # finish apriori
        self.endTime = time.time()
        process = psutil.Process(os.getpid())
        self.memoryUSS = process.memory_full_info().uss
        self.memoryRSS = process.memory_info().rss
        print("Frequent patterns were generated successfully using Apriori algorithm ")

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
