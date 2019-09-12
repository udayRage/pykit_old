#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys


# In[2]:


path = sys.argv[1]
outfile= sys.argv[2]
min_pf = float(sys.argv[3])
per = float(sys.argv[4])
min_sup=float(sys.argv[5])
length=int(sys.argv[6])


# In[3]:


class Node(object):
    def __init__(self, item, children):
        self.item = item
        self.children = children #dictionary of children
        self.parent = None
        self.tids = set()
        self.freq=0

    def addChild(self, node):
        self.children[node.item] = node
        node.parent = self


# In[4]:


class Tree(object):
    def __init__(self):
        self.root = Node(None, {})
        self.summaries = {}
        
    def add_transaction(self,transaction,tid,freq):
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
        curr_node.tids |= tid
        curr_node.freq+=freq
        
    
    def get_condition_pattern(self,alpha):
        final_patterns=[]
        final_sets=[]
        final_freq=[]
        for i in self.summaries[alpha]:
            set1=i.tids 
            loc_f=i.freq
            set2=[]
            while(i.parent.item!=None):
                set2.insert(0,i.parent.item)
                i=i.parent
            if(len(set2)>0):
                final_patterns.append(set2)
                final_freq.append(loc_f)
                final_sets.append(set1)
        pat,tids,fre=cond_trans(final_patterns,final_sets,final_freq)
        return pat,tids,fre
    
    def remove_node(self,node_val):
        for i in self.summaries[node_val]:
            i.parent.tids |= i.tids
            i.parent.freq += i.freq
            del i.parent.children[node_val]
            i=None
    def get_ts(self,alpha):
        tid_s=set()
        freq=0
        for i in self.summaries[alpha]:
            tid_s |=i.tids
            freq+=i.freq
        per_fre=get_per_fre(tid_s)
        return per_fre,freq        
    def generate_patterns(self,prefix,genelist):
        for i in sorted(self.summaries,reverse = True): 
            per_fre,freq=self.get_ts(i)
            pattern=prefix.copy()
            pattern.append(genelist[i])
            yield (pattern,per_fre,freq)                        
            patterns,tid_summ,tid_pf=self.get_condition_pattern(i)
            conditional_tree=Tree()
#             print(patterns)
            for pat in range(len(patterns)):
                conditional_tree.add_transaction(patterns[pat],tid_summ[pat],tid_pf[pat])
            if(len(patterns)>=1):
                for li in conditional_tree.generate_patterns(pattern,genelist):
                    yield (li)
            self.remove_node(i)


# In[5]:


def build_tree(data):
    root_node=Tree()
    for i in range(len(data)):
        set1=set()
        set1.add(data[i][0])
        root_node.add_transaction(data[i][1:],set1,1)
    return root_node


# In[6]:


def get_per_fre(tids):
    tids = list(tids)
    tids.sort()
    cur=tids[0]
    pf=0
    for j in range(1,len(tids)):
        if(tids[j]-cur<=per):
            pf+=1
        cur=tids[j]
    return pf


# In[7]:


def generate_dict(transactions):
    data={}
    for tr in transactions:
        for i in range(1,len(tr)):
            if tr[i] not in data:
                data[tr[i]]=[int(tr[0]),1,0]
            else:
                if((int(tr[0])-data[tr[i]][0]) <= per):
                    data[tr[i]][2]+=1
                data[tr[i]][0]=int(tr[0])
                data[tr[i]][1]+=1
    data={k: v for k,v in data.items() if v[2]>=min_pf and v[1]>=min_sup}
    return data


# In[8]:


def update_transactions1(list_of_transactions,dict1,gene_li):
    rank = dict([(index,item) for (item,index) in enumerate(gene_li)])
    list1=[]
    k=len(list_of_transactions)
    avg_tran_len=0
    for tr in list_of_transactions:
        list2=[int(tr[0])]
        for i in range(1,len(tr)):
            if tr[i] in dict1:
                list2.append(rank[tr[i]])                       
        if(len(list2)>=2):
            basket=list2[1:]
            avg_tran_len+=len(basket)
            basket.sort()
            list2[1:]=basket[0:]
            list1.append(list2)
    return list1,avg_tran_len/k


# In[9]:


def cond_trans(cond_pat,cond_tids,cond_freq):
    pat=[]
    tids=[]
    freq=[]  
    data1={}
    for i in range(len(cond_pat)):
        for j in cond_pat[i]:
#             print(j)
            if j in data1:
#                 print(cond_tids[i])
                data1[j]= data1[j] | cond_tids[i]
            else:
                data1[j]=cond_tids[i]
#                 print(cond_tids[i])
#         print(data1)
    updated_list=[]
    up_dict={}
#     print(data1)
    for m in data1:
        up_dict[m]=[get_per_fre(data1[m]),len(data1[m])]
    up_dict={k: v for k,v in up_dict.items() if v[0]<min_pf or v[1]<min_sup}
#     print(up_dict)
    count=0
    for p in cond_pat:
        trans=[]
        for q in p:
            if q not in up_dict:
                trans.append(q)
        if(len(trans)>0):
            pat.append(trans)
            tids.append(cond_tids[count])
            freq.append(cond_freq[count])
        count+=1
#     print(pat)
    return pat,tids,freq


# In[10]:


def get_segments(transactions,length):
    t_start=1
    seg_id=1
    segments=[]
    sub_segment=[]
    sub_segment.append(str(seg_id))
    incr=0
    # print(transactions)
    for i in transactions:
        # print(i)
        incr+=1
        if((int(i[0])-t_start)>length):
            segments.append(sub_segment)
            seg_id+=int((int(i[0])-t_start)/(length+1))
            t_start=int(i[0])
            sub_segment=[]
            sub_segment.append(str(seg_id))
            incr=1
        
        for j in range(1,len(i)):
            item = i[j]+'#'+str(incr)
            sub_segment.append(item)
    if len(sub_segment)>1:
        segments.append(sub_segment)
    return segments


# In[11]:


def main(path):    
    with open(path,'r') as f:
        lno=0
        list_of_transactions=[]
        for line in f:
            li=line.split() 
            list_of_transactions.append(li)
            lno=lno+1 
        f.close()
    total_transactions=len(list_of_transactions)
    x=int(total_transactions*1)
    print(x)
    list_of_segments=get_segments(list_of_transactions,length)
#     print(list_of_segments)
    generated_dict=generate_dict(list_of_segments)
#     print(generated_dict)
    gene_list=[key for key,value in sorted(generated_dict.items(), key=lambda x: x[1][1], reverse=True)]
#     rank = dict([(index,item) for (item,index) in enumerate(gene_list)])
    
    print("#########")
    print("NO of singleitems:",end='')
    print(len(gene_list))
    print("#########")
    updated_transactions1,k=update_transactions1(list_of_segments,generated_dict,gene_list)
#     print(updated_transactions1)
#     print(gene_list)
    Tree = build_tree(updated_transactions1)
#     for m in Tree.root._getTransactions():
#         print(m)
    q=Tree.generate_patterns([],gene_list)
    return q


# In[12]:


if(__name__ == "__main__"):
    k=main(path)
    with open(outfile, 'w') as f:
        for x in k:
            f.write('%s \n'%str(x))

