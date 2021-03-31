import pfgrowth as Ap

apri = Ap.Pfgrowth()
apri.iFile = "T10I4D100K.txt"
apri.minSup = 0.001
apri.maxPer = 0.02

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
