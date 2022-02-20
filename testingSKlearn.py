from sklearn.cluster import KMeans 
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import numpy as np

corpus=[
    'This is the first document.',
    'This is the second document',
    'And the third one.',
    'Is this the first document?',
]

vectorizer = CountVectorizer()
#transformer= TfidfTransformer()

#vec1 = vectorizer.fit(corpus)
vec = vectorizer.fit_transform(corpus)
#vectorizer.fit(["asd"])

print(vectorizer.vocabulary_)  # para obtener la representacion en diccionario de cada palabra como un numero
print(vec.toarray())



X = vec.toarray() 

kmeans = KMeans(n_clusters=2, random_state=0).fit(X) 
centroids = kmeans.cluster_centers_  # centroids calculados por kmeans

#print(vectorizer.inverse_transform(centroids))

q = "This second document"

vecQ = vectorizer.transform([q]).toarray()

print(kmeans.predict(X)[0])


#plt.scatter(X[:,0],X[:,1])
#plt.scatter(centroids[:,0],centroids[:,1])
#plt.show()







