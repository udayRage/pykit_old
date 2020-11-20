import time
#from pathlib import Path
#import sys
import csv
#import numpy
import pandas as pd
#from mlxtend.preprocessing import TransactionEncoder
from collections import defaultdict
#from multipledispatch import dispatch
from itertools import combinations as c
import os
import os.path
import psutil

# from collections import OrderedDict
start_time = time.time()
#itemset = set()
Database = []
items = defaultdict()
final_frequent_itemsets = defaultdict()
memory={}
totalTime={}
patterns={}
# from collections import defaultdict

items_sets = defaultdict()

# Input for Hash mod function f(x) mod No_of_children
No_of_children = 1000  # int(input('No of children:'))

# Input for splitting any Non Leaf node in after reaching maximum no of records in that tree
Max_Records_Nonleaf = 50  # int(input('Maximum number of records in Non Leaf Node:'))
writer=None

class Tree(object):
    """
        A class used to represent the hashtree structure

        ...

        Attributes
        ----------
        child : list
            storing each child of a tree as a subtree
        data : list
            stroing the each itemset as single value of the list
        leaf : bool
            representing leaf node of the hash tree, so that further exapnsion will be possible from that child
        level : int
            representing the level of the tree to identify the depth of the tree

        Methods
        -------
        createChildren(NoOfChild)
            creating children to hash tree
        setChildrenValue(data_list)
            Attach the list of data values into the children of the tree
        splitting(level)
            No of elements in a particular tree is crosses the user specified limit splitting
            is performed based on level attribute
        insertion(data, level)
            Inserting data into a particular node in a particular level of the hash tree
        first_element(self, data)
            Inserting the first element into the hash tree
        Tree_display(parent, length)
            Displaying the content of the tree based on the total number of elements and parent node
        Tree_search(self, element)
            Searching a particular element in a hash tree
    """

    def __init__(self):
        """
        Parameters
        ----------
        child : list
            storing each child of a tree as a subtree
        data : list
            stroing the each itemset as single value of the list
        leaf : bool
            representing leaf node of the hash tree, so that further exapnsion will be possible from that child
        level : int
            representing the level of the tree to identify the depth of the tree
        """
        self.child = []
        self.data = []
        self.leaf = True
        self.level = 0

    # Creating the children of a particular node

    def createChildren(self, NoOfChild):
        """Creating children to the hash tree total of NoOfChild

        :param NoOfChild: it represents the total number of children to the hash tree at each level
        :type NoOfChild: int
        """

        self.leaf = False
        for i in range(0, NoOfChild):
            self.child.append(Tree())

    # Adding values to the tree node

    def setChildrenValue(self, data_list):
        """ Attach the list of data values into the children of the tree

        :param data_list: itemset in a list format
        :type data_list: list
        :return: returns the number of data elements in a child node of a hash tree as a rowcount
        :rtype: int
        """
        self.data.append(data_list)
        rows = len(self.data)
        return rows

    # Printing the element of a particular node
    # def printdata(self):
    #   if self.data == []:
    #        print("No Element is inserted")
    #    else:
    #        print(self.data)

    # splitting a node and adding the data elements to the particular child and making node data as null
    def splitting(self, level,k=None):
        """No of elements in a particular tree is crosses the user specified limit splitting
            is performed based on level attribute

        :param level: level of the hash tree to identify the depth of the tree
        :type level: int
        """

        self.level = level

        self.createChildren(No_of_children)
        for i in range(len(self.data)):
            indexing = self.data[i][level] % No_of_children
            self.child[indexing].setChildrenValue(self.data[i])
        self.data = []
        # self.level += 1
        # print(self.level)

    # Inserting the data into tree other than root node

    def insertion(self, data, level):
        """Inserting data into a particular node in a particular level of the hash tree

        :param data: list of itemsets to be inserted into the hash tree
        :type data: list
        :param level: level of the hash tree to identify the depth of the tree
        :type level: int
        """

        self.level = level
        # print(self.level)
        data_length = len(data)
        indexing = int(data[level]) % No_of_children
        if self.child[indexing].leaf is True:
            No_rows = self.child[indexing].setChildrenValue(data)
            if No_rows > Max_Records_Nonleaf:
                level += 1
                if level < data_length:
                    self.child[indexing].splitting(level, data_length)
                # else:
                #   pass
                # print("We have reached the maximum level and There is will be No splitting")
        else:
            level += 1
            self.child[indexing].insertion(data, level)

    # Inserting the data into the tree starting with root node
    def first_element(self, data):
        """Inserting the first element into the hash tree

        :param data: list of itemsets to be inserted into the hash tree
        :type data: list
        """

        level = 0
        # data_length = len(data)
        # print(self.level)
        if not self.child:
            First = int(data[level]) % No_of_children

            self.createChildren(No_of_children)

            self.child[First].data.append(data)  # setChildrenValue(data)
        else:
            self.insertion(data, level)

    # Displaying the content of the complete tree from left to right (Child  0 to Child length )
    def Tree_display(self, parent, length):
        """Displaying the content of the hash tree

        :param parent: Object reference of the parent node of the current node
        :param length: Reresenting the depth of the hash tree
        :type length: int
        :return: returning zero after displaying all the elements of the hash tree
        """

        if self.leaf is False:
            for i in range(length):
                parent = self
                self.child[i].Tree_display(parent, length)

        else:
            if not self.data:
                return 0
            else:
                print(self.data)
                print(parent.level)

    def Tree_search(self, element):
        """Searching a particular element in a hash tree and if it is identified we ll increment the count
            that element by 1 other returning the cursor to called function without any modification

        :param element: list of itemset to be searched in the hash tree
        :type element: list
        :return: returning non zero value to the called function after seraching the particular element
        """

        if self.leaf is False:
            indexing111 = element[self.level] % No_of_children
            # print(indexing111) # for displaying the path of the element evaluation
            self.child[indexing111].Tree_search(element)
        else:
            if not self.data:
                return
            else:
                for i in range(len(self.data)):
                    ind = str(element)
                    # comp = str(self.data[i])
                    if element == self.data[i]:  # ind == comp:
                        # print(type(element),"element type and element is:", element)

                        if items_sets.get(ind) is None:
                            items_sets[ind] = 1
                            return
                        else:
                            items_sets[ind] = items_sets.get(ind) + 1
                            # print(self.data[i], "Success")
                            return


