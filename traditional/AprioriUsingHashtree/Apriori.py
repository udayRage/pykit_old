import time
import csv
import pandas as pd
from collections import defaultdict
from itertools import combinations as c
import os
import os.path
import psutil

startTime = float
endTime = float
itemSets = defaultdict()

# Input for Hash mod function f(x) mod No_of_children
noOfChildren = 1000  # int(input('No of children:'))

# Input for splitting any Non Leaf node in after reaching maximum no of records in that tree
maxRecordsInNonLeaf = 50  # int(input('Maximum number of records in Non Leaf Node:'))


class Tree(object):
    """
        We will use this class to represent the Hash tree structure

        ...

        Attributes
        ----------
        child : list
            storing each child of a tree as a subtree
        data : list
            storing the each item set as single value of the list
        leaf : bool
            representing leaf node of the hash tree, so that further expansion will be possible from that child
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

        :param data_list: item set in a list format
        :type data_list: list
        :return: returns the number of data elements in a child node of a hash tree as a rowcount
        :rtype: int
        """
        self.data.append(data_list)
        rows = len(self.data)
        return rows

    # Printing the element of a particular node
    # def print data(self):
    #   if self.data == []:
    #        print("No Element is inserted")
    #    else:
    #        print(self.data)

    # splitting a node and adding the data elements to the particular child and making node data as null
    def splitting(self, level):
        """No of elements in a particular tree is crosses the user specified limit splitting
            is performed based on level attribute

        :param level: level of the hash tree to identify the depth of the tree
        :type level: int
        
        """

        self.level = level

        self.createChildren(noOfChildren)
        for i in range(len(self.data)):
            indexing = self.data[i][level] % noOfChildren
            self.child[indexing].setChildrenValue(self.data[i])
        self.data = []
        # self.level += 1
        # print(self.level)

    # Inserting the data into tree other than root node

    def insertion(self, data, level):
        """Inserting data into a particular node in a particular level of the hash tree

        :param data: list of item sets to be inserted into the hash tree
        :type data: list
        :param level: level of the hash tree to identify the depth of the tree
        :type level: int
        """

        self.level = level
        # print(self.level)
        data_length = len(data)
        indexing = int(data[level]) % noOfChildren
        if self.child[indexing].leaf is True:
            noOfRows = self.child[indexing].setChildrenValue(data)
            if noOfRows > maxRecordsInNonLeaf:
                level += 1
                if level < data_length:
                    self.child[indexing].splitting(level)  # data_length as a parameter
                # else:
                #   pass
                # print("We have reached the maximum level and There is will be No splitting")
        else:
            level += 1
            self.child[indexing].insertion(data, level)

    # Inserting the data into the tree starting with root node
    def first_element(self, data):
        """Inserting the first element into the hash tree

        :param data: list of item sets to be inserted into the hash tree
        :type data: list
        """

        level = 0
        # data_length = len(data)
        # print(self.level)
        if not self.child:
            First = int(data[level]) % noOfChildren

            self.createChildren(noOfChildren)

            self.child[First].data.append(data)  # setChildrenValue(data)
        else:
            self.insertion(data, level)

    # Displaying the content of the complete tree from left to right (Child  0 to Child length )
    def Tree_display(self, parent, length):
        """Displaying the content of the hash tree

        :param parent: Object reference of the parent node of the current node
        :param length: Representing the depth of the hash tree
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

        :param element: list of item set to be searched in the hash tree
        :type element: list
        :return: returning non zero value to the called function after searching the particular element
        """

        if self.leaf is False:
            indexing111 = element[self.level] % noOfChildren
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

                        if itemSets.get(ind) is None:
                            itemSets[ind] = 1
                            return
                        else:
                            itemSets[ind] = itemSets.get(ind) + 1
                            # print(self.data[i], "Success")
                            return


