import sys
from collections import defaultdict
supp_dict={}
path = sys.argv[1]
nbh_path= sys.argv[2]
outfile= sys.argv[3]
per_freq = float(sys.argv[4])
periodicity = float(sys.argv[5])
min_rps=float(sys.argv[6])
def defaultvalue():
    return set();
updated_nbh=defaultdict(defaultvalue)
gene_list=[]
class Node(object):
    def __init__(self, item, children):
        self.item = item
        self.children = children #dictionary of children
        self.parent = None
        self.tids = []

    def addChild(self, node):
        self.children[node.item] = node
        node.parent = self

class Tree(object):
    def __init__(self):
        self.root = Node(None, {})
        self.summaries = {}
        
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
        curr_node.tids= curr_node.tids + tid
        
    def get_condition_pattern(self,alpha,new_nbh):
        final_patterns=[]
        final_sets=[]
        for i in self.summaries[alpha]:
            q= self.genrate_tids(i)
            set1=i.tids 
            set2=[]
            while(i.parent.item!=None):
            	if i.parent.item in new_nbh:
            		set2.insert(0,i.parent.item)
            	i=i.parent
            if(len(set2)>0):
                final_patterns.append(set2)
                final_sets.append(set1)
            set2=[]
        return final_patterns,final_sets
    
    def genrate_tids(self,node):
        final_tids=node.tids
        return final_tids
    def remove_node(self,node_val):
        for i in self.summaries[node_val]:
            # print(gene_list[i.item],gene_list[i.parent.item])
            i.parent.tids = i.parent.tids + i.tids
            del i.parent.children[node_val]
            i=None
    def get_ts(self,alpha):
        temp_ids=[]
        for i in self.summaries[alpha]:
            temp_ids+=i.tids
            # print(i.children)
        return temp_ids
                
    def generate_patterns(self,prefix,nbh):
        for i in sorted(self.summaries,reverse = True):
            temp_ids=self.get_ts(i)
            pf=verify_tids(temp_ids)
            if(len(prefix)==0):
                # k=
                rps=pf/(supp_dict[gene_list[i]]-1)
            else:
                rps=pf/(supp_dict[prefix[0]]-1)
            if(pf>=per_freq and rps>=min_rps):
                pattern=prefix.copy()
                pattern.append(gene_list[i])
                yield (pattern,pf)
                new_nbh= nbh & updated_nbh[i]
                patterns,tids=self.get_condition_pattern(i,new_nbh)
                conditional_tree=Tree()
                for pat in range(len(patterns)):
                    conditional_tree.add_transaction(patterns[pat],tids[pat])
                if(len(patterns)>=1):
                    for li in conditional_tree.generate_patterns(pattern,new_nbh):
                        yield (li)
            self.remove_node(i)


def build_tree(data):
    root_node=Tree()
    for i in range(len(data)):
        set1=[]
        set1.append(data[i][0])
#         print(data[i][1:])
        root_node.add_transaction(data[i][1:],set1)
    return root_node 


# In[21]:


def verify_tids(tids):
    tids.sort()
    cur=tids[0]
    pf=0
    for j in range(1,len(tids)):
        if(tids[j]-cur<=periodicity):
            pf+=1
        cur=tids[j]
    return pf


# In[22]:


def generate_dict(transactions):
    data={}
    for tr in transactions:
        for i in range(1,len(tr)):
            if tr[i] not in data:
                data[tr[i]]=[0,int(tr[0]),1]
                supp_dict[tr[i]]=1
            else:
                if((int(tr[0])-data[tr[i]][1]) <= periodicity):
                    data[tr[i]][0]+=1
                    data[tr[i]][1]=int(tr[0]) 
                    data[tr[i]][2]+=1
                else:
                    data[tr[i]][1]=int(tr[0]) 
                    data[tr[i]][2]+=1
                supp_dict[tr[i]]+=1                    
    data={k: v for k,v in data.items() if v[0]>=per_freq}
    return data,supp_dict


# In[23]:


def update_transactions1(list_of_transactions,dict1,gene_li):
    rank = dict([(index,item) for (item,index) in enumerate(gene_li)])
#     print(rank)
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


# In[24]:
def genelist(generated_dict):
	global gene_list
	gene_list=[key for key,value in sorted(generated_dict.items(), key=lambda x: x[1][2], reverse=True)]
	return gene_list;


def main():    
    with open(path,'r') as f:
        lno=0
        list_of_transactions=[]
        for line in f:
            li=line.split() 
            list_of_transactions.append(li)
            lno=lno+1 
        f.close()
    print(per_freq,periodicity)
    nbh_dict={}
    generated_dict,supp_dict=generate_dict(list_of_transactions)
    # print(supp_dict)
    gene_list=genelist(generated_dict)
    
    updated_transactions1=update_transactions1(list_of_transactions,generated_dict,gene_list)
    with open(nbh_path,'r') as nbh:
        for line in nbh:
            li=line.split()
            ds=set()
            for i in range(1,len(li)):
                ds.add(li[i])
            nbh_dict[li[0]]=ds
    # print(updated_nbh[1])
    rank = dict([(index,item) for (item,index) in enumerate(gene_list)])
    print(len(gene_list))
    us=set(gene_list)
    for i in gene_list:
        if i in nbh_dict:
        	for j in nbh_dict[i]:
        		if j in gene_list:
        			updated_nbh[rank[i]].add(rank[j])
        			updated_nbh[rank[j]].add(rank[i])
    # print(updated_nbh)
    g_list = [i for i in range(len(gene_list))]
    nbh=set(g_list)
    # print(updated_nbh)
    # print(updated_transactions1)
    Tree = build_tree(updated_transactions1)
    q=Tree.generate_patterns([],nbh)
    return q


# In[26]:


if(__name__ == "__main__"):
    k=main()
    with open(outfile, 'w') as f:
        for x in k:
            f.write('%s \n'%str(x))