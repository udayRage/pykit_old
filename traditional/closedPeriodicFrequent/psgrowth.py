import sys
import time
import resource
import math
path=sys.argv[1]
outfile=sys.argv[2]
minsup=int(sys.argv[3])
maxperiod=int(sys.argv[4])
periodicitems=0
periodic={}
lno=0
class Node(object):
    def __init__(self, item, children):
        self.item = item
        self.children = children
        self.parent = None
        self.tids = []
        self.sup=0
        self.last=0

    def addChild(self, node):
        self.children[node.item] = node
        node.parent = self
class Tree(object):
	def __init__(self):
        	self.root = Node(None, {})
        	self.summaries = {}
        	self.info={}
	def add_transaction(self,transaction,tid):
		if type(tid)==int:
       	 		curr_node=self.root
        		for i in range(len(transaction)):
            			if transaction[i] not in curr_node.children:
                			new_node=Node(transaction[i],{})
                			curr_node.addChild(new_node)
                			if transaction[i] in self.summaries:
                    				self.summaries[transaction[i]].append(new_node)
                			else:
                    				self.summaries[transaction[i]]=[new_node]                    
                			curr_node=new_node                
            			else:
                			curr_node=curr_node.children[transaction[i]] 
       			curr_node.sup+=1
       			n=len(curr_node.tids)-1  
       			if(curr_node.tids==[]):
        			curr_node.tids.insert(n,[tid,tid,0])
       			else:
        			lp=abs(curr_node.last-tid)
        			if(lp>maxperiod):
        				curr_node.tids.insert(n+1,[tid,tid,0])
        			else:
        				curr_node.tids[n][2]=max(curr_node.tids[n][2],lp)
        				curr_node.tids[n][1]=tid
        		curr_node.last=tid
	def addTransaction(self,transaction,tid,sup):
       		curr_node=self.root
        	for i in range(len(transaction)):
            		if transaction[i] not in curr_node.children:
               	 		new_node=Node(transaction[i],{})
                		curr_node.addChild(new_node)
                		if transaction[i] in self.summaries:
                    			self.summaries[transaction[i]].append(new_node)
                		else:
                    			self.summaries[transaction[i]]=[new_node]                    
                		curr_node=new_node                
            		else:
                		curr_node=curr_node.children[transaction[i]]
                curr_node.sup=sup
             	curr_node.tids=tid
       	def get_condition_pattern(self,alpha):
        	final_patterns=[]
        	final_sets=[]
        	sup=[]
        	for i in self.summaries[alpha]:
            		q= self.genrate_tids(i)
            		set1=i.tids
            		s=i.sup 
            		set2=[]
            		while(i.parent.item!=None):
                		set2.append(i.parent.item)
                		i=i.parent
            		if(len(set2)>0):
                		set2.reverse()
                		final_patterns.append(set2)
                		final_sets.append(set1)
                		sup.append(s)
        	final_patterns,final_sets,info,support=cond_trans(final_patterns,final_sets,sup)
        	return final_patterns,final_sets,info,support
    
    	def genrate_tids(self,node):
        	final_tids=node.tids
        	return final_tids
    	def remove_node(self,node_val):
        	for i in self.summaries[node_val]:
            		i.parent.sup+=i.sup
            		#i.parent.tids=i.parent.tids+i.tids
            		#print i.parent.tids,"...",i.tids
            		if i.parent.tids==[]:
            			i.parent.tids=i.parent.tids+i.tids
            		else:
            			for k in i.tids:
            				for j in i.parent.tids:
            					if k[0]<j[0] and k[1]<j[1]:
            						lp=abs(k[1]-j[0])
            						if lp<=maxperiod:
            							j[0]=min(k[0],j[0])
            							j[1]=max(k[1],j[1])
            							j[2]=lp
            					elif k[0]>j[0]:
            						lp=abs(k[1]-j[0])
            						if lp<=maxperiod:
            							j[0]=min(k[0],j[0])
            							j[1]=max(k[1],j[1])
            							j[2]=lp
            		del i.parent.children[node_val]
            		i=None
                
    	def generate_patterns(self,prefix):
    		global periodic
        	for i in reversed(self.summaries.keys()):
            		pattern=prefix[:]
            		pattern.append(i)
            		if tuple(pattern) not in periodic:
            			st=saveperiodic(pattern)
            			#print st,self.info.get(i)
            			periodic[tuple(pattern)]=self.info.get(i)
            			yield pattern
            		t1=[]
            		for k in pattern:
            			t1.append(rankdup[k])
            			patterns,tids,info,support=self.get_condition_pattern(i)
            			conditional_tree=Tree()
            			conditional_tree.info=info.copy()
            			for pat in range(len(patterns)):
                			conditional_tree.addTransaction(patterns[pat],tids[pat],support[pat])
            			if(len(patterns)>0):
                			for q in conditional_tree.generate_patterns(pattern):
                    				yield q
            		self.remove_node(i)
