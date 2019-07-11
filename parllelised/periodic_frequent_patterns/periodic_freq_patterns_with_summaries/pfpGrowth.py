import sys
from pyspark import SparkContext, SparkConf
from pfp_tree import PFPTree
import time

def func1(ps, tid):
	if ps[0] == 0 and ps[1] == 0 and ps[2] == 0:
		ps[0] = tid
		ps[1] = 0
		ps[2] = tid
		ps[3] += 1
	else:
		ps[1] = max(ps[1], tid-ps[2])
		ps[2] = tid
		ps[3] += 1
	return ps

def func2(ps1, ps2):
	ps1[1] = max(ps1[1],ps2[1],ps2[0]-ps1[2])
	ps1[2] = ps2[2]
	ps1[3] += ps2[3]
	return ps1

def func3(ps, numTrans):
	x = ps[0]
	ps = ps[1]
	ps[1] = max(ps[1], ps[0], numTrans - ps[2])
	ret = []
	ret.append(x)
	ret.append(ps)
	return ret

def getFrequentItems(data, minSupport, maxPer):
	singleItems = data.flatMap(lambda x: [(x[i],x[0]) for i in range(1, len(x))])
	ps = [0,0,0,0]
	freqItems = singleItems.aggregateByKey(ps, lambda ps1, tid: func1(ps1,tid), lambda tuple1,tuple2: func2(tuple1,tuple2))
	freqItems = freqItems.map(lambda x: func3(x, numTrans.value))
	perFreqItems = [x for (x,y) in sorted(freqItems.filter(lambda c: c[1][3] >= minSupport and c[1][1] <= maxPer).collect(), key=lambda x:-x[1][3])]
	return perFreqItems

def getFrequentItemsets(data,minSupport,maxPer,freqItems):
    rank = dict([(index, item) for (item,index) in enumerate(perFreqItems)]) 
    numPartitions = data.getNumPartitions()
    workByPartition = data.flatMap(lambda basket:genCondTransactions(basket[0], basket[1:],rank,numPartitions))
    emptyTree = PFPTree()
    forest = workByPartition.aggregateByKey(emptyTree,lambda tree,transaction: tree.add(transaction[0], [transaction[1]], 1),lambda tree1,tree2: tree1.merge(tree2))
    itemsets = forest.flatMap(lambda partId_bonsai: partId_bonsai[1].extract(minSupport, maxPer, numTrans.value, lambda x: getPartitionId(x,numPartitions) == partId_bonsai[0]))
    frequentItemsets = itemsets.map(lambda ranks_count: ([perFreqItems[z] for z in ranks_count[0]],ranks_count[1]))
    return frequentItemsets

def genCondTransactions(tid,basket, rank, nPartitions):
    filtered = [rank[int(x)] for x in basket if int(x) in rank.keys()]
    filtered = sorted(filtered)
    output = {}
    for i in range(len(filtered)-1, -1, -1):
        item = filtered[i]
        partition = getPartitionId(item, nPartitions)
        if partition not in output.keys():
            output[partition] = [filtered[:i+1], tid]
    return [x for x in output.items()]

def getPartitionId(key, nPartitions):
    return key % nPartitions


if __name__=="__main__":

    APP_NAME = "PFPGrowth"
    conf = SparkConf().setAppName(APP_NAME)
        # conf = conf.setMaster("local[*]")
    sc  = SparkContext(conf=conf)
        
    finput = sys.argv[1]
    foutput = sys.argv[2]
    threshold = float(sys.argv[3])
    periodicity_threshold = float(sys.argv[4])
    data = sc.textFile(finput, minPartitions=1).map(lambda x: [int(y) for y in x.strip().split(' ')])
        # data = sc.textFile(finput).map(lambda x: [int(y) for y in x.strip().split(' ')])
    data.cache()
    minSupport = data.count() * threshold/100
    maxPer = data.count() * periodicity_threshold/100
    numTrans = sc.broadcast(data.count())
    perFreqItems = getFrequentItems(data, minSupport, maxPer)
    freqItemsets = getFrequentItemsets(data, minSupport, maxPer, perFreqItems)
    print(freqItemsets.count())
    print(minSupport)
    print(maxPer)
    print("///////////////////////////////////////////////",type(freqItemsets))
    freqItemsets.saveAsTextFile(foutput)
        #End Spark
    sc.stop()

