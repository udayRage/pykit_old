from abc import ABC, abstractmethod
import time
import csv
import pandas as pd
from collections import defaultdict
from itertools import combinations as c
import os
import os.path
import psutil


class frequentPatterns(ABC):
    """ This abstract base class defines the variables and methods that every frequent pattern mining algorithm must
    employ in PAMI

        ...

        Attributes
        ----------
        iData : str or pandas.DataFrame
            Input file name or path of the input file
        minSup: float
            UserSpecified minimum support value
        startTime:float
            to record the start time of the algorithm
        endTime:float
            to record the completed time of the algorithm
        finalPatterns: dict
            Storing the complete set of patterns in a dictionary variable
        oFile : str
            Name of the output file to store complete set of frequent patterns

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
        getMemory()
            Total amount of memory consumed by the program will be retrieved from this function
        getRuntime()
            Total amount of runtime taken by the program will be retrieved from this function
    """

    def __init__(self, iData, minSup, nodes=1000, nonLeaf=50):
        """
        :param iData: input data
        :type iData: str or pandas.DataFrame
        :param minSup: user specified minimum support value. It needs to be specified within the interval (0,1).
        :type minSup: float
        :param nodes: maximum number of children of the hash tree
        :type nodes: int
        :param nonLeaf: maximum number of elements in non leaf nodes of the hash tree
        :type nonLeaf: int
        """

        self.iData = iData
        self.minSup = minSup
        self.nodes = nodes
        self.nonLeaf = nonLeaf
        # self.finalPatterns = {}

    @abstractmethod
    def iData(self):
        """Variable to store the input file path/file name/data frame"""

        pass

    @abstractmethod
    def minSup(self):
        """Variable to store the user-specified minimum support value"""

        pass

    @abstractmethod
    def startTime(self):
        """Variable to store the start time of the mining process"""

        pass

    @abstractmethod
    def endTime(self):
        """Variable to store the end time of the complete program"""

        pass

    @abstractmethod
    def finalPatterns(self):
        """Variable to store the complete set of patterns in a dictionary"""

        pass

    @abstractmethod
    def oFile(self):
        """Variable to store the name of the output file to store the complete set of frequent patterns"""

        pass

    @abstractmethod
    def startMine(self):
        """Code for the mining process will start from this function"""

        pass

    @abstractmethod
    def getFrequentPatterns(self):
        """Complete set of frequent patterns generated will be retrieved from this function"""

        pass

    @abstractmethod
    def storePatternsInFile(self, oFile):
        """Complete set of frequent patterns will be saved in to an output file from this function

        :param oFile: Name of the output file
        :type oFile: file
        """

        pass

    @abstractmethod
    def getPatternsInDataFrame(self):
        """Complete set of frequent patterns will be loaded in to data frame from this function"""

        pass

    @abstractmethod
    def getMemory(self):
        """Total amount of memory consumed by the program will be retrieved from this function"""

        pass

    @abstractmethod
    def getRuntime(self):
        """Total amount of runtime taken by the program will be retrieved from this function"""

        pass
