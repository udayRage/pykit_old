import sys
list_of_transactions=[]
genelist=[]
with open(sys.argv[1],'r') as f:
    lno=0
    for line in f:
        li=line.split() 
        list_of_transactions.append(li)
        lno=lno+1 
    f.close()
min_sup=(float(sys.argv[3])*len(list_of_transactions))/100
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
    
        
    def add_transaction(self,transaction,freq): 
        curr_node = self.root 
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
            curr_node.freq+=freq 
    
    def get_condition_pattern(self,alpha):
        final_patterns=[] 
        final_freqencies=[]
        for i in self.summaries[alpha]:
            patfreq=i.freq
            cpattern=[] 
            while(i.parent.item!=None):
                cpattern.insert(0,i.parent.item)
                i=i.parent
            if(len(cpattern)>0):
                final_patterns.append(cpattern)
                final_freqencies.append(patfreq)
        final_patterns,final_freqencies=cond_trans(final_patterns,final_freqencies)
        return final_patterns,final_freqencies
    
    def remove_node(self,node_val):
        for i in self.summaries[node_val]:
            del i.parent.children[node_val]
            i=None

    def verify_sup(self,i):
    	freq=0
    	for j in self.summaries[i]:
    		freq+=j.freq
    	return freq

    #Fp-growth algorithm
    def generate_patterns(self,prefix): 
        for i in sorted(self.summaries,reverse = True):
            sup_i=self.verify_sup(i)
            pattern=prefix.copy()
            pattern.append(genelist[i])
            yield (pattern,sup_i)                       
            con_patterns,freq_list=self.get_condition_pattern(i)
            conditional_tree=Tree() 
            for pat in range(len(con_patterns)): 
                conditional_tree.add_transaction(con_patterns[pat],freq_list[pat]) 
            if(len(con_patterns)>=1): 
                for li in conditional_tree.generate_patterns(pattern): 
                    yield (li)
            self.remove_node(i)

def build_tree(data): # data is updated list of transactions
    root_node=Tree()
    for i in range(len(data)):
        root_node.add_transaction(data[i],1)
    return root_node

def generate_dict(transactions):
    data={}
    for tr in transactions:
        for i in range(0,len(tr)):
            if tr[i] not in data:
                data[tr[i]]=1
            else:
                data[tr[i]]+=1    
    data={k: v for k,v in data.items() if v>=min_sup}
    return data
def cond_trans(cond_pat,cond_freq):
    pat=[]
    freq=[]  
    data1={}
    for i in range(len(cond_pat)):
        for j in cond_pat[i]:
            if j in data1:
                data1[j]+=cond_freq[i]
            else:
                data1[j]=cond_freq[i]
    up_dict={}
    up_dict={k: v for k,v in data1.items() if v<min_sup}
    count=0
    for p in cond_pat:
        trans=[]
        for q in p:
            if q not in up_dict:
                trans.append(q)
        if(len(trans)>0):
            pat.append(trans)
            freq.append(cond_freq[count])
        count+=1
    return pat,freq
def update_transactions1(list_of_transactions,dict1,rank): #rearranging the transaction items; sorted by freq; eliminated non freq items
    list1=[]
    k=len(list_of_transactions)
    for tr in list_of_transactions:
        list2=[]
        for i in range(0,len(tr)):
            if tr[i] in dict1:
            	list2.append(rank[tr[i]])
        if(len(list2)>=1):	
            list2.sort()
            list1.append(list2)
    return list1
def update_hash(dict):
	genelist=[key for key,value in sorted(dict.items(), key=lambda x: x[1], reverse=True)]
	return genelist

def main():   
    generated_dict=generate_dict(list_of_transactions) #returns freq items and support; dictionary
    global genelist
    genelist=update_hash(generated_dict)
    rank = dict([(index,item) for (item,index) in enumerate(genelist)]) 
    updated_transactions1=update_transactions1(list_of_transactions,generated_dict,rank)
    Tree = build_tree(updated_transactions1)
    q=Tree.generate_patterns([]) #send prefix as empty
    return q

if(__name__ == "__main__"):
    outfile= sys.argv[2]    
    k=main()
    with open(outfile, 'w') as f:
        for x in k:
            f.write('%s \n'%str(x))
