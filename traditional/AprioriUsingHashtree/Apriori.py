from traditional.abstractClass.abstractFrequentPatterns import *

itemSets = defaultdict()

# Input for Hash mod function f(x) mod noOfChildren
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
        createChildren()
            creating children to hash tree
        setChildrenValue(data_list)
            Attach the list of data values into the children of the tree
        splitting(level)
            No of elements in a particular tree is crosses the user specified limit splitting
            is performed based on level attribute
        insertion(data, level)
            Inserting data into a particular node in a particular level of the hash tree
        firstElement(data)
            Inserting the first element into the hash tree
        treeDisplay(parent, length)
            Displaying the content of the tree based on the total number of elements and parent node
        treeSearch(element)
            Searching a particular element in a hash tree
    """

    def __init__(self):
        self.child = []
        self.data = []
        self.leaf = True
        self.level = 0

    # Creating the children of a particular node

    def createChildren(self):
        """Creating children to the hash tree total of noOfChildren"""

        global noOfChildren
        self.leaf = False
        for i in range(0, noOfChildren):
            self.child.append(Tree())

    # Adding values to the tree node

    def setChildrenValue(self, dataList):
        """ Attach the list of data values into the children of the tree

        :param dataList: item set in a list format
        :type dataList: list
        :return: returns the number of data elements in a child node of a hash tree as a rowcount
        :rtype: int
        """
        self.data.append(dataList)
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

        global noOfChildren
        self.level = level

        self.createChildren()
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

        global noOfChildren, maxRecordsInNonLeaf
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
    def firstElement(self, data):
        """Inserting the first element into the hash tree

        :param data: list of item sets to be inserted into the hash tree
        :type data: list
        """

        level = 0
        # data_length = len(data)
        # print(self.level)
        if not self.child:
            First = int(data[level]) % noOfChildren

            self.createChildren()

            self.child[First].data.append(data)  # setChildrenValue(data)
        else:
            self.insertion(data, level)

    # Displaying the content of the complete tree from left to right (Child  0 to Child length )
    def treeDisplay(self, parent, length):
        """Displaying the content of the hash tree

        :param parent: Object reference of the parent node of the current node
        :param length: Representing the depth of the hash tree
        :type length: int
        :return: returning zero after displaying all the elements of the hash tree
        """

        if self.leaf is False:
            for i in range(length):
                parent = self
                self.child[i].treeDisplay(parent, length)

        else:
            if not self.data:
                return 0
            else:
                print(self.data)
                print(parent.level)

    def treeSearch(self, element):
        """Searching a particular element in a hash tree and if it is identified we ll increment the count
            that element by 1 other returning the cursor to called function without any modification

        :param element: list of item set to be searched in the hash tree
        :type element: list
        :return: returning non zero value to the called function after searching the particular element
        """

        if self.leaf is False:
            indexing111 = element[self.level] % noOfChildren
            # print(indexing111) # for displaying the path of the element evaluation
            self.child[indexing111].treeSearch(element)
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


class Apriori(frequentPatterns):
    """

    """
    minSup = float()
    startTime = float()
    endTime = float()
    finalPatterns = {}
    iFile = " "
    oFile = " "
    memoryUSS = float()
    memoryRSS = float()
    Database = []

    @staticmethod
    def check(line):
        """Identifying the delimiter of the input file

            :param line: list of special characters may be used by a user to separate the items in a input file
            :type line: list of string
            :returns: Delimited string used in the input file to separate each item
            :rtype: string
            """
        listOfDelimiters = [',', '*', '&', ' ', '%', '$', '#', '@', '!', '    ', '*', '(', ')']
        j = None
        # print(line)
        for i in listOfDelimiters:
            if i in line:
                return i
        return j

    def creatingItemSets(self, iFileName):
        """Creating a Database from input file and updating the same to global variable finalPatterns

            :param iFileName: User given input file path with each row as a single transaction
            :type iFileName: str
            """
        # import pandas as pd
        # global Database
        self.Database = []
        lno = 0
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
                        if lno == 0:
                            lno += 1
                            delimiter = self.check([*line])
                            # li=[lno]
                            li = line.split(delimiter)
                            li1 = [i.rstrip() for i in li]
                            self.Database.append([i.rstrip() for i in li1])
                            # else:
                            # self.Database.append(li)
                            # data.append([lno,li1])
                        else:
                            lno += 1
                            li = line.split(delimiter)
                            # if delimiter==',':
                            li1 = [i.rstrip() for i in li]
                            self.Database.append(li1)
            except IOError:
                print("File Not Found")
                quit()

        # else:
        # self.Database=iFileName['Transactions'].tolist()

    # function to get frequent one item set
    def frequentOneItem(self):
        """Generating One frequent items sets and updating the same to global variable finalPatterns

        """

        candidate = {}
        # global finalPatterns, minSup, Database
        # self.minSup = self.minSup
        for i in range(len(self.Database)):
            for j in range(len(self.Database[i])):
                if self.Database[i][j] not in candidate:
                    candidate[self.Database[i][j]] = 1
                else:
                    candidate[self.Database[i][j]] += 1
        self.finalPatterns = {keys: value for keys, value in candidate.items() if value >= self.minSup}

    # def less_items():
    #    pass

    @staticmethod
    def dictKeysToInt(iList):
        """Converting dictionary keys to integer elements

        :param iList: Dictionary with item sets as keys with list of strings type and their support count as a value
        :type iList: dict
        :returns: a list of integer item sets to represent dictionary keys
        :rtype: list
        """

        temp = []
        for ite in iList.keys():
            ite = [int(i) for i in ite.strip('[]').split(',')]
            temp.append(ite)
            # print(sorted(temp))
        return sorted(temp)

    @staticmethod
    def subsetCreation(transaction, lengthSubset):
        """Generating combination of item sets

            :param transaction: Total list of transactions of the database, each with items
            :type transaction: list
            :param lengthSubset: No of elements in the combination of items
            :type lengthSubset: int
            :returns: list of combinations of items each with of length equals to lengthSubset
            :rtype: list
            """

        subset = list(c(transaction, lengthSubset))
        temp = []
        for i in range(len(subset)):
            finalList = sorted(list(subset[i]))
            temp.append(finalList)
        return sorted(temp)

    def aprioriGenerate(self, listOfItemSets, nLength):
        """Apriori Generation function along with item pruning of redundant items

            :param listOfItemSets: list of k-1 length item sets for generating k length length item sets
            :type listOfItemSets: list
            :param nLength: length of the next item sets
            :type nLength: int
            :returns: list of final candidate item sets of length k after pruning k-1 length item sets
            :rtype: list
            """

        ck = []
        # join step
        lengthK = len(listOfItemSets)
        for i in range(lengthK):
            for j in range(i + 1, lengthK):
                list1 = list(listOfItemSets[i])[:nLength - 2]
                list2 = list(listOfItemSets[j])[:nLength - 2]
                if list1 == list2:
                    ck.append(sorted(list(set(listOfItemSets[i]) | set(listOfItemSets[j]))))
        # print(ck)
        # prune step
        finalCandidateK = []
        for candidate in ck:
            all_subsets = self.subsetCreation(candidate, nLength - 1)
            found = True
            for i in range(len(all_subsets)):
                value = list(sorted(all_subsets[i]))
                if value not in listOfItemSets:
                    found = False
                    break
            if found:
                finalCandidateK.append(candidate)

        # print(finalCandidateK)

        return sorted(finalCandidateK)

    def startMine(self):
        """main program to start the operation"""

        # global  endTime, startTime, minSup, iFile
        global noOfChildren, maxRecordsInNonLeaf, itemSets
        self.startTime = time.time()
        # minSup = self.minSup
        # iFile = self.iFile

        if self.iFile is None:
            raise Exception("Please enter the file path or file name:")
            # quit()
        iFileName = self.iFile
        if self.minSup is None:
            raise Exception("Please enter the Minimum Support")
        # self.Database = []
        if self.minSup <= 0:
            raise Exception(
                "Please enter the Minimum Support between (0,1) in percentage(%) calculated with database count")
            # quit()

        self.creatingItemSets(iFileName)

        if self.minSup > len(self.Database):
            raise Exception("Please enter the minSup in range between 0 to 1")
            # quit()

        # self.minSup = (len(self.Database) * self.minSup)

        # print(self.minSup)
        self.frequentOneItem()
        # Sorting one frequent item sets
        frequentOne = sorted([int(i) for i in self.finalPatterns.keys()])

        iteration = True
        listForNextIteration = []
        temp = 2
        while iteration:
            # print("hello")
            if temp == 2:
                # Generation of candidate two item sets and adding the same to Hash tree
                comb = self.subsetCreation(frequentOne, 2)  # list(c(frequentOne, 2))
                # print(comb)
            else:
                comb = self.aprioriGenerate(listForNextIteration, temp)
                # print("comb")
            if len(comb) == 1:
                count = 0
                for i in range(len(self.Database)):
                    rowOfDatabase = set(int(t) for t in self.Database[i])
                    if set(comb[0]).issubset(rowOfDatabase):
                        count += 1
                if count >= self.minSup:
                    self.finalPatterns[str(comb)] = count
                break
            if not comb:
                break
            maintain = Tree()
            # Inserting Candidate item sets into hash tree
            for i in range(len(comb)):
                test = comb[i]  # sorted([int(t) for t in comb[i]])
                maintain.firstElement(test)
            for i in range(len(self.Database)):
                rowOfDatabase = [int(t) for t in self.Database[i]]
                subSet = self.subsetCreation(rowOfDatabase, temp)
                for j in range(len(subSet)):
                    maintain.treeSearch(subSet[j])

            itemsAfterSupport = {keys: value for keys, value in itemSets.items() if value >= self.minSup}
            # print(iter, "frequent item sets :", len(itemsAfterSupport))
            if itemsAfterSupport is None:
                # iteration = False
                break
            self.finalPatterns.update(itemsAfterSupport)
            # print("Total frequent item sets are:", len(self.finalPatterns))
            if len(itemsAfterSupport) == 0 or len(itemsAfterSupport) == 1:
                # print("Total frequent item sets are:", len(self.finalPatterns))
                break
            listForNextIteration = self.dictKeysToInt(itemsAfterSupport)
            itemsAfterSupport.clear()
            itemSets.clear()

            temp += 1

        self.endTime = time.time()
        process = psutil.Process(os.getpid())
        self.memoryUSS = process.memory_full_info().uss
        self.memoryRSS = process.memory_info().rss
        print("Frequent item sets were generated successfully using Apriori Hash tree algorithm")

    def getMemoryUSS(self):
        """Total amount of USS memory consumed by the program will be retrieved from this function"""

        return self.memoryUSS

    def getMemoryRSS(self):
        """Total amount of RSS memory consumed by the program will be retrieved from this function"""

        return self.memoryRSS

    def getRuntime(self):
        """Calculating the total amount of execution time taken by the Apriori algorithm"""
        # global endTime, startTime
        return self.endTime - self.startTime

    def getPatternsInDataFrame(self):
        """Storing final frequent item sets in a dataframe and converting it to .csv file"""

        # global finalPatterns
        df = {}
        # for x,y in self.finalPatterns.items():
        data = []
        for a, b in self.finalPatterns.items():
            data.append([a, b])
            # print(x)
            # s = "output" + str(x)+".CSV"
            df = pd.DataFrame(data, columns=['Patterns', 'Support'])
        # print("Total frequent item sets are:", len(df))
        return df

    def storePatternsInFile(self, outputFile):
        """ Function get the frequent patterns in to a outputFile

        :param outputFile: Storing all frequent patterns in a file
        :type outputFile: file
        """

        # data = Path(sys.argv[1])
        # global finalPatterns
        writer = open(outputFile, 'w+')
        for x, y in self.finalPatterns.items():
            # s = "output" + str(x)
            s1 = str(x) + ":" + str(y)
            writer.write("%s \n" % s1)
        # InFile()

    def getFrequentPatterns(self):
        """Returning final frequent item sets in a Dictionary

        """
        # global finalPatterns

        return self.finalPatterns
