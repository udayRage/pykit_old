# PAMI_PyKit

PAMI_PyKit stands for PAttern MIning  Python Kit. It contains a set of python libraries to discover user interest-based patterns in very large databases. The python programs in this kit are organized in the following topics:

1.  Traditional algorithms - Conventional algorithms whose input exists in the form of transactional databases (or files).

2. Parallel algorithms - Parallel pattern mining algorithms based on Map-Reduce framework.



## Sequential algorithms
1. frequentPatternGrowth (FPgrowth)
2. multipleSupportFrequentPatternGrowth using user specified minimum item supports (MSFPgrowth) 
3. multipleSupportFrequentPatternGrowth using percentage based function (IMSFPgrowth)
4. correlatedPatternGrowth (CPgrowth)
5. periodicFrequentPattern-growth (PFPgrowth)
6. periodicFrequentPattern-growth with periodic summaries (PSgrowth)
7. ITL-growth
8. periodicFrequentPattern-growth using greedy search (PFPgrowthGS)
9. periodicFrequentPattern-growth using multiple minimum supports and maximum periodicities (MSPFP-growth)
10. periodicFrequentPattern-growth using periodic-ratio (PFPgrowthPR)
11. partialPeriodicFrequentPattern-growth using period-support (PPFPgrowth)
12. partialPeriodicFrequentPattern-growth using multiple period-supports (PPFPgrowth_MPS)
13. recurringPattern-growth (RP-growth)

14. SpatialHighUtilityItemsets 

## Parallel algorithms
1. parallelFrequentPatternGrowth
2. parallel PeriodicFrequentPatternGrowth
