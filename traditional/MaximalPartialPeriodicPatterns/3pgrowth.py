import math
import sys
import time
import resource
path=sys.argv[1]
output=sys.argv[2]
periodicSupport=float(sys.argv[3])
IntervalTime=float(sys.argv[4])
frequentitems=0
periodic={}
lno=0
rank={}
rankdup={}
class Node(object):
    def __init__(self, item, children):
        self.item = item
        self.children = children
        self.parent = None
        self.tids = []

    def addChild(self, node):
        self.children[node.item] = node
        node.parent = self
class Tree(object):
    def __init__(self):
        self.root = Node(None, {})
        self.summaries = {}
        self.info={}
    def add_transaction(self,transaction,tid):
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
            curr_node.tids=curr_node.tids+tid
    def get_condition_pattern(self,alpha):
        final_patterns=[]
        final_sets=[]
        for i in self.summaries[alpha]:
            q= self.genrate_tids(i)
            set1=i.tids 
            set2=[]
            while(i.parent.item!=None):
                set2.append(i.parent.item)
                i=i.parent
            if(len(set2)>0):
                set2.reverse()
                final_patterns.append(set2)
                final_sets.append(set1)
        final_patterns,final_sets,info=cond_trans(final_patterns,final_sets)
        return final_patterns,final_sets,info
    def genrate_tids(self,node):
        final_tids=node.tids
        return final_tids
    def remove_node(self,node_val):
        for i in self.summaries[node_val]:
            i.parent.tids = i.parent.tids + i.tids
            del i.parent.children[node_val]
            i=None
    def get_ts(self,alpha):
        temp_ids=[]
        for i in self.summaries[alpha]:
            temp_ids+=i.tids
        return temp_ids
                
    def generate_patterns(self,prefix):
        for i in sorted(self.summaries,key= lambda x:(self.info.get(x)[0],-x)):
            pattern=prefix[:]
            pattern.append(i)
            s=saveperiodic(pattern)
            #print s,self.info.get(i)
            n=self.info.get(i)
            yield(pattern)
            patterns,tids,info=self.get_condition_pattern(i)
            conditional_tree=Tree()
            conditional_tree.info=info.copy()
            for pat in range(len(patterns)):
                conditional_tree.add_transaction(patterns[pat],tids[pat])
            if(len(patterns)>0):
                for q in conditional_tree.generate_patterns(pattern):
                    yield q
            self.remove_node(i)


def getPer_Sup(tids):
    tids.sort()
    cur=0
    per=0
    sup=0
    #print tids
    for i in range(len(tids)-1):
        j=i+1
        if abs(tids[j]-tids[i])<=IntervalTime:
            per+=1
        sup+=1
    return [len(tids),per]        
def cond_trans(cond_pat,cond_tids):
    pat=[]
    tids=[]
    data1={}
    for i in range(len(cond_pat)):
        for j in cond_pat[i]:
            if j in data1:
                data1[j]= data1[j] + cond_tids[i]
            else:
                data1[j]=cond_tids[i]
    up_dict={}
    for m in data1:
        up_dict[m]=getPer_Sup(data1[m])
    up_dict={k: v for k,v in up_dict.items() if v[1]>=periodicSupport}
    count=0
    for p in cond_pat:
        p1=[v for v in p if v in up_dict]
        trans=sorted(p1, key= lambda x: (up_dict.get(x)[0],-x), reverse=True)
        if(len(trans)>0):
            pat.append(trans)
            tids.append(cond_tids[count])
        count+=1
    return pat,tids,up_dict
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
        set1.append(data[i][0])
        root_node.add_transaction(data[i][1:],set1)
    return root_node
def generate_dict(transactions):
    global rank
    data={}
    for tr in transactions:
        for i in range(1,len(tr)):
            if tr[i] not in data:
                data[tr[i]]=[0,int(tr[0]),1]
            else:
                lp=int(tr[0])-data[tr[i]][1]
                if lp<=IntervalTime:
                    data[tr[i]][0]+=1
                data[tr[i]][1]=int(tr[0])
                data[tr[i]][2]+=1
    data={k: [v[2],v[0]] for k,v in data.items() if v[0]>=periodicSupport}
    genList=[k for k,v in sorted(data.items(),key=lambda x: (x[1][0],x[0]),reverse=True)]
    rank = dict([(index,item) for (item,index) in enumerate(genList)])
    return data,genList
def saveperiodic(itemset):
    t1=[]
    for i in itemset:
        t1.append(rankdup[i])
    return t1
#global pfList,lno,rank2,rankdup,minsup,maxperiod
def main():
    global pfList,lno,rank2,rankdup,periodicSupport,IntervalTime
    with open(path,'r') as f:
        list_of_transactions=[]
        for line in f:    
            li=line.split() 
            list_of_transactions.append(li)
            lno+=1
    f.close()
    periodicSupport=int(math.ceil(periodicSupport*lno)/100)
    IntervalTime=int(math.ceil(IntervalTime*lno)/100)
    print(periodicSupport,IntervalTime)
    generated_dict,pfList=generate_dict(list_of_transactions)  
    updated_transactions1=update_transactions1(list_of_transactions,generated_dict,rank)
    for x,y in rank.items():
            rankdup[y]=x
    info={rank[k]: v for k,v in generated_dict.items()}
    list_of_transactions=[]
    Tree1= build_tree(updated_transactions1,info)
    intpat=Tree1.generate_patterns([])
    return intpat
if(__name__ == "__main__"):
    starttime=int(round(time.time()*1000)) 
    frequentitems=0
    k=main()
    with open(output, 'w') as f:
        for x in k:
            st=saveperiodic(x)
            f.write('%s \n'%st)
    with open(output,'r') as fi:
        for line in fi:
            frequentitems+=1
    endtime=int(round(time.time()*1000))
    temp=endtime-starttime
    #print("conditionalNodes count:",conditionalnodes)
    print("partial periodic frequent",frequentitems)
    print("Time Taken:",temp)
    print("Memory Space",resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)    
