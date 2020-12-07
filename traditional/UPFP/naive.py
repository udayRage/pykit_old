import sys
import time
import math
import resource
path=sys.argv[1]
output=sys.argv[2]
minSup=float(sys.argv[3])
maxperiod=float(sys.argv[4])
writer=open(output,'w')
rank={}
periodic={}
rankdup={}
class Item:
	def __init__(self,item,probability):
		self.item=item
		self.probability=probability
		
class Node(object):
    def __init__(self, item, children):
        self.item = item
        self.probability=1
        self.children = children
        self.parent = None
        
    def addChild(self, node):
        self.children[node.item] = node
        node.parent = self


class Tree(object):
    def __init__(self):
        self.root = Node(None, {})
        self.summaries = {}
        self.info={}
    def add_transaction(self,transaction):
    	a1=0
        curr_node=self.root
        for i in range(len(transaction)):
            if transaction[i].item not in curr_node.children:
                new_node=Node(transaction[i].item,{})
                l1=i-1
                l=[]
                while(l1>=0):
                	l.append(transaction[l1].probability)
                	l1-=1
                if len(l)==0:
                	new_node.probability=transaction[i].probability
                else:
                	new_node.probability=max(l)*transaction[i].probability
                curr_node.addChild(new_node)
                if transaction[i].item in self.summaries:
                    self.summaries[transaction[i].item].append(new_node)
                else:
                    self.summaries[transaction[i].item]=[new_node]                    
                curr_node=new_node                
            else:
                curr_node=curr_node.children[transaction[i].item]  
                l1=i-1
                l=[]
                while(l1>=0):
                	l.append(transaction[l1].probability)
                	l1-=1
                if len(l)==0:
                	curr_node.probability+=transaction[i].probability
                else:
                	curr_node.probability+=max(l)*transaction[i].probability     
        #curr_node.tids= curr_node.tids + tid
    def addTransaction(self,transaction,sup):
        curr_node=self.root
        for i in range(len(transaction)):
            if transaction[i] not in curr_node.children:
                new_node=Node(transaction[i],{})
                new_node.probability=sup
                curr_node.addChild(new_node)
                if transaction[i] in self.summaries:
                    self.summaries[transaction[i]].append(new_node)
                else:
                    self.summaries[transaction[i]]=[new_node]                    
                curr_node=new_node                
            else:
                curr_node=curr_node.children[transaction[i]] 
                curr_node.probability+=sup           
        #curr_node.tids= curr_node.tids + tid
    def condition_pattern(self,alpha):
    	final_patterns=[]
        #final_sets=[]
        sup=[]
        for i in self.summaries[alpha]:
            #q= self.genrate_tids(i)
            #set1=i.tids
            s=i.probability 
            set2=[]
            while(i.parent.item!=None):
                set2.append(i.parent.item)
                i=i.parent
            if(len(set2)>0):
                set2.reverse()
                final_patterns.append(set2)
                #final_sets.append(set1)
                sup.append(s)
        final_patterns,support,info=cond_trans(final_patterns,sup)
        return final_patterns,support,info
    def genrate_tids(self,node):
        final_tids=node.tids
        return final_tids
    def remove_node(self,node_val):
        for i in self.summaries[node_val]:
            #i.parent.tids = i.parent.tids + i.tids
            del i.parent.children[node_val]
            i=None
    def get_ts(self,alpha):
        temp_ids=[]
        for i in self.summaries[alpha]:
            temp_ids+=i.tids
        return temp_ids
    		
    def generate_patterns(self,prefix):
    	global periodic
    	for i in sorted(self.summaries,key= lambda x:(self.info.get(x))):
            global conditionalnodes
            pattern=prefix[:]
            pattern.append(i)
            s=0
            for x in self.summaries[i]:
            	s+=x.probability
            yield pattern
            periodic[tuple(pattern)]=self.info[i]
            if s>=minSup:
            	patterns,support,info=self.condition_pattern(i)
            	conditional_tree=Tree()
            	conditional_tree.info=info.copy()
            	for pat in range(len(patterns)):
                	conditional_tree.addTransaction(patterns[pat],support[pat])
            	if(len(patterns)>0):
                	for q in conditional_tree.generate_patterns(pattern):
                		yield q
            self.remove_node(i)
    
def getPer_Sup(s,tids):
    global lno
    tids.sort()
    cur=0
    per=0
    sup=s
    for j in range(len(tids)):
        per=max(per,tids[j]-cur)
        if(per>maxperiod):
            return [0,0]
        cur=tids[j]
        #sup+=1
    per=max(per,lno-cur)
    return [sup,per]

