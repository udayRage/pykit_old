import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

inputFileContainingPointData = "dataWithClass.csv"

df = pd.read_csv(inputFileContainingPointData, header=None)

# storing last column value in to the target variable
target = df[df.columns[-1]]
# removing last column from the dataframe
df = df[df.columns[:-1]]

# Creating a new data frame to store the point information
columns = ["First", "Last"]
newDf = pd.DataFrame(columns=columns)

# storing the point information in to the new dataframe
newDf[['First', 'Last']] = df[0].str.split(expand=True)

# dropping the point column from the data frame
df = df.drop(df.columns[0], axis=1)

# modifying the content of the new dataframe into a floats
newDf['First'] = newDf['First'].str.replace(r'POINT', '', regex=True)
newDf['First'] = newDf['First'].str.replace(r'(', '', regex=True).astype(float)
newDf['Last'] = newDf['Last'].str.replace(r')', '', regex=True).astype(float)

# elbow method starts from here
distortions = []
maximumKvalue = 15
noOfClusters = int(input("Enter the number of clusters:"))
K = range(1, maximumKvalue)
for k in K:
    kmeanModel = KMeans(n_clusters=k)
    kmeanModel.fit(df)
    distortions.append(kmeanModel.inertia_)

# plotting the elbow method result
plt.figure(figsize=(16, 8))
plt.plot(K, distortions, 'bx-')
plt.xlabel('k')
plt.ylabel('Distortion')
plt.title('The Elbow Method showing the optimal k')
plt.show()

totalClusters = 4
# fixing the number of clusters
kmeanModel = KMeans(n_clusters=totalClusters)
kmeanModel.fit(df)

# displying the results in a plot
df['k_means'] = kmeanModel.predict(df)
fig, axes = plt.subplots(1, 2, figsize=(16, 8))
axes[0].scatter(newDf['First'], newDf['Last'], c=target)
axes[1].scatter(newDf['First'], newDf['Last'], c=df['k_means'], cmap=plt.cm.Set1)
axes[0].set_title('Actual', fontsize=18)
axes[1].set_title('K_Means', fontsize=18)

plt.show()
