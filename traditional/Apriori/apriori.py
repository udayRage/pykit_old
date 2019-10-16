#!/usr/bin/env python
# coding: utf-8

# In[1]:


from itertools import combinations

def Canditalist_to_Frequentlist(a):
    dicts = {}
    for j in trans:
        for i in a:
            if i.issubset(j):
                dicts[frozenset(i)]=dicts.get(frozenset(i),0)+1
    dicts = {k: v for k, v in dicts.items() if v >= minsup}
    return dicts

def Frequentlist_to_Candidatelistgen(a,length):
    c2 = []
    for i in a:
        for j in a:
            k = j.union(i)
            if len(k)==length:
                if k not in c2:
                    c2.append(k)
    return sorted(c2)


# In[2]:


minsup = float(1000)


# In[3]:


filename = "T10I4D100K.csv"

with open(filename,'r') as f:
    trans=[]
    for line in f:
        li=line.split() 
        trans.append(set(li))
    f.close()

itemslist = sorted(list(set.union(*trans)))
items = []
for i in itemslist:
    j = set([i])
    items.append(j)
itrs = len(items)
fsets = {}


# In[ ]:


#Apriori
#print("\nCandidate Items of Length: 1\n-----------------------------")
#for ci in items:
    #print(list(ci))
for i in range(1,itrs):
    l = Canditalist_to_Frequentlist(items)
    print("\nFrequet Items of length:",i,"\n-----------------------------")
    if len(l)==0:
        print ("None")
    for fi in l:
        print(sorted(fi)," Support Count = ",l[fi])
    fsets.update(l)
    items = Frequentlist_to_Candidatelistgen(l,i+1)
    if len(items)==0:
        print("\n-*-*-*-End of Frequent Item sets-*-*-*-")
        break
    #print("\nCandidate Items of length:",i+1,"\n-----------------------------")
    for ci in items:
        print(sorted(list(ci)))     

