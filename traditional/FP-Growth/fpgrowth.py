from abstract import *
import tree as T
        
        
class Fpgrowth(frequentPatterns):
    
    """
        Parameters
        ----------
        iFile : file
            Name of the Input file to mine complete set of frequent patterns
        oFile : file
            Name of the output file to store complete set of frequent patterns
        memoryUSS : float
            To store the total amount of USS memory consumed by the program
        memoryRSS : float
            To store the total amount of RSS memory consumed by the program
        startTime:float
            To record the start time of the mining process
        endTime:float
            To record the completion time of the mining process
        minSup : float
            The user given minSup
        Database : list
            To store the transactions of a database in list
        mapSupport : Dictionary
            To maintain the information of item and their frequency
        lno : int
            it represents the total no of transactions
        tree : class
            it represensts the Tree class
        itemsetCount : int
            it represenst the total no of patterns 
        finalPatterns : dict
            it represents to store the patterns
        itemsetBuffer : list
            it represenst the store the items in mining 
        maxPatternLength : int
           it represenst the constraint for pattern length

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
        check(line)
            To check the delimeter used in the user input fileTempBuffer,s,position,prefix,prefixLength
        creatingItemsets(fileName)
            Scans the dataset or dataframes and stores in list format
        frequentOneItem()
            Extracts the one-frequent patterns from transactions
        saveAllCombination(TempBuffer,s,position,prefix,prefixLength)
            Forms all the combinations between prefix and TempBuffer lists with support(s)
        saveItemset(pattern,support)
            Stores all the frequent patterns with their respective support
        fpGrowthGenerate(fptree,prefix,mapSupport)
            Mining the frequent patterns by forming conditional fptrees to particular prefix item.
            mapSupport represents the 1-length items with their respective support


        """

    startTime = float()
    endTime = float()
    minSup=float()
    finalPatterns = {}
    iFile = " "
    oFile = " "
    memoryUSS = float()
    memoryRSS = float()
    Database=[]
    mapSupport={}
    lno=0
    tree=T.Tree()
    itemsetBuffer=None
    fpNodeTempBuffer=[]
    itemsetCount=0
    maxPatternLength=1000
    
    def check(self, line):
        """Identifying the delimeter of the input file

            :param line: list of special charcters may be used by a user to seperate the items in a input file
            :type line: list of string
            :returns: Delimited string used in the input file to seperate each item
            :rtype: string
            """
        l = [',', '*', '&', ' ', '%', '$', '#', '@', '!', '    ', '*', '(', ')']
        j = None
        for i in l:
            if i in line:
                return i
        return j


    def creatingItemsets(self, iFileName):
        """Creating a Database from input file and updating the same to global variable finalPatterns

            :param iFileName: User given input file path with each row as a single transaction
            :type iFileName: str
            :param Global variable Database: list of items extracted from the input file .i.e, each row as a
                single list value
            :type Database: list
            """
        #import pandas as pd
        #global Database

        lno=0
        data=[]
        if isinstance(iFileName,list):
            self.Database=iFileName
        if isinstance(iFileName,pd.DataFrame):
             if iFileName.empty:
                 print("its empty..")
                 quit()
             i=iFileName.columns.values.tolist()
             if 'Transactions' in i:
                  self.Database=iFileName['Transactions'].tolist()
             if 'Patterns' in i:
                  self.Database=iFileName['Patterns'].tolist()

        if '.CSV' in iFileName:
            file1 = pd.read_csv(iFileName)
            columns = list(file1.head(0))
            if "Patterns" in columns:
                with open(iFileName, newline='') as csvfile:
                    data = csv.DictReader(csvfile)
                    for row in data:
                        l=row['Patterns']
                        l1=l.replace("[", "")
                        l2=l1.replace("]","")
                        li = list(l2.split(","))
                        li1=[int(i) for i in li]
                        self.Database.append(li1)
            if "Transactions" in columns:
                with open(iFileName, newline='') as csvfile:
                    data = csv.DictReader(csvfile)
                    for row in data:
                        l=row['Transactions']
                        l1=l.replace("[", "")
                        l2=l1.replace("]","")
                        li = list(l2.split(","))
                        li1=[int(i) for i in li]
                        self.Database.append(li1)
        else:
             try:
                 with open(iFileName,'r',encoding='utf-8') as f:
                    for line in f:
                        line.strip()
                        if lno==0:
                            lno+=1
                            delimeter=self.check(line)
                            #li=[lno]
                            li=line.split(delimeter)
                            if delimeter==',':
                                li1=[i.rstrip() for i in li]
                                self.Database.append([i.rstrip() for i in li])
                            else:
                                self.Database.append(li)
                            data.append([lno,li1])
                        else:
                            lno+=1
                            li=line.split(delimeter)
                            if delimeter==',':
                                li1=[i.rstrip() for i in li]
                                self.Database.append(li1)
                            else:
                                self.Database.append(li)
                   #print(Database)
             except IOError:
                  print("File Not Found")
                  quit()

        #else:
            #Database=iFileName['Transactions'].tolist()

    # function to get frequent one itemset
    def frequentOneItem(self):
        """Generating One frequent items sets

        :param minSup: User specified minimum support value as a thershold
        :type minSup: float
        :param Global variable finalPatterns: Dictionary with itemsets as keys with list of strings type and their support count as
            value
        :type finalPatterns: defaultdict
        """
    	# scans the database and finds single items whose support>=minSup 
        for i in self.Database:
            for j in i:
                if j not in self.mapSupport:
                    self.mapSupport[j]=1
                else:
                    self.mapSupport[j]+=1
    def saveItemset(self,prefix,prefixLength,support):
        """To save the frequent patterns mined form fptree

        :param prefix: the frequenct pattern
        :type prefix: list
        :param prefixLength : the length of a frequent pattern
        :type prefixLength : int
        :param support: the support of a pattern
        :type support :  int
        :The frequent patterns are update into global variable finalPatterns
        """
    	# this method taken pattern,patternLength to save itemset
        global patterns
        l=[]
        for i in range(prefixLength):
            l.append(prefix[i])
        self.itemsetCount+=1
        self.finalPatterns[tuple(l)]=support
    def saveAllCombinations(self,TempBuffer,s,position,prefix,prefixLength):
        """Generating all the combinations for items in single branch in fptree

        :param TempBuffer: items in a list
        :type TempBuffer: list
        :param s : support at leaf node of a branch
        :param position : the length of a TempBuffer
        :type position : int
        :param prefix : it represents the list of leaf node
        :type prefix : list
        :param prefixlength : the length of prefix
        :type prefixLength :int
        :type finalPatterns: defaultdict
        
        """
        max1=1<<position
        for i in range(1,max1):
            newprefixLength=prefixLength
            for j in range(position):
                isset=i&(1<<j)
                if isset>0: 
                    prefix.insert(newprefixLength,TempBuffer[j].itemid) 
                    newprefixLength+=1      
                    support=TempBuffer[j].counter
            self.saveItemset(prefix,newprefixLength,s)
            
    def fpGrowthGenerate(self,fptree,prefix,prefixLength,mapSupport):
        """Mining the fp tree

        :param tree: it represents the fptree
        :type tree: class Tree
        :param prefix : it represents a empty list and store the patterns that are mined
        :type prefix : list
        :param param prefixlength : the length of prefix
        :type prefixLength :int
        :param mapSupport : it represents the support of item
        :type mapsUpport : dictionary
        """
    	# this method is recursing mining of tree it takes tree,mapSupport is the details of support of items,
    	# prefix to store as a pattern,prefixLength is length of prefix
    	# we check no of children of a node.if it is single we identify all combinations ina branch items and save the patterns
    	# otherwise for every item in header list of tree we find prefixes of item and construct conditional tree to mine the patterns.
        singlePath=True
        position=0
        s=0
        if(len(fptree.root.child)>1):
            singlePath=False
        else:
            currentNode=fptree.root.child[0]
            while(True):
                if(len(currentNode.child)>1):
                    singlePath=False
                    break
                self.fpNodeTempBuffer.insert(position,currentNode)
                s=currentNode.counter
                position+=1
                if(len(currentNode.child)==0):
                    break
                currentNode=currentNode.child[0]
        if singlePath==True:
            self.saveAllCombinations(self.fpNodeTempBuffer,s,position,prefix,prefixLength)
        else:
            for i in reversed(fptree.headerList):
                item=i
                support=mapSupport[i]
                betaSupport=support
                prefix.insert(prefixLength,item)
                self.saveItemset(prefix,prefixLength+1,betaSupport)
                if(prefixLength+1<self.maxPatternLength):
                    prefixPaths=[]
                    path=fptree.mapItemNodes.get(item)
                    mapSupportBeta={}
                    while(path!=None):
                        if(path.parent.itemid!=-1):
                            prefixPath=[]
                            prefixPath.append(path)
                            pathCount=path.counter
                            parent1=path.parent
                            while(parent1.itemid!=-1):
                                prefixPath.append(parent1)
                                if(mapSupportBeta.get(parent1.itemid)==None):
                                    mapSupportBeta[parent1.itemid]=pathCount
                                else:
                                    mapSupportBeta[parent1.itemid]=mapSupportBeta[parent1.itemid]+pathCount
                                parent1=parent1.parent
                            prefixPaths.append(prefixPath)
                        path=path.nodeLink
                    treeBeta=T.Tree()
                    for i in prefixPaths:
                        treeBeta.addPrefixPath(i,mapSupportBeta,self.minSup)
                    if(len(treeBeta.root.child)>0):
                        treeBeta.createHeaderList(mapSupportBeta,self.minSup)
                        self.fpGrowthGenerate(treeBeta,prefix,prefixLength+1,mapSupportBeta)

    def startMine(self):
        """main program to start the operation

        :param minSup: user specified minimum support
        :type minSup: float
        """
    	#this method takes the minsup and returns the patterns
    	#firstly it scans the database and identifies the single-frequent items
    	#secondly it sorts the transactions with descending supports of items in transactions
    	#with sorted transactions we build tree and store the header list to tree with ascending order of 1-length frequent items.
    	# lastly we call fpgrowth method for mining the patterns from tree
        self.startTime = time.time()
        if self.iFile == None:
            raise Exception("Please enter the file path or file name:")
            quit()
        iFileName = self.iFile
        if self.minSup == None:
            raise Exception("Please enter the Minimum Support")
        #Database = []
        if self.minSup <= 0:
            raise Exception("Please enter the Minimum Support between (0,1) in percentage(%) calculated with database count")
            quit()

        self.creatingItemsets(iFileName)

        if self.minSup > len(self.Database):
            raise Exception("Please enter the minSup in range between 0 to 1")
            quit()
        self.frequentOneItem()
        self.minSup = (len(self.Database) * self.minSup)
        self.mapSupport={k: v for k, v in self.mapSupport.items() if  v>= self.minSup}
        mapsup=[k for k,v in sorted(self.mapSupport.items(),key=lambda x: x[1],reverse=True)]
        #print(self.minSup)
        for i in self.Database:
            transaction=[]
            for j in i:
                if j in mapsup:
                    transaction.append(j)
            transaction.sort(key=lambda val:self.mapSupport[val],reverse=True)
            self.tree.addTransaction(transaction)
        self.tree.createHeaderList(self.mapSupport,self.minSup)
        if(len(self.tree.headerList)>0):
            self.itemsetBuffer=[]
            self.fpGrowthGenerate(self.tree,self.itemsetBuffer,0,self.mapSupport)
        print("Frequent itemsets were generated successfully using FPGrowth algorithm")
        self.endTime = time.time()
        process = psutil.Process(os.getpid())
        self.memoryUSS = process.memory_full_info().uss
        self.memoryRSS = process.memory_info().rss
    
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
