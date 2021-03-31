import Spatial_Eclat as Ap

apri = Ap.Eclart("input.txt","neighbouts.txt",5)
apri.startMine()

frequentPatterns = apri.getFrequentPatterns()

print("Total number of Spatial Frequent Patterns:", len(frequentPatterns))

apri.storePatternsInFile("outFile")

memUSS = apri.getMemoryUSS()

print("Total Memory in USS:", memUSS)

memRSS = apri.getMemoryRSS()

print("Total Memory in RSS", memRSS)

run = apri.getRuntime()

print("Total ExecutionTime in seconds:", run)


