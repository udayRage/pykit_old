import sys
import time
import resource
import os
import psutil
from collections import defaultdict
iFile=sys.argv[1]
oFile=sys.argv[2]
minSup=int(sys.argv[3])
class Eclat():
    def __init__(self,data,output,minSup):
        self.data=data
        self.minSup=minSup
        self.tidList={}
        self.lno=0
        self.totalItemsets={}
        self.writer = open(output, 'w+')
    def createItemsets(self):
        with open(self.data,'r')as f:
            for line in f:
                l=line.split()
                for i in range(1,len(l)):
                    if l[i] in self.tidList:
                        self.tidList[l[i]].append(int(l[0]))
                    else:
                        self.tidList[l[i]]=[int(l[0])]
        self.tidList={k:v for k,v in self.tidList.items() if len(v)>=self.minSup}
        for x,y in self.tidList.items():
            self.totalItemsets[x]=len(y)
    def generate2Length_FrequentPatterns(self,tids): 
         tidList1={}
         x=list(tids.keys())
         for i in range(0,len(x)):
             for j in range(i+1,len(x)):
                 k=list(set(tids[x[i]]).intersection(set(tids[x[j]])))
                 l=[]
                 if(len(k)>=self.minSup):
                     l+=x[i],x[j]
                     l.sort()
                     tidList1[tuple(l)]=k
         return tidList1
         

    def generateAllFrequentPatterns(self,itemsets):
        tidList1={}
        x=list(itemsets.keys())
        for i in range(0,len(x)):
            for j in range(i+1,len(x)):
                k=list(set(itemsets[x[i]]).intersection(set(itemsets[x[j]])))
                l=[]
                l+=x[i]
                l+=x[j]
                if(len(k)>=self.minSup):
                    l.sort()
                    if tuple(l) not in tidList1:
                        tidList1[tuple(set(l))]=k
        return tidList1
    def startMine(self):
        startTime=time.time()
        self.createItemsets()
        #To generate 2-length itemsets
        patterns=self.generate2Length_FrequentPatterns(self.tidList)
        for x,y in patterns.items():
            if x not in self.totalItemsets:
                self.totalItemsets[x]=len(y)
        while(1):
            # to generate all patterns recursively
            patterns=self.generateAllFrequentPatterns(patterns)
            for x,y in patterns.items():
                if x not in self.totalItemsets:
                    self.totalItemsets[x]=len(y)
            if(len(patterns)==0):
                break
        for x,y in self.totalItemsets.items():
            s=str(x)+":"+str(y)
            self.writer.write("%s \n" %s)
        endTime=time.time()
        print("total itemsets:",len(self.totalItemsets))
        print("time:",endTime-startTime ,":(in Sec)")
        process = psutil.Process(os.getpid())
        memory = process.memory_full_info().uss
        memory_in_MB = memory / (1024 * 1024)
        print("Memory Space:",memory_in_MB ,":(in MBs)")
        
        
e=Eclat(iFile,oFile,minSup)
e.startMine()
