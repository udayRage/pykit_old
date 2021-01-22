import time
import sys
import os
import psutil


def candidateListToFrequentList(candidateList):
    frequentSetSup = {}
    for transactionItems in transaction:
        dictionary = {frozenset(candidateSet): int(frequentSetSup.get(frozenset(candidateSet), 0))+1
                      for candidateSet in candidateList if candidateSet.issubset(transactionItems)}
        frequentSetSup.update(dictionary)
    frequentSetSup = {key: value for key, value in frequentSetSup.items() if value >= minSupport}
    return frequentSetSup


def frequentListToCandidateList(frequentList, length):
    candidateList = []
    # candidateList = [set(c) for c in combinations(a,length) if c not in candidateList]
    for item1 in frequentList:
        temporaryList = [item1 | item2 for item2 in frequentList if len(item1 | item2) == length
                         and (item1 | item2) not in candidateList]
        candidateList.extend(temporaryList)
        
    return sorted(candidateList)


startTime = time.time()
inputFileName = (sys.argv[1])
outputFileName = (sys.argv[2])
with open(inputFileName, 'r') as file:
    transaction = [set(line.split()) for line in file]

itemsList = sorted(list(set.union(*transaction)))
items = [{item} for item in itemsList]
itemsLength = len(items)
frequentSets = {}
numberOfFrequent = {}
totalFrequentSet = 0
lengthOfLastFrequentSet = 0
minSupport = float(sys.argv[3])
# support_counter = [[0 for x in range(1000)] for y in range(1000)]

file = open(outputFileName, 'w+')
print(minSupport)
# f.write('{0}\n'.format(minSupport))
for i in range(1, itemsLength):
    frequentItemSets = candidateListToFrequentList(items)
    if len(frequentItemSets) == 0:
        print("No frequentPatterns")
    numberOfFrequent[i] = len(frequentItemSets)
    for frequentSet in frequentItemSets:
        file.write('{0}, Support Count = {1}\n'.format(sorted(frequentSet), frequentItemSets[frequentSet]))
        # print(sorted(li)," Support Count = ",l[li])
    frequentSets.update(frequentItemSets)
    items = frequentListToCandidateList(frequentItemSets, i + 1)
    if len(items) == 0:
        lengthOfLastFrequentSet = i
        print("End of Frequent Item Sets")
        break
        # finish apriori

process = psutil.Process(os.getpid())
memory = process.memory_full_info().uss
memoryInMB = memory / (1024 * 1024)
print("Total Memory consumed by the program is:", memoryInMB)

for i in range(1, lengthOfLastFrequentSet + 1):
    print('f{0} = {1}'.format(i, numberOfFrequent[i]))
    totalFrequentSet = totalFrequentSet + numberOfFrequent[i]
print('total items = {0}'.format(totalFrequentSet))
print('total execution time = {0}'.format(time.time() - startTime))
file.close()