root = Tree()

'''list_of_files = []
i=0
for filename in glob.iglob('*.csv'):
    list_of_files.append(filename)
    print("Index",i," and File Name:",filename)
    i+=1
print(list_of_files)
Index = int(input("Enter the Index to choose the file:"))
print(list_of_files[Index])
iFileName= list_of_files[Index]'''

'''def creating_itemsets():
    global Database
    with open(iFileName, 'r', encoding='utf-8') as f:
        file = f.readlines()
        i=0
        for line in file:
            line = line.strip()
            line = line.split(',')
            print(line)
            Database.append(line)
            #print(Database)
            #itemset = itemset.union(set(Database[i]))
            #i = i + 1
            #print(i)'''

l = [',', '*', '&', ' ', '%', '$', '#', '@', '!', '    ', '*', '(', ')']


def Check(line):
    """Identifying the delimeter of the input file

        :param line: list of special charcters may be used by a user to seperate the items in a input file
        :type line: list of string
        :returns: Delimited string used in the input file to seperate each item
        :rtype: string
        """

    j = None
    for i in l:
        if i in line:
            return i
    return j


def creating_itemsets(iFileName):
    """Creating a Database from input file and updating the same to global variable final_frequent_itemsets

        :param iFileName: User given input file path with each row as a single transaction
        :type iFileName: str
        :param Global variable Database: list of items extracted from the input file .i.e, each row as a
            single list value
        :type Database: list
        """

    global Database
    lno=0
    data=[]
    if isinstance(iFileName,list):
        database=iFileName
    if isinstance(iFileName,pd.DataFrame):
         if iFileName.empty:
             print("its empty..")
             quit()
         i=iFileName.columns.values.tolist()
         if 'Transactions' in i:
              Database=iFileName['Transactions'].tolist()
         if 'Patterns' in i:
              Database=iFileName['Patterns'].tolist()

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
                    Database.append(li1)
        if "Transactions" in columns:
            with open(iFileName, newline='') as csvfile:
                data = csv.DictReader(csvfile)
                for row in data:
                    l=row['Transactions']
                    l1=l.replace("[", "")
                    l2=l1.replace("]","")
                    li = list(l2.split(","))
                    li1=[int(i) for i in li]
                    Database.append(li1)
    else:
         try:
             with open(iFileName,'r',encoding='utf-8') as f:
                for line in f:
                    line.strip()
                    if lno==0:
                        lno+=1
                        delimeter=Check(line)
                        #li=[lno]
                        li=line.split(delimeter)
                        if delimeter==',':
                            li1=[i.rstrip() for i in li]
                            Database.append([i.rstrip() for i in li])
                        else:
                            Database.append(li)
                        data.append([lno,li1])
                    else:
                        lno+=1
                        li=line.split(delimeter)
                        if delimeter==',':
                            li1=[i.rstrip() for i in li]
                            Database.append(li1)
                        else:
                            Database.append(li)
               #print(Database)
         except IOError:
              print("File Not Found")
              quit()

    #else:
        #Database=iFileName['Transactions'].tolist()

