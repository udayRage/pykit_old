import sys
from collections import defaultdict
import time
# import psutil
# import os
def defaultvalue():
    return [[],[]]
def defaultvalue1():
    return [[],[],[]]
input_file=open(sys.argv[1])
period=int(sys.argv[2])
minSup=int(sys.argv[3])
outfile=open(sys.argv[4],'w')
mu = input("Enter no of membership terms: ") 
# process = psutil.Process(os.getpid())
mt=[]
for k in range(int(mu)):
    v=input("enter member-ship term: ")
    mt.append(int(v))
# print(mt)
start_time = time.time()
maxts=0
d = defaultdict(defaultvalue)
for i in input_file:
    i=i.strip('\n')
    li=i.split(' ')
    k=li[1].split(',')
    for j in k:
        v=j.split(':')
        d[v[0]][0].append(int(li[0]))
        d[v[0]][1].append(float(v[1]))
    maxts+=1
# print("without fl %s seconds ---" % (time.time() - start_time))
d1 = defaultdict(defaultvalue1)
def getMem(value):
    for i in range(len(mt)):
        if value<=mt[i]:
            if(i-1>=0):
                return [i-1,i],[(mt[i]-value)/(mt[i]-mt[i-1]),(value-mt[i-1])/(mt[i]-mt[i-1])]
            else:
                return [i-1,i],[0,1]
    return [i-1,i],[0,1]
for i in d:
    si=len(d[i][1])
    for j in range(si):
        m1,m2=getMem(d[i][1][j])
        for k in range(len(m1)):
            if(m2[k]!=0):
                st=i+'#'+str(m1[k])
                d1[st][0].append(d[i][0][j])
                d1[st][1].append(m2[k])
                d1[st][2].append(0)
#print("without fl %s seconds ---" % (time.time() - start_time))
def get_Sup(lists,ind):
    return round(sum(lists[ind]),3)
def chkPeriod(li2):
    chk=1
    cur=0
    for q in range(len(li2)):
        if li2[q]-cur>period:
            chk=0
            return chk
        cur=li2[q]
    if (maxts-cur)>period:
        chk=0
    return chk
psItems=[]
psDict={}
for key in d1:
    psDict[key]=get_Sup(d1[key],1)
# print(psDict)
#print("without fl %s seconds ---" % (time.time() - start_time))
for i in psDict:
    if psDict[i]>=minSup:
        if chkPeriod(d1[i][0])==1:
            psItems.append(i)
#print("psItems %s seconds ---" % (time.time() - start_time))
rm_li=[]
for k in d1:
    # print(k)
    if k not in psItems:
        rm_li.append(k)
d={}
for ky in rm_li:
    del d1[ky]
def func(value):
    return psDict[value]
psItems=sorted(psItems,key=func)

# print(psItems)

def update(i,j):
    global d1
    for p in range(len(d1[i][0])):
        for q in range(len(d1[j][0])):
            if d1[i][0][p] == d1[j][0][q]:
                d1[i][2][p]=max(d1[i][2][p],d1[j][1][q])
                break
            else:
                if d1[i][0][p] < d1[j][0][q]:
                    break
    

updatedpsItems=[]
psItems.reverse()
# print(psItems)
rem=[]
for i in psItems:
    j=i.split('#')
    if j[0] not in rem:
        updatedpsItems.append(i)
        rem.append(j[0])
# print(i)
# print("delting rep %s seconds ---" % (time.time() - start_time))
updatedpsItems.reverse()   
si=len(updatedpsItems)
#print(si)
for i in range(si):
    for j in range(i+1,si):
        k1=updatedpsItems[i]
        k2=updatedpsItems[j]
        # print(i,j)
        for p in range(len(d1[k1][0])):
            for q in range(len(d1[k2][0])):
                if d1[k1][0][p] == d1[k2][0][q]:
                    d1[k1][2][p]=max(d1[k1][2][p],d1[k2][1][q])
                    break
                else:
                    if d1[k1][0][p] < d1[k2][0][q]:
                        break
# print(d1)updatedpsItem
# print("modified %s seconds ---" % (time.time() - start_time))
def merge(cur_table,lists):
    rl=[[],[],[]]
    if len(cur_table)==0:
        return lists.copy()
    else:
        for i in range(len(cur_table[0])):
            for j in range(len(lists[0])):
                if cur_table[0][i]==lists[0][j]:
                    rl[0].append(cur_table[0][i])
                    rl[1].append(min(cur_table[1][i],lists[1][j]))
                    rl[2].append(lists[2][j])
                    break
                else:
                    if cur_table[0][i] < lists[0][j]:
                        break
    return rl 
# print(d1)
def extract(items,prefix,cur_table):
    while items:
        i=items.pop()
        it_sent=items.copy()
        cur_table1 = merge(cur_table,d1[i])
        ps=get_Sup(cur_table1,1)
        if ps >= minSup:
            if chkPeriod(cur_table1[0])==1:
                yield prefix+[i],ps
                ub=get_Sup(cur_table1,2)
                if ub >= minSup:
                    for fuz in extract(it_sent,prefix+[i],cur_table1):
                        yield fuz



# print(updatedpsItems)
updatedpsItems.reverse()
print(updatedpsItems)
for pat in extract(updatedpsItems,[],[]):
    outfile.write('%s\n'%str(pat))
outfile.close()
print("--- %s seconds ---" % (time.time() - start_time))
# print(process.memory_info().rss)
