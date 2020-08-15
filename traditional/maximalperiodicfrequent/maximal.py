import sys
from collections import defaultdict

path = sys.argv[1]
outfile= sys.argv[2]
periodicity = int(sys.argv[3])
minSup=int(sys.argv[4])


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
        curr_node.tids= curr_node.tids + tid
        
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
        global maximalTree,maximalItemsets
        for i in sorted(self.summaries,key= lambda x:(self.info.get(x)[0],-x)):
            pattern=prefix.copy()
            pattern.append(i)
            patterns,tids,info=self.get_condition_pattern(i)
            conditional_tree=Tree()
            conditional_tree.info=info.copy()
            head=pattern.copy()
            tail=[]
            for l in info:
                tail.append(l)
            sub=head+tail
            if(maximalTree.checkerSub(sub)==1):
                for pat in range(len(patterns)):
                    conditional_tree.add_transaction(patterns[pat],tids[pat])
                if(len(patterns)>1):
                    conditional_tree.generate_patterns(pattern)
                else:
                    #print(prefix,pattern)
                    if len(patterns)==0:
                        mappedP=[]
                        for lm in pattern:
                            mappedP.append(pfList[lm])
                        maximalTree.add_transaction(pattern)
                        maximalItemsets.append([mappedP,self.info[i]])
                    else:
                        inf=getPer_Sup(tids[0])
                        patterns[0].reverse()
                        pattern=pattern+patterns[0]
                        mappedP=[]
                        for lm in pattern:
                            mappedP.append(pfList[lm])
                        maximalTree.add_transaction(pattern)
                        maximalItemsets.append([mappedP,inf])
            self.remove_node(i)


class MNode(object):
    def __init__(self, item, children):
        self.item = item
        self.children = children

    def addChild(self, node):
        self.children[node.item] = node
        node.parent=self

class MPTree(object):
    def __init__(self):
        self.root = Node(None, {})
        self.summaries = {}
    def add_transaction(self,transaction):
        curr_node=self.root
        # #print(transaction)
        transaction.sort()
        # #print("adding",transaction)
        for i in range(len(transaction)):
            if transaction[i] not in curr_node.children:
                new_node=MNode(transaction[i],{})
                curr_node.addChild(new_node)
                if transaction[i] in self.summaries:
                    self.summaries[transaction[i]].insert(0,new_node)
                else:
                    self.summaries[transaction[i]]=[new_node]                    
                curr_node=new_node                
            else:
                curr_node=curr_node.children[transaction[i]]

    def checkerSub(self,items):
        items.sort(reverse=True)
        sitem=items[0]
        if sitem not in self.summaries:
            return 1
        else:
            if len(items)==1:
                return 0
        for t in self.summaries[sitem]:
            cur=t.parent
            i=1
            e=0
            while cur.item != None:
                if items[i]==cur.item:
                    i+=1
                    if i==len(items):
                        return 0
                cur=cur.parent
        return 1


                
maximalTree=MPTree()
maximalItemsets=[]
def getPer_Sup(tids):
    tids.sort()
    cur=0
    per=0
    sup=0
    for j in range(len(tids)):
        per=max(per,tids[j]-cur)
        if(per>periodicity):
            return [0,0]
        cur=tids[j]
        sup+=1
    per=max(per,lno-cur)
    return [sup,per]

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
    up_dict={k: v for k,v in up_dict.items() if v[0]>=minSup and v[1]<=periodicity}
    count=0
    for p in cond_pat:
        p1=[v for v in p if v in up_dict]
        trans=sorted(p1, key= lambda x: (up_dict.get(x)[0],-x), reverse=True)
        if(len(trans)>0):
            pat.append(trans)
            tids.append(cond_tids[count])
        count+=1
    return pat,tids,up_dict

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

    data={k: [v[2],v[0]] for k,v in data.items() if v[0]<=periodicity and v[2]>=minSup}
    genList=[k for k,v in sorted(data.items(),key=lambda x: (x[1][0],x[0]),reverse=True)]
    rank = dict([(index,item) for (item,index) in enumerate(genList)])
    # genList=[k for k,v in sorted(data.items(),key=lambda x: (x[1][0],x[0]),reverse=True)]
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
        set1.append(data[i][0])
        root_node.add_transaction(data[i][1:],set1)
    return root_node 
lno=0
rank={}
rank2={}
def main():
    global pfList,lno,rank2
    with open(path,'r') as f:
        list_of_transactions=[]
        for line in f:
            li=line.split() 
            list_of_transactions.append(li)
            lno+=1
        f.close()
    generated_dict,pfList=generate_dict(list_of_transactions)
    print("No. of single items:",len(pfList))
    #print(pfList)   
    updated_transactions1=update_transactions1(list_of_transactions,generated_dict,rank)
    # print(updated_transactions1)
    info={rank[k]: v for k,v in generated_dict.items()}
    list_of_transactions=[]
    Tree = build_tree(updated_transactions1,info)
    Tree.generate_patterns([])
    


if(__name__ == "__main__"):
    k=main()
    with open(outfile, 'w') as f:
        for x in maximalItemsets:
            stri=str(x[0]).replace('[','(').replace(']',')') +':'+str(x[1]).replace('[','(').replace(']',')')           
            f.write('%s \n'%stri)