# function to get frequent one itemset
def frequent_one_item(minSup):
    """Generating One frequent items sets and updating the same to global variable final_frequent_itemsets

    :param minSup: User specified minimum support value as a thershold
    :type minSup: float
    :param Global variable final_frequent_itemsets: Dictionary with itemsets as keys with list of strings type and their support count as
        value
    :type final_frequent_itemsets: defaultdict
    """

    candidate = {}
    global final_frequent_itemsets
    for i in range(len(Database)):
        for j in range(len(Database[i])):
            if Database[i][j] not in candidate:
                candidate[Database[i][j]] = 1
            else:
                candidate[Database[i][j]] += 1
    final_frequent_itemsets = {keys: value for keys, value in candidate.items() if value >= minSup}


# def less_items():
#    pass

def dict_keys_to_int_elements(a):
    """Converting dictionary keys to interger elements

    :param a: Dictionary with itemsets as keys with list of strings type and their support count as
        value
    :type a: dict
    :returns: a list of integer itemsets to represent dictionary keys
    :rtype: list
    """

    temp = []
    for ite in a.keys():
        ite = [int(i) for i in ite.strip('[]').split(',')]
        temp.append(ite)
        # print(sorted(temp))
    return sorted(temp)


def subset_creation(transaction, length_subset):
    """Generating combination of itemsets

        :param transaction: Total list of transactions of the database, each with items
        :type transaction: list
        :param length_subset: No of elements in the combination of items
        :type length_subset: int
        :returns: list of combinations of items each with of length equals to length_subset
        :rtype: list
        """

    # print(type(transaction))
    subset = list(c(transaction, length_subset))
    temp = []
    for i in range(len(subset)):
        # ite = [int(j) for j in subset[i]]
        # temp.append(ite)
        final_list = sorted(list(subset[i]))
        # print(type(subset[i]))
        temp.append(final_list)
    return sorted(temp)


def apriori_generate(listofitemsets, k):
    """Apriori Generation function along with item pruning of redundant items

        :param listofitemsets: list of k-1 length itemsets for generating k length length itemsets
        :type listofitemsets: list
        :param k: length of the next itemsets
        :type k: int
        :returns: list of final candidate itemsets of length k after pruning k-1 length itemsets
        :rtype: list
        """

    ck = []
    # join step
    lenlk = len(listofitemsets)
    for i in range(lenlk):
        for j in range(i + 1, lenlk):
            L1 = list(listofitemsets[i])[:k - 2]
            L2 = list(listofitemsets[j])[:k - 2]
            if L1 == L2:
                ck.append(sorted(list(set(listofitemsets[i]) | set(listofitemsets[j]))))
    # print(ck)
    # prune step
    final_ck = []
    for candidate in ck:
        all_subsets = subset_creation(candidate, k - 1)
        found = True
        for i in range(len(all_subsets)):
            value = list(sorted(all_subsets[i]))
            if value not in listofitemsets:
                found = False
                break
        if found == True:
            final_ck.append(candidate)

    # print(final_ck)

    return sorted(final_ck)


