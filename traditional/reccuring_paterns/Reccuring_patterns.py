import sys
import time as tm

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
        curr_node.tids=curr_node.tids | tid
        
    def get_condition_pattern(self,alpha):
        final_patterns=[]
        final_sets=[]
        final_tids=set()
        for i in self.summaries[alpha]:
            q= self.genrate_tids(i)
            set1=i.tids | q
            set2=[]
            while(i.parent.item!=None):
                set2.insert(0,i.parent.item)
                i=i.parent
            if(len(set2)>0):
                final_patterns.append(set2)
                final_sets.append(set1)
            set2=[]
        return final_patterns,final_sets


    def updated_tids(self,alpha):
        tids=set()
        for i in self.summaries[alpha]:
            tids |=self.genrate_tids(i)
        return tids
            

    def genrate_tids(self,node):
        final_tids=node.tids
        for i in node.children:
            final_tids |=self.genrate_tids(node.children[i])
        return final_tids
        
    def generate_patterns(self,prefix,per,min_ps,min_rec):
        for j in self.summaries:
            temp_ids=self.updated_tids(j)
            if(getUpperbound(temp_ids,per,min_ps,min_rec)==1):
                rec_pattern=prefix.copy()
                rec_pattern.append(j)
                if(getReccurance(temp_ids,per,min_ps,min_rec)==1):
                    yield(rec_pattern,len(temp_ids))
                patterns,tids=self.get_condition_pattern(j)
                conditional_tree=Tree()
                for pat in range(len(patterns)):
                    conditional_tree.add_transaction(patterns[pat],tids[pat])
                if(len(patterns)>=1):
                    for li in conditional_tree.generate_patterns(rec_pattern,per,min_ps,min_rec):
                        yield(li)
                    
        
        





class Node(object):
    def __init__(self, item, children):
        self.item = item
        self.children = children #dictionary of children
        self.parent = None
        self.tids = set()

    def addChild(self, node):
        self.children[node.item] = node
        node.parent = self
        





def gen_list(list_of_transactions,maxPer,min_reccur,min_ps):
    rp_dict={}
    count=0
    for i in range(len(list_of_transactions)):
        for j in range(1,len(list_of_transactions[i])):
            if list_of_transactions[i][j] not in rp_dict:
                si=1
                erec=0
                id_l=list_of_transactions[i][0]
                ps=1
                rp_dict[list_of_transactions[i][j]]=[si,erec,id_l,ps]
                count+=1
            else:
                if((int(list_of_transactions[i][0])-int(rp_dict[list_of_transactions[i][j]][2]))<maxPer):
                    rp_dict[list_of_transactions[i][j]][0]+=1
                    rp_dict[list_of_transactions[i][j]][3]+=1
                    rp_dict[list_of_transactions[i][j]][2]=list_of_transactions[i][0]
                else:
                    rp_dict[list_of_transactions[i][j]][1]+=int(rp_dict[list_of_transactions[i][j]][3]/min_ps)
                    rp_dict[list_of_transactions[i][j]][0]+=1
                    rp_dict[list_of_transactions[i][j]][3]=1
                    rp_dict[list_of_transactions[i][j]][2]=list_of_transactions[i][0]
    
    for k in rp_dict:
        rp_dict[k][1]+=int(rp_dict[k][3]/min_ps)
    rp_dict1={ k: v for k, v in rp_dict.items() if  v[1]>= min_reccur}
    rp_list=[key for key,value in sorted(rp_dict1.items(), key=lambda x: x[1][0], reverse=True)]
    return rp_list            





def buildTree(data):
    root_node=Tree()
    for i in range(len(data)):
        if(len(data[i]) > 1):
            set1=set()
            set1.add(data[i][0])
            root_node.add_transaction(data[i][1:],set1)
    return root_node    




def reordered_transactions(data,k):
    rank = dict([(index, item) for (item,index) in enumerate(k)])
    q=[]
    for i in range(len(data)):
        q.append(genCondTransactions(data[i][0], data[i][1:],rank))
    return q



def genCondTransactions(tid,basket, rank):
    filtered = [x for x in basket if x in rank.keys()]
    filtered = sorted(filtered, key=lambda x: rank[x])
    updt=[int(tid)]+filtered
    return updt



def getReccurance(tids,per,min_ps,min_rec):
    subdbs=0
    current_ps=0
    tids_final=sorted(tids)
    for i in tids_final:
        if(current_ps==0):
            current_ps=1
            start_ts=i
        else:
            if((i-ts_cur)<=per):
                current_ps+=1
            else:
                if(current_ps>=min_ps):
                    subdbs+=1
                current_ps=1
                start_ts=ts_cur
        ts_cur=i
    if(current_ps>=min_ps):
        subdbs+=1
    if(subdbs>=min_rec):
        return 1
    else:
        return 0    



def getUpperbound(tids,per,min_ps,min_rec):
    ub=0
    current_ps=0
    tids_final=sorted(tids)
    for i in tids_final:
        if(current_ps==0):
            current_ps=1
            start_ts=i
        else:
            if((i-ts_cur)<=per):
                current_ps+=1
            else:
                ub+=int(current_ps/min_ps)
                current_ps=1
        ts_cur=i
    ub+=int(current_ps/min_ps)
    if(ub>=min_rec):
        return 1
    else:
        return 0



def main(path,periodicity,min_ps,min_rec):    
    with open(path,'r') as f:
        lno=0
        list_of_transactions=[]
        for line in f:
            li=line.split()        
            list_of_transactions.append(li)
            lno=lno+1 
        f.close()
    print('the reccuring patterns are')
    total_transactions=len(list_of_transactions)
    min_reccur=int(min_rec)
    maxPer = int(periodicity)
    min_ps=(float(min_ps)*total_transactions)/100
    print(min_ps)
    rp_list=gen_list(list_of_transactions,maxPer,min_reccur,min_ps)
    print(len(rp_list))
    print(rp_list)
    final_data=reordered_transactions(list_of_transactions,rp_list)
    print(final_data[1])
    print('data is reordered')
    print(len(final_data))
    tree_root=buildTree(final_data)
    print('tree built')
    print('generating patterns')
    patterns=tree_root.generate_patterns([],periodicity,min_ps,min_rec)
    return patterns





if(__name__ == "__main__"):
    t0=tm.time()
    path = sys.argv[1]
    min_rec =int(sys.argv[2])
    min_ps=float(sys.argv[3])
    periodicity_threshold =int(sys.argv[4])
    k=main(path,periodicity_threshold,min_ps,min_rec)
    print(tm.time() - t0, "left with extracing")
    count=0
    for x in k:
        #print(x)
        count=count+1
    print (tm.time() - t0, "seconds process time")
    print("total patterns:",end="")
    print(count)
