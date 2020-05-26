import sys
from pyspark import SparkContext, SparkConf
from fpTree import FPTree

def getFrequentItems(data,minSupport):
    singleItems = data.flatMap(lambda x: [(y,1) for y in x])
    freqItems = [x for (x,y) in sorted(singleItems.reduceByKey(lambda x,y: x+y).filter(lambda c: c[1]>=minSupport).collect(), key=lambda x: -x[1])]
    return freqItems

def getFrequentItemsets(data,minSupport,freqItems):
    rank = dict([(index, item) for (item,index) in enumerate(freqItems)]) # Ordered list based on the freequncy of items, the first is the most appearing one , the last is not appearing too much.
    numPartitions = data.getNumPartitions()
    workByPartition = data.flatMap(lambda basket: genCondTransactions(basket,rank,numPartitions))
    emptyTree = FPTree()
    forest = workByPartition.aggregateByKey(emptyTree,lambda tree,transaction: tree.add(transaction,1),	lambda tree1,tree2: tree1.merge(tree2))
    itemsets = forest.flatMap(lambda bonsai_tuple: bonsai_tuple[1].extract(minSupport, lambda x: getPartitionId(x,numPartitions) == bonsai_tuple[0]))
    frequentItemsets = itemsets.map(lambda ranks_count: ([freqItems[z] for z in ranks_count[0]],ranks_count[1]))
    return frequentItemsets

def genCondTransactions(basket, rank, nPartitions):
    #translate into new id's using rank
    filtered = [rank[int(x)] for x in basket if int(x) in rank.keys()]
    #sort basket in ascending rank
    filtered = sorted(filtered)
    #subpatterns to send to each worker. (part_id, basket_slice)
    output = {}
    for i in range(len(filtered)-1, -1, -1):
        item = filtered[i]
        partition = getPartitionId(item, nPartitions)
        if not partition in output.keys():
            output[partition] = filtered[:i+1]
    return [x for x in output.items()]

def getPartitionId(key, nPartitions):
    return key % nPartitions

def runFPGrowth(data, minSupport):
    freqItems = getFrequentItems(data, minSupport)
    freqItemsets = getFrequentItemsets(data, minSupport, freqItems)
    return freqItemsets



if __name__=="__main__":

    APP_NAME = "FPGrowth"

    conf = SparkConf().setAppName(APP_NAME)
    # conf = conf.setMaster("local[*]")


    sc  = SparkContext(conf=conf)
    sc.addFile("fpTree.py");
    # sc.setLogLevel("ERROR")

    finput = sys.argv[1]
    foutput = sys.argv[2]
    # file = open("output.txt",'w+')
    threshold = float(sys.argv[3])

    data = sc.textFile(finput).map(lambda x: [int(y) for y in x.strip().split(' ')])

    minSupport = data.count() * threshold/100
    freqItems = getFrequentItems(data, minSupport)
    rank = dict([(index, item) for (item,index) in enumerate(freqItems)])
    numPartitions = data.getNumPartitions()
    workByPartition = data.flatMap(lambda basket: genCondTransactions(basket,rank,numPartitions))
    #samp1=workByPartition.aggregateByKey()
    #print(workByPartition.take(20))
    freqItemsets = getFrequentItemsets(data, minSupport, freqItems)
    freqItemsets.saveAsTextFile(foutput)
    #End Spark
    # file.close()
    sc.stop()
