import sys
from array import *
import datetime
import resource
import time
import os
import os.path
import psutil
import functools
class FFList:
	"""
	 A class represent a Fuzzy List of an element

	 	Attributes
	 	----------
	 	item: int
	 		the item name
	 	sumIutil: float
	 		the sum of utilities of an fuzzy item in database
	 	sumRutil: float
	 		the sum of resting values of a fuzzy item in database
	 	elements: list
	 		a list of elements contain tid,Utility and resting values of element in each transaction
		Methods
		-------
		addElement(element)
			Method to add an element to this fuzzy list and update the sums at the same time.

		printelement(e)
			Method to print elements			

	"""
	def __init__(self,itemName):
		self.item=itemName
		self.sumIutil=0.0
		self.sumRutil=0.0
		self.elements=[]
	
	def addElement(self,element):
		self.sumIutil+=element.iutils
		self.sumRutil+=element.rutils
		self.elements.append(element);
	def printelement(self):
		for ele in self.elements:
			print(ele.tid,ele.iutils,ele.rutils)

class Element:
	"""
		A class represents an Element of a fuzzy list
		Attributes
		----------
		tid : int
			keep tact of transaction id
		iutils: float
			the utility of an fuzzy item in the transaction
		rutils : float
			the nighbourhood resting value of an fuzzy item in the transaction
	"""
	def __init__(self,tid,iutil,rutil):
		self.tid=tid
		self.iutils=iutil
		self.rutils=rutil
class Reagions:
		"""
			A class caluculate the regions
			Attributes
			----------
			low : int
				low region value
			middle: int 
				middle region value
			high : int
				high region values
		"""
		def __init__(self,quantity,regionsNumber):
			self.low=0 
			self.middle=0
			self.high=0 
			if(regionsNumber==3): #if we have 3 regions
				if(quantity>0 and quantity<=50):
					self.low=1
					self.high=0
					self.middle=0
				elif(quantity>=50 and quantity<300):
					self.low=(float)((-0.2 * quantity)+1.2)
					self.middle=(float)((0.2*quantity)-0.2)
					self.high=0;
				elif(quantity>=300 and quantity<=2000):
					self.low=0;
					self.middle=(float)((-0.2*quantity)+2.2)
					self.high=(float)((0.2*quantity)-1.2)
				else:
					self.low=0;
					self.middle=0;
					self.high=1;
class Pair:
	def __init__(self):
		self.item=0
		self.quantity=0

