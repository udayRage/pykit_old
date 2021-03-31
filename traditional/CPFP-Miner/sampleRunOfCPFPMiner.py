import CPFPMiner as Ap

apri = Ap.CPFPMiner(r"/home/apiiit-rkv/Downloads/aprioriFinal/sample", 0.2, 0.9)

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
