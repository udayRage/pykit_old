Algorithm:
>>>>inputs required: temperol data file,neighbours file,minPF,maxPer,minRPS

         --->temperol data file format:
                        timestamp1 item1 item2 item3 ........(space sperated)
                        timestamp2 item1 item2 item3 ........

	 --->neighbours file format:
                        item1 neighbour(item1) neighbour(item1)......(space seperated)
                        item2 neighbour(item2) neighbour(item2)......

>>>>output: partialSpatialPeriodicPatterns
         --->output file format:
		    (output pattern1,periodic frequency,RPS)
		    (output pattern2,periodic frequency,RPS)


Way to execute:
python3 pnp.py /*InputDataFile*/ /*NeighbourFile*/ /*output path*/ /*minPF*/ /*maxPer*/ /*minRPS*/


Data file and Neighbour files are present in synthetic folder
