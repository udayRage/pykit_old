import sys
from traditional.abstractClass.abstractPeriodicPatterns import *


minSup = float()
maxPer = float()
lno = int()
first = int()
last = int()
periodic = {}
rankdup = {}


class Item:
    """
                    A class used to represent the item with probability in transaction of dataset

                    ...

                    Attributes
                    __________
                    item : int or word
                        Represents the name of the item
                    probability : float
                        Represent the existential probability(likelihood presence) of an item
                """
    def __init__(self, item, probability):
        self.item = item
        self.probability = probability
        

class Node(object):
    """
                A class used to represent the node of frequentPatternTree

                    ...

                    Attributes
                    ----------
                    item : int
                        storing item of a node
                    probability : int
                        To maintain the expected support of node
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
        self.probability = 1
        self.secondProbability = 1
        self.p = 1
        self.children = children
        self.parent = None
        self.tids = []

    def addChild(self, node):
        self.children[node.item] = node
        node.parent = self
        

def Second(transactions, i):
    l = []
    for j in range(0, i):
        l.append(transactions[j].probability)
    l1 = max(l)
    l.remove(l1)
    l2 = max(l)
    return l2


def printTree(root):
    for x, y in root.children.items():
        print(x, y.item, y.probability, y.parent.item, y.tids, y.secondProbability)
        printTree(y)


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

    def add_transaction(self, transaction, tid):
        """adding transaction into tree

                                        :param transaction : it represents the one transactions in database
                                        :type transaction : list
                                        :param tid : the timestamp of transaction
                                        :type tid : list
                                        """
        curr_node = self.root
        k = 0
        for i in range(len(transaction)):
            k += 1
            if transaction[i].item not in curr_node.children:
                new_node = Node(transaction[i].item, {})
                new_node.k = k
                if k >= 3:
                    new_node.secondProbability = Second(transaction, i)
                l1 = i-1
                l = []
                while l1 >= 0:
                    l.append(transaction[l1].probability)
                    l1 -= 1
                if len(l) == 0:
                    new_node.probability = round(transaction[i].probability, 2)
                else:
                    new_node.probability = round(max(l) * transaction[i].probability, 2)
                curr_node.addChild(new_node)
                if transaction[i].item in self.summaries:
                    self.summaries[transaction[i].item].append(new_node)
                else:
                    self.summaries[transaction[i].item] = [new_node]
                curr_node = new_node
            else:
                curr_node = curr_node.children[transaction[i].item]
                if k >= 3:
                    curr_node.secondProbability = max(transaction[i].probability, curr_node.secondProbability)
                curr_node.k = k
                l1 = i-1
                l = []
                while l1 >= 0:
                    l.append(transaction[l1].probability)
                    l1 -= 1
                if len(l) == 0:
                    curr_node.probability += round(transaction[i].probability, 2)
                else:
                    nn = max(l) * transaction[i].probability
                    curr_node.probability += round(nn, 2)
        curr_node.tids = curr_node.tids + tid

    def addTransaction(self, transaction, tid, sup, second):
        """constructing conditional tree from prefixPaths

                        :param transaction : it represents the one transactions in database
                        :type transaction : list
                        :param tid : timestamps of a pattern or transaction in tree
                        :param tid : list
                        :param sup : support of prefixPath taken at last child of the path
                        :type sup : int
                                                """
        curr_node = self.root
        k = 0
        for i in range(len(transaction)):
            k += 1
            if transaction[i] not in curr_node.children:
                new_node = Node(transaction[i], {})
                new_node.k = k
                new_node.secondProbability = second
                new_node.probability = sup
                curr_node.addChild(new_node)
                if transaction[i] in self.summaries:
                    self.summaries[transaction[i]].append(new_node)
                else:
                    self.summaries[transaction[i]] = [new_node]
                curr_node = new_node
            else:
                curr_node = curr_node.children[transaction[i]]
                curr_node.k = k
                curr_node.secondProbability = max(curr_node.secondProbability, second)
                curr_node.probability += sup
        curr_node.tids = curr_node.tids + tid

    def condition_pattern(self, alpha):
        """generates all the conditional patterns of respective node

                        :param alpha : it represents the Node in tree
                        :type alpha : Node
                                        """
        final_patterns = []
        final_sets = []
        sup = []
        second = []
        for i in self.summaries[alpha]:
            q= self.genrate_tids(i)
            set1 = i.tids
            s = i.probability
            s1 = i.secondProbability
            set2 = []
            while i.parent.item != None:
                set2.append(i.parent.item)
                i = i.parent
            if len(set2) > 0:
                set2.reverse()
                final_patterns.append(set2)
                final_sets.append(set1)
                second.append(s1)
                sup.append(s)
        final_patterns, final_sets, support, info = cond_trans(final_patterns, final_sets, sup)
        return final_patterns, final_sets, support, info, second

    def genrate_tids(self, node):
        final_tids = node.tids
        return final_tids

    def remove_node(self, node_val):
        """removing the node from tree

                        :param nodeValue : it represents the node in tree
                        :type nodeValue : node
                                       """
        for i in self.summaries[node_val]:
            i.parent.tids = i.parent.tids + i.tids
            del i.parent.children[node_val]
            i = None

    def get_ts(self, alpha):
        temp_ids = []
        for i in self.summaries[alpha]:
            temp_ids += i.tids
        return temp_ids
            
    def generate_patterns(self, prefix):
        """generates the patterns

                                        :param prefix : forms the combination of items
                                        :type prefix : list
                                        """
        global periodic
        for i in sorted(self.summaries, key= lambda x: (self.info.get(x)[0])):
            pattern = prefix[:]
            pattern.append(i)
            s = 0
            for x in self.summaries[i]:
                if x.k <= 2:
                    s += x.probability
                elif x.k >= 3:
                    n = x.probability*pow(x.secondProbability, (x.k-2))
                    s += n
            yield pattern, self.info[i]
            periodic[tuple(pattern)] = self.info[i]
            if s >= minSup:
                patterns, tids, support, info, second = self.condition_pattern(i)
                conditional_tree = Tree()
                conditional_tree.info = info.copy()
                for pat in range(len(patterns)):
                    conditional_tree.addTransaction(patterns[pat], tids[pat], support[pat], second[pat])
                if len(patterns) > 0:
                    for q in conditional_tree.generate_patterns(pattern):
                        yield q
            self.remove_node(i)
    

def getPer_Sup(s, tids):
    """

            Parameters
            ----------
            support
            tids

            Returns
            -------
            support and period

            """
    global lno, maxPer
    tids.sort()
    cur = 0
    per = 0
    sup = s
    for j in range(len(tids)):
        per = max(per, tids[j]-cur)
        if per > maxPer:
            return [0, 0]
        cur = tids[j]
    per = max(per, lno-cur)
    return [sup, per]


def cond_trans(conditionalPatterns, conditionalTids, support):
    """ It generates the conditional patterns with frequent items

                :param conditionalPatterns : conditional_patterns generated from condition_pattern method for respective node
                :type conditionalPatterns : list
                :param conditionalTids : timestamps of repective conditional timestamps
                :type conditionalTids : list
                :support : the support of conditional pattern in tree
                :support : int
                """
    global minSup, maxPer
    pat = []
    tids = []
    sup = []
    data1 = {}
    count = {}
    for i in range(len(conditionalPatterns)):
        for j in conditionalPatterns[i]:
            if j in data1:
                data1[j] = data1[j] + conditionalTids[i]
                count[j] += support[i]
            else:
                data1[j] = conditionalTids[i]
                count[j] = support[i]
    up_dict = {}
    for m in data1:
        up_dict[m] = getPer_Sup(count[m], data1[m])
    up_dict = {k: v for k, v in up_dict.items() if v[0] >= minSup and v[1] <= maxPer}
    count = 0
    for p in conditionalPatterns:
        p1 = [v for v in p if v in up_dict]
        trans = sorted(p1, key= lambda x: (up_dict.get(x)[0]), reverse=True)
        if len(trans) > 0:
            pat.append(trans)
            tids.append(conditionalTids[count])
            sup.append(support[count])
        count += 1
    return pat, tids, sup, up_dict


class Ptubes():
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
            scanDatabse()
                Extracts the one-frequent patterns from transactions
            updateTransactions()
                update the transactions by removing aperiodic items and sort the transaction by item decreased support
            buildTree()
                after updating the transactions ar added into the tree by setting root node as null
            startMine()
                the main method to run the program



                """
    rank = {}
    startTime = float()
    endTime = float()
    minSup = float()
    maxPer = float()
    finalPatterns = {}
    iFile = " "
    oFile = " "
    memoryUSS = float()
    memoryRSS = float()
    Database = []

    def scanDatabase(self, transactions):
        """takes the transactions and calculates the support of each item in the dataset and assign the
                                    ranks to the items by decreasing support and returns the frequent items list

                                        :param transactions : it represents the one transactions in database
                                        :type transactions : list
                                        """
        global minSup, maxPer, rank, first, last
        mapSupport = {}
        n = 0
        for i in transactions:
            n = i[0]
            for j in i[1:]:
                if j.item not in mapSupport:
                    mapSupport[j.item] = [round(j.probability, 2), abs(first - n), n]
                else:
                    mapSupport[j.item][0] += round(j.probability, 2)
                    mapSupport[j.item][1] = max(mapSupport[j.item][1], abs(n - mapSupport[j.item][2]))
                    mapSupport[j.item][2] = n
        for key in mapSupport:
            mapSupport[key][1] = max(mapSupport[key][1], last - mapSupport[key][2])
        minSup = self.minSup
        maxPer = self.maxPer
        mapSupport = {k: [round(v[0], 2), v[1]] for k, v in mapSupport.items() if
                          v[1] <= maxPer and v[0] >= minSup}
        plist = [k for k, v in sorted(mapSupport.items(), key=lambda x: (x[1][0], x[0]), reverse=True)]
        self.rank = dict([(index, item) for (item, index) in enumerate(plist)])
        return mapSupport, plist

    def build_tree(self, data, info):
        """it takes the transactions and support of each item and construct the main tree with setting root
                                    node as null

                :param data : it represents the one transactions in database
                :type data : list
                :param info : it represents the support of each item
                :type info : dictionary
            """
        a = 0
        root_node = Tree()
        root_node.info = info.copy()
        for i in range(len(data)):
            set1 = []
            set1.append(data[i][0])
            q = root_node.add_transaction(data[i][1:], set1)
        return root_node, a

    def update_transactions1(self,list_of_transactions, dict1):
        """remove the items which are not frequent from transactions and updates the transactions with rank of items

                        :param list_of_transactions : it represents the transactions of database
                        :type list_of_transactions : list
                        :param dict1 : frequent items with support
                        :type dict1 : dictionary
                        """
        list1 = []
        for tr in list_of_transactions:
            list2 = [int(tr[0])]
            for i in range(1, len(tr)):
                if tr[i].item in dict1:
                    list2.append(tr[i])
            if (len(list2) >= 2):
                basket = list2[1:]
                basket.sort(key=lambda val: self.rank[val.item])
                list2[1:] = basket[0:]
                list1.append(list2)
        return list1

    def saveperiodic(self,itemset):
        t1 = []
        for i in itemset:
            t1.append(rankdup[i])
        return t1

    def Check(self, i, x):
        """To check the presence of item or pattern in transaction

                                        :param x: it represents the pattern
                                        :type x : list
                                        :param i : represents the uncertain transactions
                                        :type i : list
                                        """
        for m in x:
            k = 0
            for n in i:
                if m == n.item:
                    k += 1
            if k == 0:
                return 0
        return 1

    def startMine(self):
        """Main method where the patterns are mined by constructing tree and remove the remove the false patterns
                                   by counting the original support of a patterns


                       """
        global lno, first, last, minSup, maxPer
        self.startTime = int(round(time.time() * 1000))
        lno = 1
        first = 0
        last = 0
        transactions = []
        with open(self.iFile, 'r') as f:
            for line in f:
                l = line.split()
                if lno == 1:
                    first = int(l[0])
                tr = [int(l[0])]
                for i in l[1:]:
                    i1 = i.index('(')
                    i2 = i.index(')')
                    item = i[0:i1]
                    probability = float(i[i1 + 1:i2])
                    product = Item(item, probability)
                    tr.append(product)
                lno += 1
                transactions.append(tr)
                last = int(l[0])
        mapSupport, plist = self.scanDatabase(transactions)
        transactions1 = self.update_transactions1(transactions, mapSupport)
        info = {k: v for k, v in mapSupport.items()}
        Tree1, nodescount = self.build_tree(transactions1, info)
        n = Tree1.generate_patterns([])
        count = 0
        count1 = 0
        for x in n:
            s = str(x)
            count1 += 1
        print("total itemsets:", count1)
        periods = {}
        for i in transactions:
            for x, y in periodic.items():
                l = []
                s = 1
                if len(x) == 1:
                    periods[x] = y[0]
                else:
                    check = self.Check(i[1:], x)
                    if check == 1:
                        for j in i[1:]:
                            if j.item in x:
                                s *= j.probability
                        if x in periods:
                            periods[x] += s
                        else:
                            periods[x] = s
        for x, y in periods.items():
            if y >= minSup:
                self.finalPatterns[tuple(x)] = y
        print("Frequent patterns were generated successfully using frequentPatternGrowth algorithm")
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

        dataframe = {}
        data = []
        for a, b in self.finalPatterns.items():
            data.append([a, b])
            dataframe = pd.DataFrame(data, columns=['Patterns', 'Support'])
        return dataframe

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


if __name__ == "__main__":
    ap = Ptubes()
    ap.iFile = sys.argv[1]
    ap.oFile = sys.argv[2]
    ap.minSup = float(sys.argv[3])
    ap.maxPer = float(sys.argv[4])
    ap.startMine()
    frequentPatterns = ap.getFrequentPatterns()
    print("Total number of Frequent Patterns:", len(frequentPatterns))
    ap.storePatternsInFile(sys.argv[2])
    memUSS = ap.getMemoryUSS()
    print("Total Memory in USS:", memUSS)
    memRSS = ap.getMemoryRSS()
    print("Total Memory in RSS", memRSS)
    run = ap.getRuntime()

