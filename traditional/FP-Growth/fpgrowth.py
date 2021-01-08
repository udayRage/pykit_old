import time
from pathlib import Path
import sys
import csv
import numpy
import pandas as pd
from collections import defaultdict
from itertools import combinations as c
import os
import os.path
import psutil

start_time = float
end_time = float

#denoting a class for a node
class Node:
    def __init__(self):
        self.itemid=-1
        self.counter=1
        self.parent=None
        self.child=[]
        self.nodeLink=None
    def getChild(self,id1):
    	# denoting function to return the node with item name as input
        for i in self.child:
            if(i.itemid==id1):
                return i
        return None
class Tree:
    """
        A class used to represent the fpgrowth tree structure

        ...

        Attributes
        ----------
        child : list
            storing each child of a tree as a subtree
        data : list
            stroing the each itemset as single value of the list

        Methods
        -------
        createHeaderList(items,minSup)
            takes items only which are greater than minSup and sort the items in ascending order
        addTransaction(transaction)
            creating transaction as a branch in fptree
        fixNodeLinks(item,newNode)
            To create the link for nodes with same item
        printTree(Node)
            gives the details of node in fpgrowth tree
        addPrefixPath(prefix,mapSupport,minSup)
           It takes the items in prefix pattern whose support is >=minSup and construct a subtree
    """
    def __init__(self):
        """
        Parameters
        ----------
        headerList : list
            storing the list of items in tree sorted in ascending of their supports
        mapItemNodes : dictionary
            stroing the nodes with same item name
        mapItemLastNodes : dictionary
            representing the map that indicates the last node for each item
        root : Node
            representing the root Node in a tree
        """
        self.headerList=[]
        self.mapItemNodes={}
        self.mapItemLastNodes={}
        self.root=Node()

    def addTransaction(self,transaction):
        """adding transaction into tree

        :param transaction: it represents the one transactions in database
        :type(transaction): list
        """

    	# This method taken a transaction as input and returns the tree
        current=self.root
        for i in transaction:
            child=current.getChild(i)
            if(child==None):
                newNode=Node()
                newNode.itemid=i
                newNode.parent=current
                current.child.append(newNode)
                self.fixNodeLinks(i,newNode)
                current=newNode
            else:
                child.counter+=1
                current=child
    def fixNodeLinks(self,item,newNode):
        """Fixing node link for the newNode that inserted into fptree

        :param item: it represents the item of newNode
        :type item : int
        :param newNode : it represents the newNode that inserted in fptree
        :type newNode : Node
        
        """
        if item in self.mapItemLastNodes.keys():
            lastNode=self.mapItemLastNodes[item]
            lastNode.nodeLink=newNode
        self.mapItemLastNodes[item]=newNode
        if item not in self.mapItemNodes.keys():
            self.mapItemNodes[item]=newNode
            
    def printTree(self,root):
        """Print the details of Node in fptree
        
        :param root: it represents the Node in fptree
        :type root: Node
        
        This method is to find the details of parent,children,support of Node
        """

    	# this method is used print the details of tree
        if root.child==[]:
            return
        else:
            for i in root.child: 
                print(i.itemid,i.counter,i.parent.item)
                self.printTree(i)
    def update(self,header,u1):
        """To update the headerList 

        :param mapsup: it represents the header list
        :type mapsup: list
        :param u1: the list of items
        :type u1 : list
        """

        t1=[]
        for i in header:
            if i in u1:
                t1.append(i)
        return t1
    def createHeaderList(self,mapSupport,min_sup):
        """To create the headerList 

        :param mapSupport : it represents the items with their supports
        :type mapsup : dictionary
        :param min_sup : it represents the minSup
        :param min_sup : float
        """
    	#the fptree always maintains the header table to start the mining from leaf nodes
        t1=[]
        for x,y in mapSupport.items():
            if y>=min_sup:
                t1.append(x)
        mapsup=[k for k,v in sorted(mapSupport.items(),key=lambda x: x[1],reverse=True)]
        self.headerList=self.update(mapsup,t1)
    def addPrefixPath(self,prefix,mapSupportBeta,min_sup):
        """To construct the conditional tree with prefix paths of a node in fptree 

        :param prefix : it represents the prefix items of a Node
        :type prefix : list
        :param mapSupportBeta : it represents the items with their supports
        :param mapSupportBeta : dictionary
        :param min_sup : to check the item meets with minSup
        :param min_sup : float
        """
    	#this method is used to add prefix paths in conditional trees of fptree
        pathCount=prefix[0].counter
        current=self.root
        prefix.reverse()
        for i  in range(0,len(prefix)-1):
            pathItem=prefix[i]
            #pathCount=mapSupportBeta.get(pathItem.itemid)
            if(mapSupportBeta.get(pathItem.itemid)>=min_sup):
                child=current.getChild(pathItem.itemid)
                if(child==None):
                    newNode=Node()
                    newNode.itemid=pathItem.itemid
                    newNode.parent=current
                    newNode.counter=pathCount
                    current.child.append(newNode)
                    current=newNode
                    self.fixNodeLinks(pathItem.itemid,newNode)
                else:
                    child.counter+=pathCount
                    current=child
        
        
        
