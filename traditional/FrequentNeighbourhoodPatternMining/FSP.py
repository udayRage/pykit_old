import sys
from collections import defaultdict
import os
import psutil
process = psutil.Process(os.getpid())
def defaultvalue():
    return set();
path = sys.argv[1]
outfile= sys.argv[3]
# periodicity = int(sys.argv[5])
min_sup=int(sys.argv[4])
updated_nbh=defaultdict(defaultvalue)
nbh_path= sys.argv[2]


class Node(object): 
    def __init__(self, item, children):
        self.item = item
        self.children = children 
        self.parent = None
        self.freq =  0  

    def addChild(self, node): 
        self.children[node.item] = node  
        node.parent = self 


class Tree(object):
    def __init__(self):
        self.root = Node(None, {}) 
        self.summaries = {}
        self.info={} 
    
        
    def add_transaction(self,transaction,freq): 
        curr_node = self.root
        # c=0
        for i in range(len(transaction)):
            if transaction[i] not in curr_node.children:
                new_node=Node(transaction[i],{})
                curr_node.addChild(new_node)
                # print(freq)
                 
                if transaction[i] in self.summaries:
                    self.summaries[transaction[i]].append(new_node)
                else: 
                    self.summaries[transaction[i]]=[new_node]                  
                curr_node=new_node
                # print("initial",curr_node.freq,freq)
                # curr_node.freq+=freq               
            else:
                curr_node=curr_node.children[transaction[i]]           
            curr_node.freq+=freq
            # print((i,curr_node.freq),end='') 
        # print()
    
    def get_condition_pattern(self,alpha,newNBH):
        final_patterns=[]
        final_freqencies=[]
        #final_freq=[]
        for i in self.summaries[alpha]:
            patfreq=i.freq     
            cpattern=[] 
            while(i.parent.item!=None):
                if i.parent.item in newNBH:
                    cpattern.append(i.parent.item) 
                i=i.parent 
            cpattern.reverse()
            if(len(cpattern)>0):
                final_patterns.append(cpattern)
                final_freqencies.append(patfreq)
        upCpatterns,upFreq,info=getupdate(final_patterns,final_freqencies)
        del final_patterns,final_freqencies,patfreq,cpattern
        return upCpatterns,upFreq,info
    
    def remove_node(self,node_val):
        for i in self.summaries[node_val]:
            del i.parent.children[node_val]
            i=None
            del i

    def verify_sup(self,i): # return support of item i in the tree
    	freq=0
    	for j in self.summaries[i]:
    		freq+=j.freq
    	return freq

    #Fp-growth algorithm
    def generate_patterns(self,prefix,nbh): 
        for i in sorted(self.summaries,key= lambda x:(self.info.get(x),-x)):
            pattern=prefix.copy() # projecte database; 
            pattern.append(fpList[i]) # add item to the pattern
            yield (pattern,self.info[i])
            newNBH= nbh& updated_nbh[i]
            # print(pattern)                        
                # print(pattern,pf)
            con_patterns,freq_list,info=self.get_condition_pattern(i,newNBH) #generate condition patterns for item i
            conditional_tree=Tree()
            conditional_tree.info=info.copy()
            # del info
            for pat in range(len(con_patterns)): #iterate over condtion patterns
                conditional_tree.add_transaction(con_patterns[pat],freq_list[pat]) # add conditional patterns to conditional tree
            if(len(con_patterns)>=1): # con_pattren length is not zero
                for li in conditional_tree.generate_patterns(pattern,newNBH): #generates freq patterns from conditional tree
                    yield (li)
            del con_patterns,freq_list,conditional_tree
            del newNBH
            del pattern
            self.remove_node(i)
        del self.summaries
        del self.info
        del self