class AlgoFFSHUIM:
	"""
        Parameters
        ----------
        self.iFile : file
            Name of the input file to mine complete set of fuzzy spatial frequent patterns
       	self. oFile : file
           	Name of the oFile file to store complete set of fuzzy spatial frequent patterns
    	minSup1 : int
            The user given support
        neighbors: map
			keep track of nighboues of elements
        memoryRSS : float
            	To store the total amount of RSS memory consumed by the program
        startTime:float
           	To record the start time of the mining process
        endTime:float
	        To record the completion time of the mining process
        itemsCnt: int
			To record the number of fuzzy spatial itemsets generated
		mapItemsLowSum: map
			To keep track of low region values of items
		mapItemsMidSum: map
			To keep track of middle region values of items
		mapItemsHighSum: map
			To keep track of high region values of items
		mapItemSum: map
			To keep track of sum of Fuzzy Vlues of items
		mapItemRegions: map
			To Kepp track of fuzzy regions of item
		jointCnt: int
			To keep track of the number of FFI-list that was constructed
		BufferSize: int
			represent the size of Buffer
		itemBuffer list
			to kepp track of items in buffer
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

	"""
	def __init__(self,iFile,nFile,oFile,minsup):
		self.startTime=0
		self.endTime=0
		self.itemsCnt=0 
		self.mapItemsLowSum={}
		self.mapItemsMidSum={}
		self.mapItemsHighSum={}			
		self.mapItemSum={}
		self.mapItemRegions={}
		self.joinsCnt=0 
		self.BufferSize=200
		self.itemsetBuffer=[]
		self.minSup=minsup
		self.iFile=iFile
		self.oFile=oFile
		self.nighb=nFile
	def compareItems(self,o1,o2):
		"""
			A Function that sort all FFI-list in asendng order of Support
		"""
		compare=self.mapItemSum[o1.item]-self.mapItemSum[o2.item]
		if(compare==0):
			return o1.item-o2.item
		else:
			return compare
	def startMine(self):
		""" Frequent pattern mining process will start from here        	
		"""
		self.startTime=datetime.datetime.now();
		self.bwriter=open(self.oFile,'w')
		self.mapItemNighbours={}
		minSup=self.minSup
		with open(self.nighb,'r') as file1:
			for line in file1:
				parts=line.split()
				item=int(parts[0])
				neigh1=[]
				for i in range(1,len(parts)):
					neigh1.append(int(parts[i]))
				self.mapItemNighbours[item]=neigh1;
		with open(self.iFile,'r') as file:
			for line in file:
				parts=line.split(":")
				items=parts[0].split();
				quanaities=parts[2].split();
				for i in range(0,len(items)):
					regions=Reagions(int(quanaities[i]),3);
					item=int(items[i]);
					if(item in self.mapItemsLowSum.keys()):
						low=self.mapItemsLowSum[item]
						low+=regions.low
						self.mapItemsLowSum[item]=low
					else:
						self.mapItemsLowSum[item]=regions.low
					if(item in self.mapItemsMidSum.keys()):
						mid=self.mapItemsMidSum[item]
						mid+=regions.middle
						self.mapItemsMidSum[item]=mid
					else:
						self.mapItemsMidSum[item]=regions.middle
					if(item in self.mapItemsHighSum.keys()):
						high=self.mapItemsHighSum[item]
						high+=regions.high
						self.mapItemsHighSum[item]=high
					else:
						self.mapItemsHighSum[item]=regions.high
			listOfFFIlist=[]
			mapItemsToFFLIST={}
			for item1 in self.mapItemsLowSum.keys():
				item=int(item1)
				low=self.mapItemsLowSum[item]
				mid=self.mapItemsMidSum[item]
				high=self.mapItemsHighSum[item]
				if(low>=mid and low>=high):
					self.mapItemSum[item]=low
					self.mapItemRegions[item]="L"
				elif(mid>=low and mid>=high):
					self.mapItemSum[item]=mid
					self.mapItemRegions[item]="M"
				elif(high>=low and high>=mid):
					self.mapItemRegions[item]="H"
					self.mapItemSum[item]=high
				if(self.mapItemSum[item]>=self.minSup):
					fuList=FFList(item)
					mapItemsToFFLIST[item]=fuList;
					listOfFFIlist.append(fuList)
			listOfFFIlist.sort(key=functools.cmp_to_key(self.compareItems))
		tid=0;
		with open(self.iFile,'r') as file:
			for line in file:
				parts=line.split(":")
				items=parts[0].split();
				quanaities=parts[2].split();
				revisedTransaction=[]
				for i in range(0,len(items)):
					pair=Pair();
					pair.item=int(items[i])
					regions=Reagions(int(quanaities[i]),3)
					item=pair.item
					if(self.mapItemSum[item]>=minSup):
						if(self.mapItemRegions[pair.item]=="L"):
							pair.quantity=regions.low
						elif(self.mapItemRegions[pair.item]=="M"):
							pair.quantity=regions.middle
						elif(self.mapItemRegions[pair.item]=="H"):
							pair.quantity=regions.high
						if(pair.quantity>0):
							revisedTransaction.append(pair)
				revisedTransaction.sort(key=functools.cmp_to_key(self.compareItems))
				remaingUtility=-1
				for i in range(len(revisedTransaction)-1,-1,-1):
					pair=revisedTransaction[i]
					remainUtil=0
					for j in range(len(revisedTransaction)-1,i,-1):
						if(self.mapItemNighbours.get(pair.item)==None):
							continue
						if (revisedTransaction[j].item in self.mapItemNighbours[pair.item]):
							remainUtil+=revisedTransaction[j].quantity
					remaingUtility=remainUtil
					if(mapItemsToFFLIST.get(pair.item) is not None):
						FFListOfItem=mapItemsToFFLIST[pair.item]
						element=Element(tid,pair.quantity,remaingUtility)
						FFListOfItem.addElement(element)
				tid+=1
		itemNighbours=list(self.mapItemNighbours.keys())
		self.FSFIMining(self.itemsetBuffer,0,listOfFFIlist,self.minSup,itemNighbours);
		self.endTime=datetime.datetime.now();
		dif=self.endTime-self.startTime
		print("No.Of Itemssets ",self.itemsCnt);
		print("joinsCnt: ",self.joinsCnt);
	def FSFIMining(self,prefix,prefixLen,FSFIM,minsup,itemNighbours):
		"""Generates FFSI from prefix

        :param prefix: the prefix patterns of FFSI
        :type prefix: len
        :param prefixLen: the length of prefix
        :type prefixLen: int
       	:param FSFIM: the Fuzzy list of prefix itemsets
       	:type FSFIM: list
       	:param minsup: the minimum support of 
       	:type minsup:int
       	:param itemNighbours: the set of common neighbours of prefix
       	:type itemNighbours: set
		"""
		for i in range(0,len(FSFIM)):
			X=FSFIM[i]
			if(X.sumIutil>=minsup):
				self.WriteOut(prefix,prefixLen,X.item,X.sumIutil);
			newNeighbours=self.Intersection(self.mapItemNighbours.get(X.item),itemNighbours);
			if(X.sumRutil>=minsup):
				exULs=[]
				for j in range(i+1,len(FSFIM)):
					Y=FSFIM[j]
					if(Y.item in newNeighbours):
						exULs.append(self.construct(X,Y))
						self.joinsCnt+=1
				self.itemsetBuffer.insert(prefixLen,X.item)
				self.FSFIMining(self.itemsetBuffer,prefixLen+1,exULs,minsup,newNeighbours)
	def Intersection(self,nighb1,nighb2):
		"""
			A function to get common neighbous from 2 itemsets
			:param nighb1: the set of neighbours of itemset 1
			:type nighb1: set
			:param nighb2: the set of neighbours of itemset 2
			:type nighb2: set
			:return : set of common neighbours of 2 itemsets
			:rtype :set
		"""
		result=[]
		if(nighb1==None or nighb2==None):
			return result
		for i in range(0,len(nighb1)):
			if(nighb1[i] in nighb2):
				result.append(nighb1[i])
		return result
	def getMemoryRSS(self):
	    """Total amount of RSS memory consumed by the mining process will be retrieved from this function

        :return: returning RSS memory consumed by the mining process
        :rtype: float
	   """
	    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
	def getRuntime(self):
	    """Calculating the total amount of runtime taken by the mining process


        :return: returning total amount of runtime taken by the mining process
        :rtype: float
	   """
	    dif=self.endTime-self.startTime;
	    return dif.total_seconds()*1000
	def construct(self,px,py):
		"""
			A function to construct a new Fuzzy itemset from 2 fuzzy itemsets

			:param px:the itemset px
			:type px:FFI-List
			:param py:ithemset py
			:type py:FFI-List
			:return :the itemset of pxy(px and py)
			:rtype :FFI-List
		"""
		pxyUL=FFList(py.item)
		for ex in px.elements:
			ey=self.findElementWithTID(py,ex.tid);
			if(ey==None):
				continue
			eXY=Element(ex.tid,min([ex.iutils,ey.iutils],key=lambda x:float(x)),ey.rutils)
			pxyUL.addElement(eXY)
		return pxyUL
	def findElementWithTID(self,ulist,tid):
		"""
			To find element with same tid as given
			:param ulist:fuzzylist 
			:type ulist:FFI-List
			:param tid:transaction id
			:type tid:int
			:return:element eith tid as given
			:rtype: element if exizt or None
		"""
		List=ulist.elements
		first=0
		last=len(List)-1
		while first<=last:
			mid=(first+last)>>1;
			if(List[mid].tid<tid):
				first=mid+1
			elif(List[mid].tid>tid):
				last=mid-1
			else:
				return List[mid]
		return None
	def WriteOut(self,prefix,prefixLen,item,sumIutil):
		"""
			To Store the patten
			:param prefix: prefix of itemset
			:type prefix: list
			:param prefixLen: length of prefix
			:type prefixLen: int
			:param item: the last item
			:type item: int
			:param sumIutil: sum of utility of itemset
			:type sumIutil: float

		"""
		self.itemsCnt+=1
		res="";
		for i in range(0,prefixLen):
			res+=str(prefix[i])+" "+str(self.mapItemRegions[prefix[i]])+' '
		res+=str(item)+"."+str(self.mapItemRegions.get(item));
		res+=" #FVL: "+str(sumIutil)+"\n"
		self.bwriter.write(res)

if __name__ == "__main__":
	ap=AlgoFFSHUIM(sys.argv[1],sys.argv[2],sys.argv[3],int(sys.argv[4]))
	ap.startMine()
	memRSS = ap.getMemoryRSS()
	print("Total Memory in RSS", memRSS)
	run = ap.getRuntime()
	print("Total ExecutionTime in seconds:", run)