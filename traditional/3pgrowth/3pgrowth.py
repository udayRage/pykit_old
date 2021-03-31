from traditional.abstractClass.abstractPartialPeriodic import *
import sys

periodicSupport = float()
period = float()
lno = int()


class Node(object):
    """
            A class used to represent the node of frequentPatternTree

                ...

                Attributes
                ----------
                item : int
                    storing item of a node
                timeStamps : list
                    To maintain the timestamps of transaction at the end of the branch
                parent : node
                    To maintain the parent of every node
                children : list
                    To maintain the children of node

                Methods
                -------

                addChild(itemName)
                    storing the children to their respective parent nodes
            """
    def __init__(self, item, children):
        self.item = item
        self.children = children
        self.parent = None
        self.timeStamps = []

    def addChild(self, node):
        self.children[node.item] = node
        node.parent = self


class Tree(object):
    """
                A class used to represent the frequentPatternGrowth tree structure

                ...

                Attributes
                ----------
                root : Node
                    Represents the root node of the tree
                summaries : dictionary
                    storing the nodes with same item name
                info : dictionary
                    stores the support of items


                Methods
                -------
                add_transaction(transaction)
                    creating transaction as a branch in frequentPatternTree
                addTransaction(prefixPaths, supportOfItems)
                    construct the conditional tree for prefix paths
                condition_patterns(Node)
                    generates the conditional patterns from tree for specific node
                cond_trans(prefixPaths,Support)
                    takes the prefixPath of a node and support at child of the path and extract the frequent items from
                    prefixPaths and generates prefixPaths with items which are frequent
                remove(Node)
                    removes the node from tree once after generating all the patterns respective to the node
                generate_patterns(Node)
                    starts from the root node of the tree and mines the frequent patterns

            """
    def __init__(self):
        self.root = Node(None, {})
        self.summaries = {}
        self.info = {}

    def addTransaction(self, transaction, tid):
        """
                adding transaction into tree

                        :param transaction : it represents the one transactions in database
                        :type transaction : list
                        :param tid : represents the timestamp of transaction
                        :type tid : list
                """
        currentNode = self.root
        for i in range(len(transaction)):
            if transaction[i] not in currentNode.children:
                newNode = Node(transaction[i], {})
                currentNode.addChild(newNode)
                if transaction[i] in self.summaries:
                    self.summaries[transaction[i]].append(newNode)
                else:
                    self.summaries[transaction[i]] = [newNode]
                currentNode = newNode
            else:
                currentNode = currentNode.children[transaction[i]]
            currentNode.timeStamps = currentNode.timeStamps + tid

    def getConditionalPatterns(self, alpha):
        """generates all the conditional patterns of respective node

                            :param alpha : it represents the Node in tree
                            :type alpha : Node
                """
        finalPatterns = []
        finalSets = []
        for i in self.summaries[alpha]:
            set1 = i.timeStamps
            set2 = []
            while i.parent.item is not None:
                set2.append(i.parent.item)
                i = i.parent
            if len(set2) > 0:
                set2.reverse()
                finalPatterns.append(set2)
                finalSets.append(set1)
        finalPatterns, finalSets, info = self.conditionalTransactions(finalPatterns, finalSets)
        return finalPatterns, finalSets, info

    def generateTimeStamps(self, node):
        finalTs = node.timeStamps
        return finalTs

    def removeNode(self, nodeValue):
        """removing the node from tree

                                :param nodeValue : it represents the node in tree
                                :type nodeValue : node
                                """
        for i in self.summaries[nodeValue]:
            i.parent.timeStamps = i.parent.timeStamps + i.timeStamps
            del i.parent.children[nodeValue]
            i = None

    def getTimeStamps(self, alpha):
        temporary = []
        for i in self.summaries[alpha]:
            temporary += i.timeStamps
        return temporary

    def getPeriodicSupport(self, timeStamps):
        """
                    calculates the support and periodicity with list of timestamps

                    :param timeStamps : timestamps of a pattern
                    :type timeStamps : list


                            """
        timeStamps = list(set(timeStamps))
        timeStamps.sort()
        per = 0
        sup = 0
        for i in range(len(timeStamps) - 1):
            j = i + 1
            if abs(timeStamps[j] - timeStamps[i]) <= period:
                per += 1
            sup += 1
        return [per]

    def conditionalTransactions(self, conditionalPatterns, conditionalTimeStamps):
        """ It generates the conditional patterns with periodic frequent items

                        :param conditionalPatterns : conditional_patterns generated from condition_pattern method for
                                            respective node
                        :type conditionalPatterns : list
                        :param conditionalTimeStamps : represensts the timestamps of conditional patterns of a node
                        :type conditionalTimeStamps : list
                        """
        global periodicSupport, period
        pat = []
        timeStamps = []
        data1 = {}
        for i in range(len(conditionalPatterns)):
            for j in conditionalPatterns[i]:
                if j in data1:
                    data1[j] = data1[j] + conditionalTimeStamps[i]
                else:
                    data1[j] = conditionalTimeStamps[i]
        updatedDictionary = {}
        for m in data1:
            updatedDictionary[m] = self.getPeriodicSupport(data1[m])
        updatedDictionary = {k: v for k, v in updatedDictionary.items() if v[0] >= periodicSupport}
        count = 0
        for p in conditionalPatterns:
            p1 = [v for v in p if v in updatedDictionary]
            trans = sorted(p1, key=lambda x: (updatedDictionary.get(x)[0], -x), reverse=True)
            if (len(trans) > 0):
                pat.append(trans)
                timeStamps.append(conditionalTimeStamps[count])
            count += 1
        return pat, timeStamps, updatedDictionary

    def generatePatterns(self, prefix):
        """generates the patterns

                        :param prefix : forms the combination of items
                        :type prefix : list
                        """
        for i in sorted(self.summaries, key=lambda x: (self.info.get(x)[0], -x)):
            pattern = prefix[:]
            pattern.append(i)
            yield (pattern, self.info[i])
            patterns, timeStamps, info = self.getConditionalPatterns(i)
            conditionalTree = Tree()
            conditionalTree.info = info.copy()
            for pat in range(len(patterns)):
                conditionalTree.addTransaction(patterns[pat], timeStamps[pat])
            if len(patterns) > 0:
                for q in conditionalTree.generatePatterns(pattern):
                    yield q
            self.removeNode(i)


