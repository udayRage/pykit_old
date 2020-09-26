import sys
import time
import resource
import math
path=sys.argv[1]
output=sys.argv[2]
minsup=float(sys.argv[3])
maxperiod=int(sys.argv[4])
tidlist={}
hashing={}
lno=0
def getPer_Sup(tids):
	tids.sort()
	cur=0
    	per=0
   	sup=0
    	for j in range(len(tids)):
        	per=max(per,tids[j]-cur)
        	if(per>maxperiod):
        		break
            		return [0,0]
        	cur=tids[j]
        	sup+=1
    	per=max(per,lno-cur)
    	return [sup,per]
class charm():
	def __init__(self):
		self.mapSupport={}
		self.hashing={}
		self.itemsetCount=0
		self.maxItemId=0
		self.tablesize=10000
		self.writer=None
		self.minSup=0
	def scanDatabase(self,path):
		global lno,tidlist,maxperiod
		id1=0
		with open(path,'r') as f:
			for line in f:
				lno+=1
				s=line.split()
				n=lno
				for i in range(0,len(s)):
					si=s[i]
					if(si>id1):
						id1=si
					if(self.mapSupport.get(si)==None):
						self.mapSupport[si]=[1,abs(0-n),n]
						tidlist[si]=[n]
					else:
						self.mapSupport[si][0]+=1
						self.mapSupport[si][1]=max(self.mapSupport[si][1],abs(n-self.mapSupport[si][2]))
						self.mapSupport[si][2]=n
						tidlist[si].append(n)
		self.minSup=int(math.ceil(minsup*lno)/100)
		maxperiod=int(math.ceil(maxperiod*lno)/100)
		print(self.minSup,maxperiod)
		self.mapSupport={k: [v[0],v[1]] for k,v in self.mapSupport.items() if v[0]>=self.minSup and v[1]<=maxperiod}
		#plist=[key for key,value in sorted(self.mapSupport.items(), key=lambda x:x[1])]
		plist={}
		tidlist={k:v for k,v in tidlist.items() if k in self.mapSupport}
		for x,y in tidlist.items():
			t1=0
			for i in y:
				t1+=i
			plist[x]=t1
		plist=[key for key,value in sorted(plist.items(), key=lambda x:x[1])]
		#print(plist)
		return id1,plist
							
	def calculate(self,tidset,tablesize):
		hashcode=0
		for i in tidset:
			hashcode+=i	
		if hashcode<0:
			hashcode=abs(0-hashcode)
		#print(hashcode%tablesize)
		return hashcode%tablesize
	def contains(self,itemset,val,hashcode):
		if(hashing.get(hashcode)==None):
			return False
		for i in hashing[hashcode]:
			itemsetx=i
			if val[0]==hashing[hashcode][itemsetx][0]and set(itemsetx).issuperset(itemset) and val[1]!=hashing[hashcode][itemsetx][1]:
				return True
		return False
	def save(self,prefix,suffix,tidsetx):
		if(prefix==None):
			prefix=suffix
		else:
			prefix=prefix+suffix
		prefix=list(set(prefix))
		prefix.sort()
		val=getPer_Sup(tidsetx)
		#print(prefix,val)
		if(val[0]>=self.minSup and val[1]<=maxperiod):
			hashcode=self.calculate(tidsetx,self.tablesize)
			if self.contains(prefix,val,hashcode)==False:
				self.itemsetCount+=1
				x=str(prefix)+" : "+str(val)
				self.writer.write('%s \n'%x)
				#print(prefix,val)
			if hashcode not in hashing:
				hashing[hashcode]={tuple(prefix):val}
			else:
				hashing[hashcode][tuple(prefix)]=val
	def processEquivalenceClass(self,prefix,itemsets,tidsets):
		if(len(itemsets)==1):
			i=itemsets[0]
			tidi=tidsets[0]
			self.save(prefix,[i],tidi)
			return
		if(len(itemsets)==2):
			itemi=itemsets[0]
			tidseti=tidsets[0]
			itemj=itemsets[1]
			tidsetj=tidsets[1]
			y1=list(set(tidseti).intersection(tidsetj))
			if(len(y1)>=self.minSup):
				suffixij=[]
				suffixij+=[itemi,itemj]
				suffixij=list(set(suffixij))
				self.save(prefix,suffixij,y1)
			if len(y1)!=len(tidseti):
				self.save(prefix,[itemi],tidseti)
			if len(y1)!=len(tidsetj):
				self.save(prefix,[itemj],tidsetj)
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
				if(itemj==None):	
					continue
				tidsetj=tidsets[j]
				y=list(set(tidsetx).intersection(tidsetj))
				#print(tidsetx,tidsetj,y)
				if(len(y)<self.minSup):
					continue
				if len(tidsetx)==len(tidsetj) and len(y)==len(tidsetx):
					itemsets.insert(j,None)
					tidsets.insert(j,None)
					itemsetx+=itemj
				elif len(tidsetx)<len(tidsetj) and len(y)==len(tidsetx):
					itemsetx+=itemj
				elif len(tidsetx)>len(tidsetj) and len(y)==len(tidsetj):
					itemsets.insert(j,None)
					tidsets.insert(j,None)
					classItemsets.append(itemj)
					classtidsets.append(y)
				else:
					classItemsets.append(itemj)
					classtidsets.append(y)
			if(len(classItemsets)>0):
				newprefix=list(set(itemsetx))+prefix
				self.processEquivalenceClass(newprefix, classItemsets,classtidsets)
			self.save(prefix,list(set(itemsetx)),tidsetx)
		
	def runAlgorithm(self,path,output,minsup,maxperiod):
		self.writer=open(output,'w')
		starttime=int(round(time.time()*1000))
		self.maxItemId,plist=self.scanDatabase(path)
		#print(plist)
		#for x,y in tidlist.items():
			#print(x,y)
		'''for x,y in self.mapSupport.items():
			print(x,y)'''
		for i in range(len(plist)):
			itemx=plist[i]
			if itemx==None:
				continue
			tidsetx=tidlist[itemx]
			itemsetx=[itemx]
			itemsets=[]
			tidsets=[]
			#self.saveperiodicFrequent(itemx,val)
			for j in range(i+1,len(plist)):
				itemj=plist[j]
				if(itemj==None):
					continue
				tidsetj=tidlist[itemj]
				y1=list(set(tidsetx).intersection(tidsetj))
				if(len(y1)<self.minSup):
					continue
				if len(tidsetx)==len(tidsetj) and len(y1)==len(tidsetx):
					plist.insert(j,None)
					itemsetx+=itemj
				elif len(tidsetx)<len(tidsetj) and len(y1)==len(tidsetx):
					itemsetx+=itemj
				elif len(tidsetx)>len(tidsetj) and len(y1)==len(tidsetj):
					plist.insert(j,None)
					itemsets.append(itemj)
					tidsets.append(y1)
				else:
					itemsets.append(itemj)
					tidsets.append(y1)
			if(len(itemsets)>0):
				self.processEquivalenceClass(itemsetx,itemsets,tidsets)
			self.save(None,itemsetx,tidsetx)
		'''for x,y in hashing.items():
			print(x,y)'''
		print("Total Itemsets:",self.itemsetCount)
		endtime=int(round(time.time()*1000))
		temp=(endtime-starttime)
		print("Time taken:",temp ,":ms")
		print("MemorySpace",resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)			
				
					
ch=charm()
ch.runAlgorithm(path,output,minsup,maxperiod)
