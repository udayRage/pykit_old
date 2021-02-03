import random
import pandas as pd

inputFileContainingNoClassLabel = 'processedData.csv'
df = pd.read_csv(inputFileContainingNoClassLabel, header=None)
rows, columns = df.shape
randomList = []

noOfClassLabels = 4
for i in range(0, rows):
    n = random.randint(1, noOfClassLabels)
    randomList.append(n)

df["classLabel"] = randomList

df.to_csv("dataWithClass.csv", index=False, header=False)
