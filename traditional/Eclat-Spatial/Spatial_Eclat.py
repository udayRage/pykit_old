#from traditional.abstractClass.abstractFrequentPatterns import *
import sys
from array import *
import resource
import time
import functools
import time
import csv
import pandas as pd
from collections import defaultdict
from itertools import combinations as c
import os
import os.path
import psutil

class Eclat():
    """ ECLAT main class

            ...

            Attributes
            ----------
            iFile : str
                Input file name or path of the input file
            minSup: float
                UserSpecified minimum support value. It has to be given in terms of count of total number of
                transactions in the input database/file
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
            Database : list
                To store the complete set of transactions available in the input database/file

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
            findDelimiter(line)
                Identifying the delimiter of the input file
            creatingItemSets(iFileName)
                Storing the complete transactions of the database/input file in a database variable
            frequentOneItem()
                Generating one frequent patterns
            dictKeysToInt(iList)
                Converting dictionary keys to integer elements
            eclatGeneration(cList)
                It will generate the combinations of frequent items
            generateFrequentPatterns(tidList)
                It will generate the combinations of frequent items from a list of items
    """

    minSup = float()
    startTime = float()
    endTime = float()
    finalPatterns = {}
    iFile = " "
    oFile = " "
    nFileName = " "
    memoryUSS = float()
    memoryRSS = float()
    Database = []
    def __init__(self,iFile,nFile,minsup):
        self.iFile=iFile;
        self.nFileName=nFile;
        self.minSup=minsup
    @staticmethod
    def findDelimiter(line):
        """Identifying the delimiter of the input file

            :param line: list of special characters may be used by a user to separate the items in a input file
            :type line: list of string
            :returns: delimited string used in the input file to separate each item
            :rtype: string
            """
        listOfDelimiters = [',', '*', '&', ' ', '%', '$', '#', '@', '!', '    ', '*', '(', ')']
        delimiter = None
        # print(line)
        for i in listOfDelimiters:
            if i in line:
                return i
        return delimiter

    def creatingItemSets(self, iFileName):
        """Storing the complete transactions of the database/input file in a database variable

            :param iFileName: user given input file/input file path
            :type iFileName: str
            """
        # import pandas as pd
        # global Database
        self.Database = []
        lineNumber = 0
        # data = []
        if isinstance(iFileName, list):
            self.Database = iFileName
        if isinstance(iFileName, pd.DataFrame):
            if iFileName.empty:
                print("its empty..")
                quit()
            i = iFileName.columns.values.tolist()
            if 'Transactions' in i:
                self.Database = iFileName['Transactions'].tolist()
            if 'Patterns' in i:
                self.Database = iFileName['Patterns'].tolist()

        if '.CSV' in iFileName:
            file1 = pd.read_csv(iFileName)
            columns = list(file1.head(0))
            if "Patterns" in columns:
                with open(iFileName, newline='') as csvFile:
                    data = csv.DictReader(csvFile)
                    for row in data:
                        listValue = row['Patterns']
                        l1 = listValue.replace("[", "")
                        l2 = l1.replace("]", "")
                        li = list(l2.split(","))
                        li1 = [int(i) for i in li]
                        self.Database.append(li1)
            if "Transactions" in columns:
                with open(iFileName, newline='') as csvFile:
                    data = csv.DictReader(csvFile)
                    for row in data:
                        listValue = row['Transactions']
                        l1 = listValue.replace("[", "")
                        l2 = l1.replace("]", "")
                        li = list(l2.split(","))
                        li1 = [int(i) for i in li]
                        self.Database.append(li1)
        else:
            try:
                with open(iFileName, 'r', encoding='utf-8') as f:
                    for line in f:
                        # line.strip()
                        if lineNumber == 0:
                            lineNumber += 1
                            delimiter = self.findDelimiter([*line])
                            # li=[lineNumber]
                            li = line.split(delimiter)
                            li1 = [i.rstrip() for i in li]
                            self.Database.append([i.rstrip() for i in li1])
                            # else:
                            # self.Database.append(li)
                            # data.append([lineNumber,li1])
                        else:
                            lineNumber += 1
                            li = line.split(delimiter)
                            # if delimiter==',':
                            li1 = [i.rstrip() for i in li]
                            self.Database.append(li1)
            except IOError:
                print("File Not Found")
                quit()

        # else:
        # self.Database=iFileName['Transactions'].tolist()

    # function to get frequent one pattern
    def frequentOneItem(self):
        """Generating one frequent patterns"""

        candidate = {}
        # global finalPatterns, minSup, Database
        # self.minSup = self.minSup
        for i in range(len(self.Database)):
            for j in range(len(self.Database[i])):
                if self.Database[i][j] not in candidate:
                    candidate[self.Database[i][j]] = [i]
                else:
                    candidate[self.Database[i][j]] += [i]
        self.finalPatterns = {keys: value for keys, value in candidate.items() if len(value) >= self.minSup}
        #print(candidate)
    # def less_items():
    #    pass

    @staticmethod
    def dictKeysToInt(iList):
        """Converting dictionary keys to integer elements

        :param iList: Dictionary with patterns as keys and their support count as a value
        :type iList: dict
        :returns: list of integer patterns to represent dictionary keys
        :rtype: list
        """

        temp = []
        for ite in iList.keys():
            ite = [int(i) for i in ite.strip('[]').split(',')]
            temp.append(ite)
            # print(sorted(temp))
        return sorted(temp)

    def eclatGeneration(self, cList):
        """It will generate the combinations of frequent items

        :param cList :it represents the items with their respective transaction identifiers
        :type cList: dictionary
        :return: returning transaction dictionary
        :rtype: dict
        """
        # to generate all
        tidList = {}
        key = list(cList.keys())
        for i in range(0, len(key)):
            nighbousItems=self.getNighboirItems(key[i])
            for j in range(i + 1, len(key)):
                # print(c[key[i]],c[key[j]])
                if not key[j] in nighbousItems:
                	continue
                intersectionList = list(set(cList[key[i]]).intersection(set(cList[key[j]])))
                itemList = []
                itemList += key[i]
                itemList += key[j]
                if len(intersectionList) >= self.minSup:
                    itemList.sort()
                    if tuple(itemList) not in tidList:
                        tidList[tuple(set(itemList))] = intersectionList
        return tidList

    def generateFrequentPatterns(self, tidList):
        """It will generate the combinations of frequent items from a list of items

        :param tidList :it represents the items with their respective transaction identifiers
        :type tidList: dictionary
        :return: returning transaction dictionary
        :rtype: dict
        """
        tidList1 = {}
        if len(tidList) == 0:
            print("There are no more candidate sets")
        else:
            key = list(tidList.keys())
            for i in range(0, len(key)):
                nighbousItems=self.getNighboirItems(key[i])
                for j in range(i + 1, len(key)):
                    if not key[j] in nighbousItems:
                    	continue
                    intersectionList = list(set(tidList[key[i]]).intersection(set(tidList[key[j]])))
                    itemList = []
                    if len(intersectionList) >= self.minSup:
                        itemList += key[i], key[j]
                        itemList.sort()
                        tidList1[tuple(itemList)] = intersectionList

        return tidList1
    def getNighboirItems(self,keyset):
    	"""
    		A function to get Neighbours of a item
    		:param keyset:itemset
    		:type keyset:str or tuple
    		:return: set of common neighbours 
			:rtype:set
    	"""
    	itemsnibs=self.NighboursMap.keys();
    	if isinstance(keyset,str):
    		if(self.NighboursMap.get(keyset)==None):
    			return []
    		itemsnibs=list(set(itemsnibs).intersection(set(self.NighboursMap.get(keyset))))
    	if isinstance(keyset,tuple):
    		keyset=list(keyset)
    		#print(keyset)
    		for j in range(0,len(keyset)):
    			i=keyset[j]
    			itemsnibs=list(set(itemsnibs).intersection(set(self.NighboursMap.get(i))))
    	return itemsnibs
    def mapNighbours(self,name):
    	"""
    		A function to map items to their Neighbours
    		:param name: item name
    		:type name: int
    	"""
    	with open(name, 'r', encoding='utf-8') as f:
            for line in f:
                li = line.split()
                item=li[0]
                nighbs=li[1:]
                self.NighboursMap[item]=nighbs
    def startMine(self):
        """Frequent pattern mining process will start from here"""

        # global items_sets, endTime, startTime
        self.startTime = time.time()
        self.NighboursMap={}
        if self.iFile is None:
            raise Exception("Please enter the file path or file name:")
        iFileName = self.iFile
        if self.minSup is None:
            raise Exception("Please enter the Minimum Support")
        # Database = []
        if self.minSup <= 0:
            raise Exception(
                "Please enter the minimum support in terms of count of total number of transactions in the input"
                " database/file")
        self.creatingItemSets(iFileName)
        self.mapNighbours(self.nFileName)
        print(self.NighboursMap)
        self.frequentOneItem()
        frequentSet = self.generateFrequentPatterns(self.finalPatterns)

        for x, y in frequentSet.items():
            if x not in self.finalPatterns:
                self.finalPatterns[x] = y
        while 1:
            frequentSet = self.eclatGeneration(frequentSet)
            for x, y in frequentSet.items():
                if x not in self.finalPatterns:
                    self.finalPatterns[x] = y
            if len(frequentSet) == 0:
                break
        # print("Frequent patterns were generated successfully using Eclat algorithm")
        self.endTime = time.time()
        process = psutil.Process(os.getpid())
        self.memoryUSS = process.memory_full_info().uss
        self.memoryRSS = process.memory_info().rss
        print("Frequent patterns were generated successfully using Eclat algorithm")

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
            patternsAndSupport = str(x) + ":" + str(y)
            writer.write("%s \n" % patternsAndSupport)

    def getFrequentPatterns(self):
        """ Function to send the set of frequent patterns after completion of the mining process

        :return: returning frequent patterns
        :rtype: dict
        """
        return self.finalPatterns
if __name__ == "__main__":
	ap=Eclat(sys.argv[1],sys.argv[2],int(sys.argv[3]))
	ap.startMine()
	frequentPatterns = ap.getFrequentPatterns()
	print("Total number of Spatial Frequent Patterns:", len(frequentPatterns))
	ap.storePatternsInFile(sys.argv[4])
	memUSS = ap.getMemoryUSS()
	print("Total Memory in USS:", memUSS)
	memRSS = ap.getMemoryRSS()
	print("Total Memory in RSS", memRSS)
	run = ap.getRuntime()
	print("Total ExecutionTime in seconds:", run)