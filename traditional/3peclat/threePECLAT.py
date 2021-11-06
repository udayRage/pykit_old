import sys
import time
import resource
import math
import os
import resource
import csv

path=sys.argv[1]
outFile = sys.argv[2]
maxPeriod=float(sys.argv[3])
minPS=float(sys.argv[4])



class EclatPfp:
    startTime = float()
    endTime = float()
    finalPatterns = {}
    memoryRSS = float()
    tidList = {}
    PS = []
    Per = []


    def findPer(self,list):
        a = 0
        for i in list:
            if i > a:
                a = i
        return a

    def getPS(self,tidS):
        tidS.sort()
        count = 0
        a = []
        for k in range(len(tidS) - 1):
            ps = tidS[k + 1] - tidS[k]
            a.append(ps)
            if ps <= maxPeriod1:
                count += 1
        return [count, a]

    def scanDataBase(self, file):
        global minPS1, maxPeriod1, lNo
        with open(file) as f:
            read = csv.reader(f)
            listOfRead = list(read)
            listOfRead1=[]
            count = 0
            for i in listOfRead:
                    listOfRead1.append(i[0].split())
            lNo = len(listOfRead1)
            minPS1 = int(math.ceil(minPS * lNo) / 100)
            maxPeriod1 = int(math.ceil(maxPeriod * lNo) / 100)
            Lis1 = []
            for i in listOfRead1:
                Lis1.append(i)
            for i in range(len(Lis1)):
                s = Lis1[i]
                n = int(s[0])
                for j in range(1, len(s)):
                    si = s[j]
                    if self.tidList.get(si) is None:
                        self.tidList[si] = [n]
                    else:
                        self.tidList[si].append(n)
        plist = [key for key, value in sorted(self.tidList.items()) if self.getPS(self.tidList[key])[0]>=minPS1]
        return plist

    def save(self, prefix, suffix, tidSetX):
        if prefix is None:
            prefix = suffix
        else:
            prefix = prefix + suffix
        self.finalPatterns[str(prefix)]=[self.getPS(tidSetX)[0]]
        EclatPfp.PS.append(self.getPS(tidSetX)[0])
        b = self.findPer(self.getPS(tidSetX)[1])
        EclatPfp.Per.append(b)

    def Generation(self, prefix, itemSets, tidSets):
        if len(itemSets) == 1:
            i = itemSets[0]
            tidI = tidSets[0]
            self.save(prefix, [i], tidI)
            return
        for i in range(len(itemSets)):
            itemX = itemSets[i]
            if itemX is None:
                continue
            tidSetX = tidSets[i]
            classItemSets = []
            classTidSets = []
            itemSetX = [itemX]
            for j in range(i + 1, len(itemSets)):
                itemJ = itemSets[j]
                tidSetJ = tidSets[j]
                y = list(set(tidSetX).intersection(tidSetJ))
                if self.getPS(y)[0] >= minPS1:
                    classItemSets.append(itemJ)
                    classTidSets.append(y)
            newPrefix = list(set(itemSetX)) + prefix
            self.Generation(newPrefix, classItemSets, classTidSets)
            self.save(prefix, list(set(itemSetX)), tidSetX)

    def startMine(self):
        self.startTime = int(round(time.time()*1000))
        plist = self.scanDataBase(path)
        for i in range(len(plist)):
            itemX = plist[i]
            tidSetX = self.tidList[itemX]
            itemSetX = [itemX]
            itemSets = []
            tidSets = []
            for j in range(i + 1, len(plist)):
                itemJ = plist[j]
                tidSetJ = self.tidList[itemJ]
                y1 = list(set(tidSetX).intersection(tidSetJ))
                if self.getPS(y1)[0] >= minPS1:
                    itemSets.append(itemJ)
                    tidSets.append(y1)
            self.Generation(itemSetX, itemSets, tidSets)
            self.save(None, itemSetX, tidSetX)
        self.endTime = int(round(time.time()*1000))
        with open(outFile, 'w') as f:
            c = 0
            for i in self.finalPatterns:
                f.write(i)
                f.write('\n')
        print("MinimumPeriodicSupport = {}".format(minPS1))
        print("MaximumPeriodicity = {}".format(maxPeriod1))
        print("partial periodic patterns {} ".format(len(self.finalPatterns.keys())))
        print("Time is {} ".format(self.endTime - self.startTime))
        print("Memory Space is {}".format(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss))

EclatPfp().startMine()

