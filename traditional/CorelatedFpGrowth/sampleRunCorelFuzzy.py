import corel_fuzzy as Ap
apri =Ap.AlgoCorelFFI("inp","outp",4,0.2)

apri.startMine()

memRSS = apri.getMemoryRSS()

print("Total Memory in RSS", memRSS)

run = apri.getRuntime()

print("Total ExecutionTime in seconds:", run)


