import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

url = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"

plt.style.use("dark_background")

# load dataset into Pandas DataFrame
df = pd.read_csv(
    url, names=["sepal length", "sepal width", "petal length", "petal width", "target"]
)


features = ["sepal length", "sepal width", "petal length", "petal width"]

# Separating out the features
x = df.loc[:, features].values

# Separating out the target
y = df.loc[:, ["target"]].values

# Standardizing the features
x = StandardScaler().fit_transform(x)

pca = PCA(n_components=2)

principalComponents = pca.fit_transform(x)

principalDf = pd.DataFrame(
    data=principalComponents,
    columns=np.array(["principal component 1", "principal component 2"]),
)

finalDf = pd.concat([principalDf, df[["target"]]], axis=1)
fig, ax = plt.subplots()
ax.set_xlabel("Principal Component 1")
ax.set_ylabel("Principal Component 2")
ax.set_title("2 component PCA")

# We center the data and compute the sample covariance matrix.
x_centered = x - np.mean(x, axis=0)
cov_matrix = np.dot(x_centered.T, x_centered) / finalDf["target"].size
eigenvalues = pca.explained_variance_ratio_
for eigen_value in eigenvalues:
    print(eigen_value)
targets = ["Iris-setosa", "Iris-versicolor", "Iris-virginica"]
colors = ["r", "g", "b"]
for target, color in zip(targets, colors):
    indicesToKeep = finalDf["target"] == target
    ax.scatter(
        finalDf.loc[indicesToKeep, "principal component 1"],
        finalDf.loc[indicesToKeep, "principal component 2"],
        c=color,
        s=50,
    )
ax.legend(targets)
ax.grid()

plt.show()