class PPPgrowth:

    periodicSupport = float()
    period = float()
    startTime = float()
    endTime = float()
    finalPatterns = {}
    iFile = " "
    oFile = " "
    memoryUSS = float()
    memoryRSS = float()
    transaction = []
    rank = {}
    rankdup = {}
    lno = 0

    """
        Parameters
            ----------
            self.iFile : file
                Name of the Input file to mine complete set of frequent patterns
           self. oFile : file
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
                it represents the Tree class
            itemSetCount : int
                it represents the total no of patterns
            finalPatterns : dict
                it represents to store the patterns

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
                To check the delimiter used in the user input file
            creatingItemSets(fileName)
                Scans the dataset or dataframes and stores in list format
            partialPeriodicOneItem()
                Extracts the one-frequent patterns from transactions
            updateTransactions()
                updates the transactions by removing the aperiodic items and sort the transactions with items 
                by decreaing support
            buildTree()
                constrcuts the main tree by setting the root node as null
            startMine()
                main program to mine the partial periodic patterns
            


            """

    def findDelimiter(self, line):
        """Identifying the delimiter of the input file

            :param line: list of special characters may be used by a user to split the items in a input file
            :type line: list of string
            :returns: Delimited string used in the input file to split each item
            :rtype: string
            """
        l = [',', '*', '&', '', '%', '$', '#', '@', '!', '    ', '*', '(', ')']
        j = None
        for i in l:
            if i in line:
                return i
        return j

    def creatingItemSets(self):
        """
            Storing the complete transactions of the database/input file in a database variable

            :param self.iFile: user given input file/input file path
            :type self.iFile: str


            """
        if isinstance(self.iFile, list):
            self.transaction = self.iFile
        if isinstance(self.iFile, pd.DataFrame):
            if self.iFile.empty:
                print("its empty..")
            i = self.iFile.columns.values.tolist()
            if 'Transactions' in i:
                self.transaction = self.iFile['Transactions'].tolist()
            if 'Patterns' in i:
                self.transaction = self.iFile['Patterns'].tolist()

        if '.CSV' in self.iFile:
            file1 = pd.read_csv(self.iFile)
            columns = list(file1.head(0))
            if "Patterns" in columns:
                with open(self.iFile, newline='') as csvFile:
                    data = csv.DictReader(csvFile)
                    for row in data:
                        l = row['Patterns']
                        l1 = l.replace("[", "")
                        l2 = l1.replace("]", "")
                        li = list(l2.split(","))
                        li1 = [int(i) for i in li]
                        self.transaction.append(li1)
            if "Transactions" in columns:
                with open(self.iFile, newline='') as csvFile:
                    data = csv.DictReader(csvFile)
                    for row in data:
                        l = row['Transactions']
                        l1 = l.replace("[", "")
                        l2 = l1.replace("]", "")
                        li = list(l2.split(","))
                        li1 = [int(i) for i in li]
                        self.transaction.append(li1)
        else:
            try:
                with open(self.iFile, 'r', encoding='utf-8') as f:
                    for line in f:
                        if self.lno == 0:
                            delimiter = self.findDelimiter([*line])
                            li1 = [i.strip(delimiter) for i in line.split(delimiter)]
                            self.transaction.append(li1)
                        else:
                            li1 = [i.strip(delimiter) for i in line.split(delimiter)]
                            self.transaction.append(li1)
                        self.lno += 1
            except IOError:
                print("File Not Found")

    def partialPeriodicOneItem(self):
        """
                    calculates the support of each item in the dataset and assign the ranks to the items
                    by decreasing support and returns the frequent items list

                    """
        data = {}
        for tr in self.transaction:
            for i in range(1, len(tr)):
                if tr[i] not in data:
                    data[tr[i]] = [0, int(tr[0]), 1]
                else:
                    lp = int(tr[0]) - data[tr[i]][1]
                    if lp <= self.period:
                        data[tr[i]][0] += 1
                    data[tr[i]][1] = int(tr[0])
                    data[tr[i]][2] += 1
        data = {k: [v[0]] for k, v in data.items() if v[0] >= self.periodicSupport}
        pfList = [k for k, v in sorted(data.items(), key=lambda x: (x[1][0], x[0]), reverse=True)]
        self.rank = dict([(index, item) for (item, index) in enumerate(pfList)])
        return data, pfList

    def updateTransactions(self, dict1):
        """remove the items which are not frequent from transactions and updates the transactions with rank of items

                    :param dict1 : frequent items with support
                    :type dict1 : dictionary
                    """
        list1 = []
        for tr in self.transaction:
            list2 = [int(tr[0])]
            for i in range(1, len(tr)):
                if tr[i] in dict1:
                    list2.append(self.rank[tr[i]])
            if len(list2) >= 2:
                basket = list2[1:]
                basket.sort()
                list2[1:] = basket[0:]
                list1.append(list2)
        return list1

    def buildTree(self, data, info):
        """it takes the transactions and support of each item and construct the main tree with setting root
                            node as null

                                :param data : it represents the one transactions in database
                                :type data : list
                                :param info : it represents the support of each item
                                :type info : dictionary
                                """
        rootNode = Tree()
        rootNode.info = info.copy()
        for i in range(len(data)):
            set1 = []
            set1.append(data[i][0])
            rootNode.addTransaction(data[i][1:], set1)
        return rootNode

    def savePeriodic(self, itemset):
        t1 = []
        for i in itemset:
            t1.append(self.rankdup[i])
        return t1

    def startMine(self):
        """
                   Main method where the patterns are mined by constructing tree.

               """
        global periodicSupport, period, lno
        self.startTime = time.time()
        if self.iFile == None:
            raise Exception("Please enter the file path or file name:")
        if self.periodicSupport == None:
            raise Exception("Please enter the Minimum Support")
        self.creatingItemSets()
        self.periodicSupport = self.periodicSupport * len(self.transaction)
        self.period = self.period * len(self.transaction)
        periodicSupport, period, lno = self.periodicSupport, period, len(self.transaction)
        if self.periodicSupport > len(self.transaction):
            raise Exception("Please enter the minSup in range between 0 to 1")
        generatedItems, pfList = self.partialPeriodicOneItem()
        updatedTransactions = self.updateTransactions(generatedItems)
        for x, y in self.rank.items():
            self.rankdup[y] = x
        info = {self.rank[k]: v for k, v in generatedItems.items()}
        Tree = self.buildTree(updatedTransactions, info)
        patterns = Tree.generatePatterns([])
        for i in patterns:
            self.finalPatterns[tuple(i[0])] = i[1]
        self.endTime = time.time()
        process = psutil.Process(os.getpid())
        self.memoryUSS = process.memory_full_info().uss
        self.memoryRSS = process.memory_info().rss
        print("Partial Periodic Patterns were generated successfully using 3P algorithm ")

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

    def getPartialPeriodicPatterns(self):
        """ Function to send the set of frequent patterns after completion of the mining process

        :return: returning frequent patterns
        :rtype: dict
        """
        return self.finalPatterns

if __name__ == "__main__":
    ap = PPPgrowth()
    ap.iFile = sys.argv[1]
    ap.oFile = sys.argv[2]
    ap.periodicSupport = float(sys.argv[3])
    ap.period= float(sys.argv[4])
    ap.startMine()
    frequentPatterns = ap.getPartialPeriodicPatterns()
    print("Total number of Frequent Patterns:", len(frequentPatterns))
    ap.storePatternsInFile(sys.argv[2])
    memUSS = ap.getMemoryUSS()
    print("Total Memory in USS:", memUSS)
    memRSS = ap.getMemoryRSS()
    print("Total Memory in RSS", memRSS)
    run = ap.getRuntime()
    print("Total ExecutionTime in seconds:", run)
