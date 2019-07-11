import sys

class Node(object): # Node is class and node is its instance
    def __init__(self, item, children): #childern
        self.item = item
        self.children = children # children is dictionary; key is item name and values is a node haveing same item name
        self.parent = None # while creating node we do not assign parent
        self.freq =  0 # default frequency is 0 

    def addChild(self, node): #self (first parameter) is parent and node is a child(second parameter) and it is an instance of Node class
        self.children[node.item] = node # self.childern is dictionary, we add a item name/value as key and its node as value 
        node.parent = self # first parameter is parent


class Tree(object):
    def __init__(self):
        self.root = Node(None, {}) # takes a Null node and assigns it to root
        self.summaries = {} # summaries is dictionary; key is item name and value is a list of nodes having same item name 
    
        
    def add_transaction(self,transaction,freq): # adds transaction into the tree; tree size increases; self is Tree, transaction is list of item names; freq is the frequecy of transaction
        curr_node = self.root # curr_node contains 
        for i in range(len(transaction)): #iterate over list of item names
            if transaction[i] not in curr_node.children: # curr_node.children is a dictionary whose key is item name; 
                # if item name in transaction is not in children names add it as new child (even it has no children)
                new_node=Node(transaction[i],{}) # creates a node with no children
                curr_node.addChild(new_node) # add created node to to current node 
                if transaction[i] in self.summaries: # if item name is in summary
                    self.summaries[transaction[i]].append(new_node) # append the new node to the summary of the item name
                else: 
                    self.summaries[transaction[i]]=[new_node] # create new entry in summaries for the new item name                   
                curr_node=new_node # added node becomes the updated current node               
            else: #if item name is in chidren names
                curr_node=curr_node.children[transaction[i]] # child node becomes the current node           
            curr_node.freq+=freq # in case of fp-tree construction freq =1 ; in case of conditional tree it can be more than 1
    
    def get_condition_pattern(self,alpha): # for item name, it creates conditioanl pattern base
        final_patterns=[] # contains conditional patterns; lists of lists
        final_freqencies=[] # contains support corresponding to above conditional patterns
        #final_freq=[]
        for i in self.summaries[alpha]: # iterate over all nodes in summary of alpha item
            patfreq=i.freq # current summary node frequency equals to pattern frequency    
            cpattern=[] # contains conditional patterns of i, pattern is a list 
            while(i.parent.item!=None): # while i parent is not root
                cpattern.insert(0,i.parent.item) # insert item name at the beginning
                i=i.parent # crawls upwards in the path of the tree
            if(len(cpattern)>0): # if path length is more than zero 
                final_patterns.append(cpattern)
                final_freqencies.append(patfreq)
        return final_patterns,final_freqencies
    
    def remove_node(self,node_val): # given item name, it deletes all its nodes in the tree
        for i in self.summaries[node_val]:
            #i.parent.freq = i.parent.freq + i.freq
            # i.parent.freq = i.parent.freq + i.freq
            del i.parent.children[node_val]
            i=None

    def verify_sup(self,i): # return support of item i in the tree
    	freq=0
    	for j in self.summaries[i]:
    		freq+=j.freq
    	return freq

    #Fp-growth algorithm
    def generate_patterns(self,prefix,min_sup,genelist): #generates frequent patterns;prefix is list; prefix of frequent pattern, genelist is list of freq items
        for i in sorted(self.summaries,reverse = True): # iterate over incresing order of support of item
            sup_i=self.verify_sup(i) #gets support of item i  
            if(sup_i>=min_sup ): 
                pattern=prefix.copy() # projecte database; 
                pattern.append(genelist[i]) # add item to the pattern
                yield (pattern,sup_i)
                print(pattern)                        
                # print(pattern,pf)
                con_patterns,freq_list=self.get_condition_pattern(i) #generate condition patterns for item i
                conditional_tree=Tree() #initialize conditional tree; conditional tree is also an compressed tree
                for pat in range(len(con_patterns)): #iterate over condtion patterns
                    conditional_tree.add_transaction(con_patterns[pat],freq_list[pat]) # add conditional patterns to conditional tree
                if(len(con_patterns)>=1): # con_pattren length is not zero
                    for li in conditional_tree.generate_patterns(pattern,min_sup,genelist): #generates freq patterns from conditional tree
                        yield (li)
            self.remove_node(i) # As we are following increasing order of the freqent items, we can remove them with out any affect
    

def build_tree(data): # data is updated list of transactions
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

def update_transactions1(list_of_transactions,dict1,gene_li): #rearranging the transaction items; sorted by freq; eliminated non freq items
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
        lno=0 #number of lines
        list_of_transactions=[] # contains all transactions; transaction is a list
        for line in f:
            li=line.split() 
            list_of_transactions.append(li)
            lno=lno+1 
        f.close()
    total_transactions=len(list_of_transactions)
#     print(total_transactions)
    min_sup = (min_sup*total_transactions)/100
    print(min_sup)
    
    generated_dict=generate_dict(list_of_transactions,min_sup) #returns freq items and support; dictionary
    # print(generated_dict)
    gene_list=[key for key,value in sorted(generated_dict.items(), key=lambda x: x[1], reverse=True)] # sorts(ascending) above dict and stores their 
    rank = dict([(index,item) for (item,index) in enumerate(gene_list)]) # 
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
    q=Tree.generate_patterns([],min_sup,gene_list) #send prefix as empty
    return q


if(__name__ == "__main__"):
    path = sys.argv[1]
    outfile= sys.argv[2]
    min_sup = float(sys.argv[3])    
    k=main(path,min_sup)
    with open(outfile, 'w') as f:
        for x in k:
            f.write('%s \n'%str(x))
