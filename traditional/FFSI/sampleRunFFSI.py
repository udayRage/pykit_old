import FSFI as Ap
apri =Ap.AlgoFFSHUIM("input_paper","nigbbs","outp",5)

apri.startMine()

memRSS = apri.getMemoryRSS()

print("Total Memory in RSS", memRSS)

run = apri.getRuntime()

print("Total ExecutionTime in seconds:", run)