def getupdate(cond_pat,cond_count):
    pat=[]
    counts=[]
    data1={}
    for i in range(len(cond_pat)):
        for j in cond_pat[i]:
            if j in data1:
                data1[j]= data1[j] + cond_count[i]
            else:
                data1[j]=cond_count[i]

    up_dict={}
    up_dict={k: v for k,v in data1.items() if v>=min_sup}
    del data1
    count=0
    p1=[]
    trans=[]
    for p in cond_pat:
        p1=[v for v in p if v in up_dict]
        trans=sorted(p1, key= lambda x: (up_dict.get(x),-x), reverse=True)
        if(len(trans)>0):
            pat.append(trans)
            counts.append(cond_count[count])
        count+=1
    del count
    del p1
    del trans
    return pat,counts,up_dict


def build_tree(data,info):
    root_node=Tree()
    # root_node=Tree()
    root_node.info=info.copy()
    del info
    for i in range(len(data)):
        # print(data[i])
        root_node.add_transaction(data[i],1)
    return root_node

rank={}
def generate_dict(transactions,min_sup):
    global rank
    data={}
    for tr in transactions:
        for i in range(0,len(tr)):
            if tr[i] not in data:
                data[tr[i]]=1
            else:
                data[tr[i]]+=1    
    # print(data)                       
    data={k: v for k,v in data.items() if v>=min_sup}
    genList=[k for k,v in sorted(data.items(),key=lambda x: (x[1],x[0]),reverse=True)]
    rank = dict([(index,item) for (item,index) in enumerate(genList)])
    #print("No of times item in a transaction deleted:",end='')
    del tr
    return data,genList

def update_transactions1(list_of_transactions,dict1,gene_li):
    list1=[]
    # k=len(list_of_transactions)
    # avg_len=0
    for tr in list_of_transactions:
        list2=[]
        for i in range(0,len(tr)):
            if tr[i] in dict1:
                list2.append(rank[tr[i]])
        if(len(list2)>=1):
            # avg_len+=len(list2)     
            list2.sort()
            list1.append(list2)
    del list2
    return list1

def main():
    global fpList,lno
    with open(path,'r') as f:
        list_of_transactions=[]
        for line in f:
            li=line.split() 
            list_of_transactions.append(li)
            # lno+=1
        f.close()
    generated_dict,fpList=generate_dict(list_of_transactions,min_sup)
    print("No. of single items:",len(fpList))
    # print(generated_dict)
    #print(fpList)   
    # break
    updated_transactions1=update_transactions1(list_of_transactions,generated_dict,rank)
    # print(len(updated_transactions1),len(list_of_transactions))
    nbh_dict={}
    with open(nbh_path,'r') as nbh:
        for line in nbh:
            li=line.split()
            ds=set()
            for i in range(1,len(li)):
                ds.add(li[i])
            nbh_dict[li[0]]=ds
    # # # print(updated_transactions1)
    for i in fpList:
        if i in nbh_dict:
            for j in nbh_dict[i]:
                if j in fpList:
                    updated_nbh[rank[i]].add(rank[j])
                    updated_nbh[rank[j]].add(rank[i])
    g_list = [i for i in range(len(fpList))]
    nbh=set(g_list)
    del nbh_dict
    # # print(rank)
    info={rank[k]: v for k,v in generated_dict.items()}
    del list_of_transactions
    # print(updated_transactions1)
    Tree = build_tree(updated_transactions1,info)
    # print(Tree.root.children)
    # print(Tree.root.children[1].freq)
    intpat=Tree.generate_patterns([],nbh)
    return intpat


if(__name__ == "__main__"):
    k=main()
    cou=0
    with open(outfile, 'w') as f:
        for x in k:
            z='Pattern:'+str(x[0])+','+'Sup:'+str(x[1])
            f.write('%s \n'%z)
            cou+=1
    print("Total Patterns:",end=' ')
    print(cou)
    print("Memory consumed(uss):",process.memory_full_info().uss)
    print("Memory consumed(rss):",process.memory_full_info().rss)    
    f.close()