def cond_trans(cond_pat,support):
    global minSup
    pat=[]
    tids=[]
    sup=[]
    data1={}
    count={}
    for i in range(len(cond_pat)):
        for j in cond_pat[i]:
            if j in count:
                count[j]+=support[i]
            else:
                count[j]=support[i]
    up_dict={}
    #for m in count:
        #up_dict[m]=getPer_Sup(count[m],data1[m])
    up_dict={k: v for k,v in count.items() if v>=minSup}
    count=0
    for p in cond_pat:
        p1=[v for v in p if v in up_dict]
        trans=sorted(p1, key= lambda x: up_dict[x],reverse=True)
        if(len(trans)>0):
            pat.append(trans)
            #tids.append(cond_tids[count])
            sup.append(support[count])
        count+=1
    return pat,sup,up_dict
        

def scanDatabase(transactions):
	global minSup,rank
	mapSupport={}
	for i in transactions:
		n=i[0]
		for j in i[1:]:
			if j.item not in mapSupport:
				mapSupport[j.item]=j.probability
			else:
				mapSupport[j.item]+=j.probability
    	mapSupport={k: v for k,v in mapSupport.items() if v>=minSup}
    	plist=[k for k,v in sorted(mapSupport.items(),key=lambda x:x[1],reverse=True)]
    	rank = dict([(index,item) for (item,index) in enumerate(plist)])
    	return mapSupport,plist

def build_tree(data,info):
    a=0
    root_node=Tree()
    root_node.info=info.copy()
    for i in range(len(data)):
        q=root_node.add_transaction(data[i][1:])
    return root_node  
    	
def update_transactions1(list_of_transactions,dict1,rank):
	list1=[]
	for tr in list_of_transactions:
		list2=[int(tr[0])]
		for i in range(1,len(tr)):
			if tr[i].item in dict1:
				list2.append(tr[i])                       
		if(len(list2)>=2):
			basket=list2[1:]
			basket.sort(key=lambda val:rank[val.item])
			list2[1:]=basket[0:]
			list1.append(list2)
	return list1
def saveperiodic(itemset):
	t1=[]
	for i in itemset:
		t1.append(rankdup[i])
	return t1
'''def getPer_Sup(tids):
    global lno
    tids.sort()
    cur=0
    per=[]
    sup=s
    for j in range(len(tids)):
        if j==0:
        	per.append(abs(tids[j]-0))
        elif j>=1:
        	per.append(abs(tids[j-1]-tids[j]))
       	elif j==len(tids)-1:
       		per.append(abs(lno-tids[j]))
    if len(per)>0:
    	return max(per)'''
def getPer(tids):
	global lno
    	tids.sort()
    	cur=0
    	per=0
    	for j in range(len(tids)):
       		per=max(per,tids[j]-cur)
        	cur=tids[j]
        	#sup+=1
    	per=max(per,lno-cur)
    	return per
def Check(i,x):
	check=False
	for m in x:
		k=0
		for n in i:
			#print m.item,n
			if m==n.item:
				k+=1
				check=True
		if k==0:
			return 0
	return 1
starttime=int(round(time.time()*1000)) 
lno=0		
transactions=[]
tt=[]
with open(path,'r') as f:
	for line in f:
		l=[lno]
		l+=line.split()
		t=[]
		tr=[int(l[0])]
		t=[int(l[0])]
		for i in l[1:]:
			i1=i.index('(')
			i2=i.index(')')
			item=i[0:i1]
			probability=float(i[i1+1:i2])
			t.append(item)
			product=Item(item,probability)
			tr.append(product)
		lno+=1
		tt.append(t)
		transactions.append(tr)
mapSupport,plist=scanDatabase(transactions)
transactions1=update_transactions1(transactions,mapSupport,rank)
info={k: v for k,v in mapSupport.items()}
Tree1 = build_tree(transactions1,info)
n=Tree1.generate_patterns([])
count=0		
for x in n:			
	s=str(x)
	#count+=1
	#writer.write('%s \n'%s)
periods={}
for i in transactions:
	#for k in i[1:]:
		#print k.item,k.probability
	for x,y in periodic.items():
		l=[]
		s=1
		check=Check(i[1:],x)
		#print check
		if check==1:
			for j in i[1:]:
				if j.item in x:
					l.append(int(i[0]))
					s*=j.probability
			if x in periods:
				periods[x][0]=periods[x][0]+l
				periods[x][1]+=s
			else:
				periods[x]=[l,s]
for x,y in periods.items():
	p=getPer(y[0])
	#print x,y,p
	if p<=maxperiod and y[1]>=minSup:
		#print x,p
		s=str(x)
		count+=1
		writer.write('%s \n'%s)
endtime=int(round(time.time()*1000)) 
temp=endtime-starttime
print("periodic-frequentitems",count)
print("Time Taken:",temp)
print("Memory Space",resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
