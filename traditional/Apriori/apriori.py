import time
import os
import psutil


def candidate2FrequentItems(cList):
    dicts = {}
    for j in trans:
        for i in cList:
            if i.issubset(j):
                dicts[frozenset(i)] = dicts.get(frozenset(i), 0) + 1
    dicts = {k: v for k, v in dicts.items() if v >= minSup}
    return dicts


def frequent2CandidateItems(fList, length):
    c2 = []
    for i in fList:
        for j in fList:
            k = j.union(i)
            if len(k) == length:
                if k not in c2:
                    c2.append(k)
    return sorted(c2)


minSup = float(2000)


filename = "/Users/ravi/PycharmProjects/pami_pykit/Datasets/transactionalDatabase/transactional_T10I4D100K.csv"
# "T10I4D100K.csv"
startTime = time.time()
with open(filename, 'r') as f:
    trans = []
    for line in f:
        li = line.split()
        trans.append(set(li))
    f.close()

listOfItems = sorted(list(set.union(*trans)))
items = []
for i in listOfItems:
    j = {i}  # set([i])
    items.append(j)
noOfItems = len(items)
finalFps = {}

for i in range(1, noOfItems):
    fList = candidate2FrequentItems(items)
    print("\nFrequent Items of length:", i, "\n-----------------------------")
    if len(fList) == 0:
        print("None")
    for fi in fList:
        print(sorted(fi), " Support Count = ", fList[fi])
    finalFps.update(fList)
    cList = frequent2CandidateItems(fList, i + 1)
    if len(cList) == 0:
        print("\n-*-*-*-End of Frequent Item sets-*-*-*-")
        break
    # print("\nCandidate Items of length:",i+1,"\n-----------------------------")
    for ci in cList:
        print(sorted(list(ci)))
print("Total number of patterns:", len(finalFps))
