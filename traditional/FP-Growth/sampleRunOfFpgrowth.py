import fpgrowth as Ap

apri = Ap.Fpgrowth(r"/home/apiiit-rkv/Downloads/aprioriFinal/transactional_T10I4D100K.csv", 0.009)

apri.startMine()

frequentPatterns = apri.getFrequentPatterns()

print("Total number of Frequent Patterns:", len(frequentPatterns))

apri.storePatternsInFile("outFile")

# Df = apri.getPatternInDf()

memUSS = apri.getMemoryUSS()

print("Total Memory in USS:", memUSS)

memRSS = apri.getMemoryRSS()

print("Total Memory in RSS", memRSS)

run = apri.getRuntime()

print("Total ExecutionTime in seconds:", run)