def main(minSup):
    """main program to start the operation

    :param minSup: user specified minimum support
    :type minSup: float
    """

    # creating_itemsets()
    # print("Total Items are:", len(itemset))
    # itemset = sorted(itemset)
    global items_sets,writer,memory,time,patterns
    #print(len(Database))
    # minSup= float(input("enter the minimum support:"))
    #print(len(Database),minSup)
    minSup = (len(Database) * minSup)
    if minSup>len(Database):
        raise Exception("Please enter the minSup in range between 0 to 1")
        quit()
    #print(minSup)
    frequent_one_item(minSup)
    # Sorting one frequent item sets
    frequent_one = sorted([int(i) for i in final_frequent_itemsets.keys()])
    # frequent_one=[k for k,v in sorted(final_frequent_itemsets.items(),key=lambda x:x)]
    #
    #print(frequent_one)
    #print("1 frequent itemsets:",len(frequent_one))

    iteration = True
    list_for_next_iteration = []
    iter = 2
    while iteration:
        #print("hello")
        if iter == 2:
            # Generation of candiate two item sets and adding the same to Hash tree
            comb = subset_creation(frequent_one, 2)  # list(c(frequent_one, 2))
            #print(comb)
        else:
            comb = apriori_generate(list_for_next_iteration, iter)
            #print("comb")
        if len(comb) == 1:
            #print(comb, type(comb))
            #print(set(comb[0]))
            count = 0
            for i in range(len(Database)):
                row_of_Database = set(int(t) for t in Database[i])
                if set(comb[0]).issubset(row_of_Database):
                    count += 1
            if count >= minSup:
                final_frequent_itemsets[str(comb)] = count
            break
        if comb == []:
            break
        maintain = Tree()
        # Inserting Candidate itemsets into hash tree
        for i in range(len(comb)):
            test = comb[i]  # sorted([int(t) for t in comb[i]])
            maintain.first_element(test)
        for i in range(len(Database)):
            row_of_Database = [int(t) for t in Database[i]]
            subse = subset_creation(row_of_Database, iter)
            for j in range(len(subse)):
                maintain.Tree_search(subse[j])

        items_after_support = {keys: value for keys, value in items_sets.items() if value >= minSup}
        #print(iter, "frequent itemsets :", len(items_after_support))
        if items_after_support is None:
            iteration = False
            break
        final_frequent_itemsets.update(items_after_support)
        #print("Total frequent itemsets are:", len(final_frequent_itemsets))
        if len(items_after_support) == 0 or len(items_after_support) == 1:
            #print("Total frequent itemsets are:", len(final_frequent_itemsets))
            break
        list_for_next_iteration = dict_keys_to_int_elements(items_after_support)

        items_after_support = {}
        items_sets = {}

        iter += 1

    #memory = process.memory_info().rss
    #memory_in_MB = memory / (1024 * 1024)
    #storePatternsInFile()
    #storePatternsInDf()
    m=Memory()
    memory[minSup]=m
    t=RunTime()
    totalTime[minSup]=t
    patterns[minSup]=final_frequent_itemsets
    print("Total frequent itemsets are:", len(final_frequent_itemsets))

    '''storePatternsInFile(final_frequent_itemsets,writer)
    storepatternsInDf(final_frequent_itemsets)
    getMemory()
    getRunTime()'''
    '''for x, y in final_frequent_itemsets.items():
        s = str(x) + ":" + str(y)
        writer.write("%s \n" % s)
    print("Memory Space:", memory_in_MB)  # in bytes
    print("Total Patterns:", len(final_frequent_itemsets))
    print("Total Execution Time is:", time.time() - start_time)'''

def getMemory():
    """Printing the amount memory taken for each minimum support to the console
    """
    global memory
    print("Memory Details:")
    for x,y in memory.items():
        print(x,":",y)

def Memory():
    """Calculating the amount of memory consumed by the Apriori algorithm

    """

    process = psutil.Process(os.getpid())
    memory = process.memory_full_info().uss  # process.memory_info().rss
    memory_in_MB = memory / (1024 * 1024)
    #print(memory_in_MB)  # in bytes
    return memory_in_MB
def getRunTime():
    """ Printing the amount runtime taken for each minimum support to the console
    """
    global totalTime
    print("Execution Time:")
    for x,y in totalTime.items():
        print(x,":",y)

def RunTime():
    """Calculating the total amount of execution time taken by the Apriori algorithm

    """
    return(time.time() - start_time)



def InFile():
    """Storing final frequent patterns in a file

    :param global patterns: Dictionary with itemsets as keys with list of strings type and
            their support count as a value
    :type patterns: dict
    """
    global patterns
    #print("Total frequent itemsets are:", patterns)
    for x,y in patterns.items():
        s = "output" + str(x)
        writer = open(s, 'w+')
        for a,b in y.items():
            s1=str(a)+":"+str(b)
            writer.write("%s \n" %s1)
    '''#data = []
    global final_frequent_itemsets,writer
    #print(writer)
    print("hello")
    for x,y in final_frequent_itemsets.items():
        s=str(x)+":"+str(y)
        writer.write("%s \n" %s)'''