class Fpgrowth():
    
    def __init__(self,data,minSup):
        """
        Parameters
        ----------
        data : file
            The user given database file
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
        final_frequent_items : int
            it represents to store the patterns
        itemsetBuffer : list
            it represenst the store the items in mining 
        maxPatternLength : int
           it represenst the constraint for pattern length
        """
        self.minSup=minSup
        self.data=data
        self.Database=[]
        self.mapSupport={}
        self.lno=0
        self.tree=Tree()
        self.itemsetBuffer=None
        self.fpNodeTempBuffer=[]
        self.itemsetCount=0
        self.maxPatternLength=1000
        self.final_frequent_itemsets={}
    def Check(self, line):
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


    def creating_itemsets(self, iFileName):
        """Creating a Database from input file and updating the same to global variable final_frequent_itemsets

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
                            delimeter=self.Check(line)
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
    def frequent_one_item(self):
        """Generating One frequent items sets

        :param minSup: User specified minimum support value as a thershold
        :type minSup: float
        :param Global variable final_frequent_itemsets: Dictionary with itemsets as keys with list of strings type and their support count as
            value
        :type final_frequent_itemsets: defaultdict
        """
    	# scans the database and finds single items whose support>=minSup 
        self.mapSupport={}
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
        :The frequent patterns are update into global variable final_frequent_itemsets
        """
    	# this method taken pattern,patternLength to save itemset
        global patterns
        l=[]
        for i in range(prefixLength):
            l.append(prefix[i])
        self.itemsetCount+=1
        self.final_frequent_itemsets[tuple(l)]=support
    def saveAllcombinations(self,TempBuffer,s,position,prefix,prefixLength):
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
        :type final_frequent_itemsets: defaultdict
        
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
            
    def fpgrowth_generate(self,tree,prefix,prefixLength,mapSupport):
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
        if(len(tree.root.child)>1):
            singlePath=False
        else:
            currentNode=tree.root.child[0]
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
            self.saveAllcombinations(self.fpNodeTempBuffer,s,position,prefix,prefixLength)
        else:
            for i in reversed(tree.headerList):
                item=i
                support=mapSupport[i]
                betaSupport=support
                prefix.insert(prefixLength,item)
                self.saveItemset(prefix,prefixLength+1,support)
                if(prefixLength+1<self.maxPatternLength):
                    prefixPaths=[]
                    path=tree.mapItemNodes.get(item)
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
                    treeBeta=Tree()
                    for i in prefixPaths:
                        treeBeta.addPrefixPath(i,mapSupportBeta,self.minSup)
                    if(len(treeBeta.root.child)>0):
                        treeBeta.createHeaderList(mapSupportBeta,self.minSup)
                        self.fpgrowth_generate(treeBeta,prefix,prefixLength+1,mapSupportBeta) 
    def updateTransaction(self,mapsup,transaction):
        """To update the list

        :param mapsup: it represents the header list
        :type mapsup: list
        :param transaction: the list of items
        :type transaction : list
        """
        t1=[]
        for i in mapsup:
            if i in transaction:
                t1.append(i)
        return t1
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
        global Database,memory,totalTime,patterns,start_time,end_time
        start_time = time.time()
        if self.data == None:
            raise Exception("Please enter the file path or file name:")
            quit()
        iFileName = self.data
        if self.minSup == None:
            raise Exception("Please enter the Minimum Support")
        #Database = []
        if self.minSup <= 0:
            raise Exception("Please enter the Minimum Support between (0,1) in percentage(%) calculated with database count")
            quit()

        self.creating_itemsets(iFileName)

        if self.minSup > len(self.Database):
            raise Exception("Please enter the minSup in range between 0 to 1")
            quit()
        self.frequent_one_item()
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
        #self.tree.printTree(self.tree.root)
        if(len(self.tree.headerList)>0):
            self.itemsetBuffer=[]
            self.fpgrowth_generate(self.tree,self.itemsetBuffer,0,self.mapSupport)
        print("Frequent itemsets were generated successfully using FPGrowth algorithm")
        end_time = time.time()
    def getMemory(self):
        """Calculating the amount of memory consumed by the Apriori algorithm

        """
        #import psutil
        #global minSup
        process = psutil.Process(os.getpid())
        memory = process.memory_full_info().uss  # process.memory_info().rss
        memory_in_MB = memory / (1024 * 1024)
        return memory_in_MB
        #print(memory_in_MB)  # in bytes
        #print("Total Memory is:", memory_in_MB)


    def getRuntime(self):
        """Calculating the total amount of execution time taken by the Apriori algorithm

        """
        global end_time, start_time
        return (end_time - start_time)




    def getPatternInDf(self):
        """Storing final frequent itemsets in a dataframe and converting it to .csv file

        :param global patterns: Dictionary with itemsets as keys with list of strings type and
                their support count as a value
        :type patterns: dict
        """
        #import pandas as pd
        #global final_frequent_itemsets
        df = {}
        #for x,y in self.final_frequent_itemsets.items():
        data=[]
        for a,b in self.final_frequent_itemsets.items():
            data.append([a,b])
           #print(x)
           #s = "output" + str(x)+".CSV"
            df = pd.DataFrame(data, columns=['Patterns','Support'])
        #print("Total frequent itemsets are:", len(df))
        return df




    def getPatternsInFile(self, outputfile):
        """Main apriori function receiving input file path, list of minimum support values, nodes, and nonleaf

        :param data: .csv input file path
        :type data: path
        :param listing: list of integers with minimum support
        :type listing: list
        :param nodes: Number of children of the hash tree
        :type nodes: int
        :param nonleaf: Maximum number of elements allowed in a non leaf node
        :type nonleaf: int
        """

        #data = Path(sys.argv[1])
        #global final_frequent_itemsets
        writer = open(outputfile, 'w+')
        for x, y in self.final_frequent_itemsets.items():
            #s = "output" + str(x)
            s1 = str(x) + ":" + str(y)
            writer.write("%s \n" % s1)
        #InFile()

    def getFPs(self):
        """Returing final frequent itemsets in a Dictionary

        Returns
        -------
        defaultdict

        """
        return self.final_frequent_itemsets

    def getStatsInFile(self,statsfile):
        """ Printing the statistics of the database into a Statistics file
        :param global Database variable: Storing the data in to a Database variable
        :type Database: defaultdict
        """
        #global Database
        sum1 = 0
        min1 = 999999
        max1 = -1
        tot = 0
        si = []
        l1 = 0
        s = statsfile
        writer1 = open(s, 'w+')
        for line in self.Database:
            l = line
            for i in l:
                if i not in si:
                    si.append(i)
            if (len(l) > max1):
                max1 = len(l)
            sum1 += len(l)
            if (len(l) < min1):
                min1 = len(l)
            tot += len(l)
        s = "Total number of transactions:" + str(len(self.Database))
        writer1.write("%s \n" % s)
        s = "Total number of items:" + str(len(si))
        writer1.write("%s \n" % s)
        s = "Minimum length of a transaction: " + str(min1)
        writer1.write("%s \n" % s)
        s = "Maximum length of a transaction: " + str(max1)
        writer1.write("%s \n" % s)
        s = "Avg length of a transaction: " + str(tot / len(self.Database))
        writer1.write("%s \n" % s)
