import Corelfpgrowth as Ap

apri = Ap.Corelfpgrowth(r"/home/apiiit-rkv/Desktop/Feb/FpGrowth/inp.csv","outFile", 0.009,0.8)

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