def InDf():
    """Storing final frequent itemsets in a dataframe and converting it to .csv file

    :param global patterns: Dictionary with itemsets as keys with list of strings type and
            their support count as a value
    :type patterns: dict
    """
    global patterns
    df = {}
    for x,y in patterns.items():
       data=[]
       for a,b in y.items():
           data.append([a,b])
       #print(x)
       s = "output" + str(x)+".CSV"
       df = pd.DataFrame(data, columns=['Patterns','Support'])
    #print("Total frequent itemsets are:", len(df))
    return df
       #df.to_csv(s,columns=['Patterns','Support'],index=False)




def storePatternsInFile(data, listing=[0.01,0.02,0.03,0.04],nodes=1000,nonleaf=50):
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
    global No_of_children,Max_Records_Nonleaf,Database
    if data==None:
        raise Exception("Please enter the file path or file name:")
        quit()
    if nodes!=None:
        No_of_children=nodes
    if nonleaf!=None:
         Max_Records_Nonleaf=nonleaf
    iFileName = data
    if listing==None:
        raise Exception("Please enter the Minimum Support")
    Database=[]
    creating_itemsets(iFileName)
    #print(Database)
    if type(listing)==list:
        l1 = len(listing)
        if l1<=0:
             raise Exception("Please enter the Minimum Support.")
             quit()
        '''else:
            for i in listing:
                if i<=0 or i>1:
                    raise Exception("Please enter the Minimum Support between(0,1) in percentage(%) calculated with database count")
                    quit()'''
        p = 0
        while (p < l1):
            i = float(listing[p])
            main(i)
            p += 1
    else:
        if listing==0:
            raise Exception("Please enter the Minimum Support between (0,1) in percentage(%) calculated with database count")
        main(listing)
    InFile()

def getPatternsInDf(data, listing=[0.01,0.02,0.03,0.04],nodes=1000,nonleaf=50):
    """Main apriori function receiving input file path and list of minimum support values

    :param data: .csv input file path
    :type data: path
    :param listing: list of integers with minimum support
    :type listing: list
    :param nodes: Number of children of the hash tree
    :type nodes: int
    :param nonleaf: Maximum number of elements allowed in a non leaf node
    :type nonleaf: int
    :return: returing frequent patterns in a data frame
    :rtype: Dataframe
    """

    #data = Path(sys.argv[1])
    global No_of_children,Max_Records_Nonleaf,Database
    if data==None:
        raise Exception("Please enter the file path or file name:")
        quit()
    if nodes!=None:
        No_of_children=nodes
    if nonleaf!=None:
         Max_Records_Nonleaf=nonleaf
    iFileName = data
    if listing==None:
        raise Exception("Please enter the Minimum Support")
    Database=[]
    creating_itemsets(iFileName)
    #print(Database)
    if type(listing)==list:
        l1 = len(listing)
        if l1<=0:
             raise Exception("Please enter the Minimum Support.")
             quit()
        '''else:
            for i in listing:
                if i<=0 or i>1:
                    raise Exception("Please enter the Minimum Support between(0,1) in percentage(%) calculated with database count")
                    quit()'''
        p = 0
        while (p < l1):
            i = float(listing[p])
            main(i)
            p += 1
    else:
        if listing==0:
            raise Exception("Please enter the Minimum Support between (0,1) in percentage(%) calculated with database count")
        main(listing)
    return InDf()

def getStatsInFile():
    """ Printing the statistics of the database into a Statistics file
    :param global Database variable: Storing the data in to a Database variable
    :type Database: defaultdict
    """
    global Database
    sum1 = 0
    min1 = 999999
    max1 = -1
    tot = 0
    si = []
    l1 = 0
    s = "Statistics"
    writer1 = open(s, 'w+')
    for line in Database:
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
    s = "Total number of transactions:" + str(len(Database))
    writer1.write("%s \n" % s)
    s = "Total number of items:" + str(len(si))
    writer1.write("%s \n" % s)
    s = "Minimum length of a transaction: " + str(min1)
    writer1.write("%s \n" % s)
    s = "Maximum length of a transaction: " + str(max1)
    writer1.write("%s \n" % s)
    s = "Avg length of a transaction: " + str(tot / len(Database))
    writer1.write("%s \n" % s)
