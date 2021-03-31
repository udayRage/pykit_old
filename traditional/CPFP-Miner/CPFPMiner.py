import sys
from traditional.abstractClass.abstractPeriodicPatterns import *


class CPFPMiner():
    
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
        tidList : dict
            stores the timestamps of an item
        hashing : dict
            stores the patterns with their support to check for the closed property

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
        creatingItemsets()
            Stores the periodic frequent items with their timestamps from the dataset
        getSupportAndperiod()
            Calculates the support and period with help of timestamps
        
            
        


        """
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
    tidList = {}
    lno = 0
    mapSupport = {}
    hashing = {}
    itemSetCount = 0
    maxItemId = 0
    tableSize = 10000
    writer = None

    def creatingItemsets(self):
        """
                    Storing the complete the periodic frequent items of the database/input file in a database variable

                    :param self.iFile: user given input file/input file path
                    :type self.iFile: str


                    """
        with open(self.iFile, 'r') as f:
            for line in f:
                i = line.split()
                n = int(i[0])
                self.lno += 1
                for j in i[1:]:    
                    if j not in self.mapSupport:
                        self.mapSupport[j] = [1, abs(0-n), n]
                        self.tidList[j] = [n]
                    else:
                        self.mapSupport[j][0] += 1
                        self.mapSupport[j][1] = max(self.mapSupport[j][1], abs(n-self.mapSupport[j][2]))
                        self.mapSupport[j][2] = n
                        self.tidList[j].append(n)
        for key in self.mapSupport:
            self.mapSupport[key][0] = max(self.mapSupport[key][0], self.lno - self.mapSupport[key][1])
        self.minSup = (self.minSup*self.lno)
        self.maxPer = (self.maxPer*self.lno)
        print("minSup and periodicity:", self.minSup, self.maxPer)
        self.mapSupport = {k: [v[0], v[1]] for k, v in self.mapSupport.items() if v[0] >= self.minSup and v[1] <= self.maxPer}
        plist = {}
        self.tidList = {k: v for k, v in self.tidList.items() if k in self.mapSupport}
        for x, y in self.tidList.items():
            t1 = 0
            for i in y:
                t1 += i
            plist[x] = t1
        plist = [key for key, value in sorted(plist.items(), key=lambda x:x[1])]
        return plist
    
    def getSupportAndPeriod(self, tids):
        """
            calculates the support and periodicity with list of timestamps

            :param tids : timestamps of a pattern
            :type tids : list


                    """
        tids.sort()
        cur = 0
        per = 0
        sup = 0
        for j in range(len(tids)):
            per = max(per, tids[j]-cur)
            if per > self.maxPer:
                return [0, 0]
            cur = tids[j]
            sup += 1
        per = max(per, self.lno-cur)
        return [sup, per]

    def calculate(self, tidSet):
        """
            to calculate the hashcode of pattern

            :param tidSet : the timestamps of a pattern
            :type tidSet : list


                    """
        hashcode = 0
        for i in tidSet:
            hashcode += i
        if hashcode < 0:
            hashcode = abs(0-hashcode)
        return hashcode % self.tableSize

    def contains(self, itemSet, value, hashcode):
        """
            checks for closed property(patterns with same support) by checking the hashcode(sum of timestamps).
            If hashcode key in hashing dict is none returns with false  otherwise returns with true.

            :param itemSet: periodic-frequent pattern
            :type itemSet: list
            :param value : support and periodicity of the pattern
            :type value : list
            :param hashcode : calculated from the timestamps of pattern
            :type hashcode : int


                    """
        if self.hashing.get(hashcode) is None:
            return False
        for i in self.hashing[hashcode]:
            itemSetx = i
            if value[0] == self.hashing[hashcode][itemSetx][0] and set(itemSetx).issuperset(itemSet) and value[1] != self.hashing[hashcode][itemSetx][1]:
                return True
        return False

    def save(self, prefix, suffix, tidSetx):
        """
            checks for the closed property(patterns with same support). if found deletes the subsets and stores
            supersets and saves the patterns that satisfy the closed periodic.

            :param prefix: the prefix of a pattern
            :type prefix: list
            :param suffix : the suffix of a patterns
            :type suffix : list
            :param tidSetx : the timestamp of a patterns
            :type tidSetx : list


                    """
        if prefix is None:
            prefix = suffix
        else:
            prefix = prefix+suffix
        prefix = list(set(prefix))
        prefix.sort()
        val = self.getSupportAndPeriod(tidSetx)
        if val[0] >= self.minSup and val[1] <= self.maxPer:
            hashcode = self.calculate(tidSetx)
            if self.contains(prefix, val, hashcode) is False:
                self.itemSetCount += 1
                self.finalPatterns[tuple(prefix)] = val
            if hashcode not in self.hashing:
                self.hashing[hashcode] = {tuple(prefix): val}
            else:
                self.hashing[hashcode][tuple(prefix)] = val

    def processEquivalenceClass(self, prefix, itemSets, tidSets):
        """
            here equivalence class is followed  and checks for the patterns satisfies periodic frequent properties.

            :param prefix :  main equivalence prefix
            :type prefix : periodic-frequent item or pattern
            :param itemSets : patterns which are items combined with prefix and satisfying the periodicity
                            and frequent with their timestamps
            :type itemSets : list
            :param tidSets : timestamps of the items in the argument itemSets
            :type tidSets : list


                    """
        if len(itemSets) == 1:
            i = itemSets[0]
            tidI = tidSets[0]
            self.save(prefix, [i], tidI)
            return
        if len(itemSets) == 2:
            itemX = itemSets[0]
            tidSetX = tidSets[0]
            itemY = itemSets[1]
            tidSetY = tidSets[1]
            y1 = list(set(tidSetX).intersection(tidSetY))
            if len(y1) >= self.minSup:
                suffix = []
                suffix += [itemX, itemY]
                suffix = list(set(suffix))
                self.save(prefix, suffix, y1)
            if len(y1) != len(tidSetX):
                self.save(prefix, [itemX], tidSetX)
            if len(y1) != len(tidSetY):
                self.save(prefix, [itemX], tidSetY)
            return
        for i in range(len(itemSets)):
            itemX = itemSets[i]
            if itemX is None:
                continue
            tidSetX = tidSets[i]
            classItemSets = []
            classTidSets = []
            itemSetx = [itemX]
            for j in range(i+1, len(itemSets)):
                itemY = itemSets[j]
                if itemY is None:
                    continue
                tidSetY = tidSets[j]
                y = list(set(tidSetX).intersection(tidSetY))
                if len(y) < self.minSup:
                    continue
                if len(tidSetX) == len(tidSetY) and len(y) == len(tidSetX):
                    itemSets.insert(j, None)
                    tidSets.insert(j, None)
                    itemSetx.append(itemY)
                elif len(tidSetX) < len(tidSetY) and len(y) == len(tidSetX):
                    itemSetx.append(itemY)
                elif len(tidSetX) > len(tidSetY) and len(y) == len(tidSetY):
                    itemSets.insert(j, None)
                    tidSets.insert(j, None)
                    classItemSets.append(itemY)
                    classTidSets.append(y)
                else:
                    classItemSets.append(itemY)
                    classTidSets.append(y)
            if len(classItemSets) > 0 :
                newPrefix = list(set(itemSetx))+prefix
                self.processEquivalenceClass(newPrefix, classItemSets, classTidSets)
                self.save(prefix, list(set(itemSetx)), tidSetX)
        
    def startMine(self):
        """
                Main program start with extracting the periodic frequent items from the database and
                performs prefix equivalence to form the combinations and generates closed periodic frequent patterns.


                    """
        self.startTime = time.time()
        plist = self.creatingItemsets()
        for i in range(len(plist)):
            itemX = plist[i]
            if itemX is None:
                continue
            tidSetx = self.tidList[itemX]
            itemSetx = [itemX]
            itemSets = []
            tidSets = []
            for j in range(i+1, len(plist)):
                itemY = plist[j]
                if itemY is None:
                    continue
                tidSetY = self.tidList[itemY]
                y1 = list(set(tidSetx).intersection(tidSetY))
                if len(y1) < self.minSup:
                    continue
                if len(tidSetx) == len(tidSetY) and len(y1) == len(tidSetx):
                    plist.insert(j, None)
                    itemSetx.append(itemY)
                elif len(tidSetx) < len(tidSetY) and len(y1) == len(tidSetx):
                    itemSetx.append(itemY)
                elif len(tidSetx) > len(tidSetY) and len(y1) == len(tidSetY):
                    plist.insert(j, None)
                    itemSets.append(itemY)
                    tidSets.append(y1)
                else:
                    itemSets.append(itemY)
                    tidSets.append(y1)
            if len(itemSets) > 0:
                self.processEquivalenceClass(itemSetx, itemSets, tidSets)
            self.save(None, itemSetx, tidSetx)
        print("Closed PeriodicFrequent patterns were generated successfully using CPFP-Miner algorithm")
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
    ap = CPFPMiner()
    ap.iFile = sys.argv[1]
    ap.oFile = sys.argv[2]
    ap.maxPer = float(sys.argv[4])
    ap.minSup = float(sys.argv[3])
    ap.startMine()
    frequentPatterns = ap.getFrequentPatterns()
    print("Total number of Frequent Patterns:", len(frequentPatterns))
    ap.storePatternsInFile(sys.argv[2])
    memUSS = ap.getMemoryUSS()
    print("Total Memory in USS:", memUSS)
    memRSS = ap.getMemoryRSS()
    print("Total Memory in RSS", memRSS)
    run = ap.getRuntime()
    print("Total ExecutionTime in seconds:", run)
