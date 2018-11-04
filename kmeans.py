#importing needed libraries
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import CountVectorizer
# including test files as a single unit in an excel file
data = pd.read_excel('textfiles.xlsx')

# selecting the first column of the excel file that has textfile's data
idea = data.iloc[:, 0:1]

#saving all the rows in the testfiles excel file as documents with each document containing many sentences
corpus = []
for index, row in idea.iterrows():
    corpus.append(row['Idea'])

#vectorizing each document and forming the TF.IDF matrix
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(data['Idea'].values.astype(str))
transformer = TfidfTransformer(smooth_idf=False)
tfidf = transformer.fit_transform(X)
print(tfidf)
print("Size of the TF.IDF matrix: ",tfidf.shape)

#defining no of clusters and clustering the data
num_clusters = 4
km = KMeans(n_clusters=num_clusters)
km.fit(tfidf)
clusters = km.labels_.tolist()

# Creating dict having doc with the corresponding cluster number and convting it into a dataframe
idea = {'Content': corpus, 'Cluster': clusters}
frame = pd.DataFrame(idea, index=[clusters], columns=['Content', 'Cluster'])

#printing each document and its respective clsuter
print("\nContent of each document and its resective cluster:\n")
print('-------------------------------------------------------')
print(frame)

#printing the size of each cluster
print("\nCluster no. and the number of text documents under it are:\n")
print('--------------------------------------------------------------')
print(frame['Cluster'].value_counts())
