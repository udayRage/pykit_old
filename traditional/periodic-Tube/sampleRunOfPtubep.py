import Ptubep as Ap

apri = Ap.Ptubep()
apri.iFile = "tubeSample"
apri.minSup = 0.001
apri.maxPer = 5

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