def Merge(tids):
	s1=[]
	s2=[]
	if len(tids)>1:
		s=sorted(tids,key=lambda x:x[0][1])
		for i in range(len(s)-1):
			j=i+1	
			if s[i][0]<s[j][0]:
				temp=s[i]
				s[i]=s[j]
				s[j]=temp
				
			if s[i][0]>s[j][0]:
				s1=[[s[j][0][0],s[i][0][1],abs(s[i][0][1]-s[j][0][0])]]
			elif s[i][1]>s[j][1]:
				d=s[i][0][1]+maxperiod
				s1=[s[i][0][0],s[i][0][1],s[i][0][2]]
			elif s[i][0][1]+maxperiod>=s[j][0][0]:
				s1=[[s[j][0][0],s[j][0][1],s[j][0][2]]]
			else:
				s1.append([s[i][0][0],s[i][0][1],s[i][0][2]])
				s1.append([s[j][0][0],s[j][0][1],s[j][0][2]])
	s=sorted(tids,key=lambda x:x[0][1])
	if len(s)==1:
		for x in s:
			s2=s2+x			
		for i in range(len(s2)-1):
			j=i+1
			m=min(s2[i][0],s2[j][0])
			m1=max(s2[i][1],s2[j][1])
			lp=abs(s2[i][1]-s2[j][0])	
			s1=[[m,m1,lp]]
	return s1
def getPer_Sup(tids,sup):
    s=[]
    apt=0
    x=[]
    s1=Merge(tids)
    if len(s1)==1:
    	x=x+s1
    	#print x
    	if x[0][0]<=maxperiod:
    		s2=lno-x[0][1]
    		if s2<=maxperiod:
    			apt=x[0][2]
    return [sup,apt]
def cond_trans(cond_pat,cond_tids,sup):
    pat=[]
    tids=[]
    data1={}
    s=[]
    support={}
    for i in range(len(cond_pat)):
        for j in cond_pat[i]:
            if j in data1:
                data1[j].append(cond_tids[i])
                support[j]+=sup[i]
            else:
                data1[j]=[cond_tids[i]]
                support[j]=sup[i] 
    up_dict={}
    for m in data1:
    	up_dict[m]=getPer_Sup(data1[m],support[m])
    up_dict={k: v for k,v in up_dict.items() if v[0]>=minsup and v[1]<=maxperiod}
    count=0
    for p in cond_pat:
        p1=[v for v in p if v in up_dict]
        trans=sorted(p1)
        if(len(trans)>0):
            pat.append(trans)
            tids.append(cond_tids[count])
        count+=1
    return pat,tids,up_dict,sup
def generate_dict(transactions):
    global rank
    data={}
    for tr in transactions:
        for i in range(1,len(tr)):
            if tr[i] not in data:
                data[tr[i]]=[int(tr[0]),int(tr[0]),1]
            else:
                data[tr[i]][0]=max(data[tr[i]][0],(int(tr[0])-data[tr[i]][1]))
                data[tr[i]][1]=int(tr[0])
                data[tr[i]][2]+=1
    for key in data:
        data[key][0]=max(data[key][0],lno-data[key][1])

    data={k: [v[2],v[0]] for k,v in data.items() if v[0]<=maxperiod and v[2]>=minsup}
    genList=[k for k,v in sorted(data.items(),key=lambda x: x[1],reverse=True)]
    rank = dict([(index,item) for (item,index) in enumerate(genList)])
    return data,genList
def update_transactions1(list_of_transactions,dict1,rank):
    list1=[]
    for tr in list_of_transactions:
        list2=[int(tr[0])]
        for i in range(1,len(tr)):
            if tr[i] in dict1:
                list2.append(rank[tr[i]])                       
        if(len(list2)>=2):
            basket=list2[1:]
            basket.sort()
            list2[1:]=basket[0:]
            list1.append(list2)
    return list1
def build_tree(data,info):
    root_node=Tree()
    root_node.info=info.copy()
    for i in range(len(data)):
        set1=[]
        root_node.add_transaction(data[i][1:],data[i][0])
    return root_node
lno=1
rank={}
rank2={}
rankdup={}
alpha=0
def main():
    global pfList,lno,rank2,minsup,maxperiod,alpha
    with open(path,'r') as f:
        list_of_transactions=[]
        for line in f:
            li=[lno]
            li+=line.split() 
            list_of_transactions.append(li)
            lno+=1
        f.close()
    minsup=int(math.ceil(minsup*lno)/100)
    maxperiod=int(math.ceil(maxperiod*lno)/100)
    print(minsup,maxperiod)
    generated_dict,pfList=generate_dict(list_of_transactions)
    print("No. of single items:",len(pfList))
    updated_transactions1=update_transactions1(list_of_transactions,generated_dict,rank)
    for x,y in rank.items():
    	rankdup[y]=x
    info={rank[k]: v for k,v in generated_dict.items()}
    #print(rank)
    print 
    list_of_transactions=[]
    Tree = build_tree(updated_transactions1,info)
    intpat=Tree.generate_patterns([])
    return intpat
def saveperiodic(itemset):
	global periodicitems
	periodicitems+=1
	t1=[]
	for i in itemset:
		t1.append(rankdup[i])
	return t1
if(__name__ == "__main__"):
    k=main()
    #print periodic
    frequentitems=0
    starttime=int(round(time.time()*1000)) 
    with open(outfile, 'w') as f:
        for x in k:
            st=saveperiodic(x)
            f.write('%s \n'%st)
    with open(outfile,'r') as fi:
    	for line in fi:
    		frequentitems+=1
    endtime=int(round(time.time()*1000))
    temp=endtime-starttime
    print("Periodic frequentitems",frequentitems)
    print("time taken:",temp)
    print("MemorySpcae",resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