class Apriori:
    """

    """

    def __init__(self, data, minSup, nodes=1000, nonLeaf=50):
        self.data = data
        self.minSup = minSup
        self.nodes = nodes
        self.nonLeaf = nonLeaf
        self.finalFps = defaultdict()
        self.Database = []

    def Check(self, line):
        """Identifying the delimiter of the input file

            :param line: list of special characters may be used by a user to separate the items in a input file
            :type line: list of string
            :returns: Delimited string used in the input file to separate each item
            :rtype: string
            """
        l = [',', '*', '&', ' ', '%', '$', '#', '@', '!', '    ', '*', '(', ')']
        j = None
        for i in l:
            if i in line:
                return i
        return j

    def creatingItemsets(self, iFileName):
        """Creating a Database from input file and updating the same to global variable finalFps

            :param iFileName: User given input file path with each row as a single transaction
            :type iFileName: str
            """
        # import pandas as pd
        # global Database

        lno = 0
        data = []
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
                with open(iFileName, newline='') as csvfile:
                    data = csv.DictReader(csvfile)
                    for row in data:
                        l = row['Patterns']
                        l1 = l.replace("[", "")
                        l2 = l1.replace("]", "")
                        li = list(l2.split(","))
                        li1 = [int(i) for i in li]
                        self.Database.append(li1)
            if "Transactions" in columns:
                with open(iFileName, newline='') as csvfile:
                    data = csv.DictReader(csvfile)
                    for row in data:
                        l = row['Transactions']
                        l1 = l.replace("[", "")
                        l2 = l1.replace("]", "")
                        li = list(l2.split(","))
                        li1 = [int(i) for i in li]
                        self.Database.append(li1)
        else:
            try:
                with open(iFileName, 'r', encoding='utf-8') as f:
                    for line in f:
                        line.strip()
                        if lno == 0:
                            lno += 1
                            delimiter = self.Check([line])
                            # li=[lno]
                            li = line.split(delimiter)
                            if delimiter == ',':
                                li1 = [i.rstrip() for i in li]
                                self.Database.append([i.rstrip() for i in li])
                            else:
                                self.Database.append(li)
                            data.append([lno, li1])
                        else:
                            lno += 1
                            li = line.split(delimiter)
                            if delimiter == ',':
                                li1 = [i.rstrip() for i in li]
                                self.Database.append(li1)
                            else:
                                self.Database.append(li)
                # print(Database)
            except IOError:
                print("File Not Found")
                quit()

        # else:
        # Database=iFileName['Transactions'].tolist()

    # function to get frequent one item set
    def frequent_one_item(self):
        """Generating One frequent items sets and updating the same to global variable finalFps

        """

        candidate = {}
        # global finalFps
        for i in range(len(self.Database)):
            for j in range(len(self.Database[i])):
                if self.Database[i][j] not in candidate:
                    candidate[self.Database[i][j]] = 1
                else:
                    candidate[self.Database[i][j]] += 1
        self.finalFps = {keys: value for keys, value in candidate.items() if value >= self.minSup}

    # def less_items():
    #    pass

    def dictKeysToInt(self, a):
        """Converting dictionary keys to integer elements

        :param a: Dictionary with item sets as keys with list of strings type and their support count as
            value
        :type a: dict
        :returns: a list of integer item sets to represent dictionary keys
        :rtype: list
        """

        temp = []
        for ite in a.keys():
            ite = [int(i) for i in ite.strip('[]').split(',')]
            temp.append(ite)
            # print(sorted(temp))
        return sorted(temp)

    def subset_creation(self, transaction, length_subset):
        """Generating combination of itemsets

            :param transaction: Total list of transactions of the database, each with items
            :type transaction: list
            :param length_subset: No of elements in the combination of items
            :type length_subset: int
            :returns: list of combinations of items each with of length equals to length_subset
            :rtype: list
            """

        subset = list(c(transaction, length_subset))
        temp = []
        for i in range(len(subset)):
            final_list = sorted(list(subset[i]))
            temp.append(final_list)
        return sorted(temp)

    def apriori_generate(self, listofitemsets, k):
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
                list1 = list(listofitemsets[i])[:k - 2]
                list2 = list(listofitemsets[j])[:k - 2]
                if list1 == list2:
                    ck.append(sorted(list(set(listofitemsets[i]) | set(listofitemsets[j]))))
        # print(ck)
        # prune step
        final_ck = []
        for candidate in ck:
            all_subsets = self.subset_creation(candidate, k - 1)
            found = True
            for i in range(len(all_subsets)):
                value = list(sorted(all_subsets[i]))
                if value not in listofitemsets:
                    found = False
                    break
            if found:
                final_ck.append(candidate)

        # print(final_ck)

        return sorted(final_ck)

    def startMine(self):
        """main program to start the operation
        """

        global itemSets, endTime, startTime
        global noOfChildren, maxRecordsInNonLeaf
        startTime = time.time()

        if self.data is None:
            raise Exception("Please enter the file path or file name:")
            # quit()
        iFileName = self.data
        if self.minSup is None:
            raise Exception("Please enter the Minimum Support")
        # Database = []
        if self.minSup <= 0:
            raise Exception(
                "Please enter the Minimum Support between (0,1) in percentage(%) calculated with database count")
            # quit()

        self.creatingItemsets(iFileName)

        if self.minSup > len(self.Database):
            raise Exception("Please enter the minSup in range between 0 to 1")
            # quit()

        self.minSup = (len(self.Database) * self.minSup)

        # print(minSup)
        self.frequent_one_item()
        # Sorting one frequent item sets
        frequent_one = sorted([int(i) for i in self.finalFps.keys()])

        iteration = True
        list_for_next_iteration = []
        iter = 2
        while iteration:
            # print("hello")
            if iter == 2:
                # Generation of candiate two item sets and adding the same to Hash tree
                comb = self.subset_creation(frequent_one, 2)  # list(c(frequent_one, 2))
                # print(comb)
            else:
                comb = self.apriori_generate(list_for_next_iteration, iter)
                # print("comb")
            if len(comb) == 1:
                count = 0
                for i in range(len(self.Database)):
                    rowOfDatabase = set(int(t) for t in self.Database[i])
                    if set(comb[0]).issubset(rowOfDatabase):
                        count += 1
                if count >= self.minSup:
                    self.finalFps[str(comb)] = count
                break
            if not comb:
                break
            maintain = Tree()
            # Inserting Candidate itemsets into hash tree
            for i in range(len(comb)):
                test = comb[i]  # sorted([int(t) for t in comb[i]])
                maintain.first_element(test)
            for i in range(len(self.Database)):
                rowOfDatabase = [int(t) for t in self.Database[i]]
                subse = self.subset_creation(rowOfDatabase, iter)
                for j in range(len(subse)):
                    maintain.Tree_search(subse[j])

            items_after_support = {keys: value for keys, value in itemSets.items() if value >= self.minSup}
            # print(iter, "frequent itemsets :", len(items_after_support))
            if items_after_support is None:
                # iteration = False
                break
            self.finalFps.update(items_after_support)
            # print("Total frequent item sets are:", len(finalFps))
            if len(items_after_support) == 0 or len(items_after_support) == 1:
                # print("Total frequent item sets are:", len(finalFps))
                break
            list_for_next_iteration = self.dictKeysToInt(items_after_support)
            items_after_support.clear()
            itemSets.clear()

            iter += 1

        endTime = time.time()
        print("Frequent itemsets were generated successfully using AprioriHashtree algorithm")

    def getMemory(self):
        """Calculating the amount of memory consumed by the Apriori algorithm

        """
        # import psutil
        # global minSup
        process = psutil.Process(os.getpid())
        memory = process.memory_full_info().uss  # process.memory_info().rss
        memoryInMb = memory / (1024 * 1024)
        return memoryInMb
        # print(memoryInMb)  # in bytes
        # print("Total Memory is:", memoryInMb)

    def getRuntime(self):
        """Calculating the total amount of execution time taken by the Apriori algorithm

        """
        global endTime, startTime
        return endTime - startTime

    def getPatternInDf(self):
        """Storing final frequent itemsets in a dataframe and converting it to .csv file
        """
        # import pandas as pd
        # global finalFps
        df = {}
        # for x,y in self.finalFps.items():
        data = []
        for a, b in self.finalFps.items():
            data.append([a, b])
            # print(x)
            # s = "output" + str(x)+".CSV"
            df = pd.DataFrame(data, columns=['Patterns', 'Support'])
        # print("Total frequent itemsets are:", len(df))
        return df

    def getPatternsInFile(self, outputfile):
        """ Function get the frequent patterns in to a outputfile
        
        :param outputfile: Storing all frequent patterns in a file
        :type outputfile: file
        """

        # data = Path(sys.argv[1])
        # global finalFps
        writer = open(outputfile, 'w+')
        for x, y in self.finalFps.items():
            # s = "output" + str(x)
            s1 = str(x) + ":" + str(y)
            writer.write("%s \n" % s1)
        # InFile()

    def getFPs(self):
        """Returing final frequent itemsets in a Dictionary

        Returns
        -------
        defaultdict

        """
        return self.finalFps

    # def getStatsInFile(self,statsfile):
    #     """ Printing the statistics of the database into a Statistics file
    #     :param global Database variable: Storing the data in to a Database variable
    #     :type Database: defaultdict
    #     """
    #     #global Database
    #     sum1 = 0
    #     min1 = 999999
    #     max1 = -1
    #     tot = 0
    #     si = []
    #     l1 = 0
    #     s = statsfile
    #     writer1 = open(s, 'w+')
    #     for line in self.Database:
    #         l = line
    #         for i in l:
    #             if i not in si:
    #                 si.append(i)
    #         if (len(l) > max1):
    #             max1 = len(l)
    #         sum1 += len(l)
    #         if (len(l) < min1):
    #             min1 = len(l)
    #         tot += len(l)
    #     s = "Total number of transactions:" + str(len(self.Database))
    #     writer1.write("%s \n" % s)
    #     s = "Total number of items:" + str(len(si))
    #     writer1.write("%s \n" % s)
    #     s = "Minimum length of a transaction: " + str(min1)
    #     writer1.write("%s \n" % s)
    #     s = "Maximum length of a transaction: " + str(max1)
    #     writer1.write("%s \n" % s)
    #     s = "Avg length of a transaction: " + str(tot / len(self.Database))
    #     writer1.write("%s \n" % s)
