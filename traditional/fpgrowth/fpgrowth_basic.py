port sys

class Node(object):
    def __init__(self, item, children):
        self.item = item
        self.children = children #dictionary of children
        self.parent = None
        self.freq =  0
        # self.freq=0

    def addChild(self, node):
        self.children[node.item] = node
        node.parent = self


class Tree(object):
    def __init__(self):
        self.root = Node(None, {})
        self.summaries = {}
    
        
    def add_transaction(self,transaction,freq):
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
        curr_node.freq+=freq
    
    def get_condition_pattern(self,alpha):
        final_patterns=[]
        final_sets=[]
        final_freq=[]
        for i in self.summaries[alpha]:
            set1=i.freq 
            set2=[]
            while(i.parent.item!=None):
                set2.insert(0,i.parent.item)
                i=i.parent
            if(len(set2)>0):
                final_patterns.append(set2)
                final_sets.append(set1)
        return final_patterns,final_sets
    
    def remove_node(self,node_val):
        for i in self.summaries[node_val]:
            i.parent.freq = i.parent.freq + i.freq
            # i.parent.freq = i.parent.freq + i.freq
            del i.parent.children[node_val]
            i=None

    def verify_sup(self,i):
    	freq=0
    	for j in self.summaries[i]:
    		freq+=j.freq
    	return freq

    def generate_patterns(self,prefix,min_sup,genelist):
        for i in sorted(self.summaries,reverse = True):
            
            sup_i=self.verify_sup(i)    
            if(sup_i>=min_sup ):
                pattern=prefix.copy()
                pattern.append(genelist[i])
                yield (pattern,sup_i)
                print(pattern)                        
                # print(pattern,pf)
                con_patterns,freq_list=self.get_condition_pattern(i)
                conditional_tree=Tree()
                for pat in range(len(con_patterns)):
                    conditional_tree.add_transaction(con_patterns[pat],freq_list[pat])
                if(len(con_patterns)>=1):
                    for li in conditional_tree.generate_patterns(pattern,min_sup,genelist):
                        yield (li)
            self.remove_node(i)
    

def build_tree(data):
    root_node=Tree()
    for i in range(len(data)):
        root_node.add_transaction(data[i],1)
    return root_node

def generate_dict(transactions,min_sup):
    data={}
    for tr in transactions:
        for i in range(0,len(tr)):
            if tr[i] not in data:
                data[tr[i]]=1
            else:
                data[tr[i]]+=1    
    # print(data)                       
    data={k: v for k,v in data.items() if v>=min_sup}
    #print("No of times item in a transaction deleted:",end='')
    return data  

def update_transactions1(list_of_transactions,dict1,gene_li):
    rank = dict([(index,item) for (item,index) in enumerate(gene_li)])
    print(rank)
    print(dict1)
    list1=[]
    k=len(list_of_transactions)
    avg_len=0
    for tr in list_of_transactions:
        list2=[]
        for i in range(0,len(tr)):
            if tr[i] in dict1:
            	list2.append(rank[tr[i]])
        if(len(list2)>=1):
            avg_len+=len(list2) 	
            list2.sort()
            list1.append(list2)
        print(list2)
    return list1,avg_len/k   


def main(path,min_sup):    
    with open(path,'r') as f:
        lno=0
        list_of_transactions=[]
        for line in f:
            li=line.split() 
            list_of_transactions.append(li)
            lno=lno+1 
        f.close()
    total_transactions=len(list_of_transactions)
#     print(total_transactions)
    min_sup = (min_sup*total_transactions)/100
    print(min_sup)
    
    generated_dict=generate_dict(list_of_transactions,min_sup)
    # print(generated_dict)
    gene_list=[key for key,value in sorted(generated_dict.items(), key=lambda x: x[1], reverse=True)]
    updated_nbh={}
    rank = dict([(index,item) for (item,index) in enumerate(gene_list)])
    print(gene_list)
    print("#########")
    #print("NO of singleitems:",end='')
    print(len(gene_list))
    print("#########")
    updated_transactions1,k=update_transactions1(list_of_transactions,generated_dict,gene_list)
    #print("average transaction length:",end='')
    print(k)
    print("#########")
    # print(updated_transactions1)
    # print(gene_list)
    # print(getsizeof(Tree))
    Tree = build_tree(updated_transactions1)
    q=Tree.generate_patterns([],min_sup,gene_list)
    return q


if(__name__ == "__main__"):
    path = sys.argv[1]
    outfile= sys.argv[2]
    min_sup = float(sys.argv[3])    
    k=main(path,min_sup)
    with open(outfile, 'w') as f:
        for x in k:
            f.write('%s \n'%str(x))
