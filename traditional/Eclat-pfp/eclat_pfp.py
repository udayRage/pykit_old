import sys
from abstractP import *


class Eclatpfp():
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
        scanDatabase()
            Scan the database and store the items with their timestamps which are periodic frequent 
        getPeriodAndSupport()
            Calculates the support and period for a list of timestamps.
        Generation()
            Used to implement prefix class equivalence method to generate the periodic patterns recursively
        startMine()
            Main program
        
        


        """
    startTime = float()
    endTime = float()
    finalPatterns = {}
    iFile = " "
    oFile = " "
    memoryUSS = float()
    memoryRSS = float()
    mapSupport = {}
    hashing = {}
    itemsetCount = 0
    writer = None
    minSup = float()
    maxPer = float()
    tidlist = {}
    lno = 0

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
            per = max(per, tids[j] - cur)
            if (per > self.maxPer):
                return [0, 0]
            cur = tids[j]
            sup += 1
        per = max(per, self.lno - cur)
        return [sup, per]
        
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

    def scanDatabase(self):
        """
                    Storing the complete transactions of the database/input file in a database variable

                    :param self.iFile: user given input file/input file path
                    :type self.iFile: str


                    """
        delimiter = str()
        with open(self.iFile, 'r') as f:
            for line in f:
                self.lno+=1
                if self.lno==1:
                    delimiter = self.findDelimiter([*line])
                s=[i.strip(delimiter) for i in line.split(delimiter)]
                n=self.lno
                for i in range(1,len(s)):
                    si=s[i]
                    if(self.mapSupport.get(si)==None):
                        self.mapSupport[si]=[1,abs(0-n),n]
                        self.tidlist[si]=[n]
                    else:
                        self.mapSupport[si][0]+=1
                        self.mapSupport[si][1]=max(self.mapSupport[si][1],abs(n-self.mapSupport[si][2]))
                        self.mapSupport[si][2]=n
                        self.tidlist[si].append(n)
        for x,y in self.mapSupport.items():
            self.mapSupport[x][1]=max(self.mapSupport[x][1],abs(self.lno-self.mapSupport[x][2]))
        self.minSup=(self.minSup*self.lno)
        self.maxPer=(self.maxPer*self.lno)
        print(self.minSup,self.maxPer)
        self.mapSupport={k: [v[0],v[1]] for k,v in self.mapSupport.items() if v[0]>=self.minSup and v[1]<=self.maxPer}
        plist=[key for key,value in sorted(self.mapSupport.items(), key=lambda x:(x[1][0],x[0]),reverse=True)]
        return plist
    def save(self,prefix,suffix,tidsetx):
         """
            saves the patterns that satisfy the periodic frequent property.

            :param prefix: the prefix of a pattern
            :type prefix: list
            :param suffix : the suffix of a patterns
            :type suffix : list
            :param tidSetx : the timestamp of a patterns
            :type tidSetx : list


                    """
         if(prefix==None):
             prefix=suffix
         else:
             prefix=prefix+suffix
         val=self.getSupportAndPeriod(tidsetx)
         if val[0]>=self.minSup and val[1]<=self.maxPer:
             self.finalPatterns[tuple(prefix)] = val
    def Generation(self,prefix,itemsets,tidsets):
        """
            here equivalence class is followed  and checks for the patterns generated for periodic frequent patterns.

            :param prefix :  main equivalence prefix
            :type prefix : periodic-frequent item or pattern
            :param itemSets : patterns which are items combined with prefix and satisfying the periodicity
                            and frequent with their timestamps
            :type itemSets : list
            :param tidSets : timestamps of the items in the argument itemSets
            :type tidSets : list


                    """
        if(len(itemsets)==1):
            i=itemsets[0]
            tidi=tidsets[0]
            self.save(prefix,[i],tidi)
            return
        for i in range(len(itemsets)):
            itemx=itemsets[i]
            if(itemx==None):
                continue
            tidsetx=tidsets[i]
            classItemsets=[]
            classtidsets=[]
            itemsetx=[itemx]
            for j in range(i+1,len(itemsets)):
                itemj=itemsets[j]
                tidsetj=tidsets[j]
                y=list(set(tidsetx).intersection(tidsetj))
                if(len(y)>=self.minSup):
                    classItemsets.append(itemj)
                    classtidsets.append(y)
            newprefix=list(set(itemsetx))+prefix
            self.Generation(newprefix, classItemsets,classtidsets)
            self.save(prefix,list(set(itemsetx)),tidsetx)
        
    def startMine(self):
        """
                Main program start with extracting the periodic frequent items from the database and
                performs prefix equivalence to form the combinations and generates closed periodic frequent patterns.


                    """
        self.startTime=time.time()
        plist=self.scanDatabase()
        for i in range(len(plist)):
            itemx=plist[i]
            tidsetx=self.tidlist[itemx]
            itemsetx=[itemx]
            itemsets=[]
            tidsets=[]
            for j in range(i+1,len(plist)):
                itemj=plist[j]
                tidsetj=self.tidlist[itemj]
                y1=list(set(tidsetx).intersection(tidsetj))
                if(len(y1)>=self.minSup):
                    itemsets.append(itemj)
                    tidsets.append(y1)
            self.Generation(itemsetx,itemsets,tidsets)
            self.save(None,itemsetx,tidsetx)
        print("Periodic Frequent patterns were generated successfully using eclat_pfp algorithm")
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
    ap = Eclatpfp()
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

