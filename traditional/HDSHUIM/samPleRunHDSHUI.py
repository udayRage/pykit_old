import HDSHUIM as Ap
import sys
apri = Ap.SHDSHUIs(sys.argv[1],sys.argv[2],sys.argv[3],int(sys.argv[4]))
apri.startMine()

memRSS = apri.getMemoryRSS()

print("Total Memory in RSS", memRSS)

run = apri.getRuntime()

print("Total ExecutionTime in seconds:", run)


