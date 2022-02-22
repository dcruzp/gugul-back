import math
from re import I
from matplotlib.pyplot import text

from numpy import vectorize
from sklearn import cluster

from documents import document
from typing import * 
from collections import defaultdict
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk import FreqDist

from sklearn.cluster import KMeans 
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
class DocumentsHandler:
    def __init__(self,documents : List['document'], alpha=0.5, clusters=8):
        self._global_freq = FreqDist()
        self._len = len(documents)
        self._documents:List['document'] = documents
        self._frec = []
        self._norm_frec = []
        self._alpha = alpha

        self._total_clusters=clusters
        self.vectorizer = CountVectorizer()
        self.documents_as_vectors = []
        self._calc_freq_in_all_documents()
        self.clasified_documents = [ [] for _ in range(clusters) ]
        self.kmeans = None   # instancia del clusterizador kmeans
        self._clasify_documents() 
        
        pass

    def _calc_freq_in_all_documents(self):
        for d in self._documents:
            self.add_document(d)
            
    #siendo doc un dict
    def add_document(self,doc:document):
                
        tokens = self.prepare_tokens(doc.text)
        if len(tokens)!=0:
            self.vectorizer.fit(tokens)

        freq = FreqDist(tokens)
        self._frec.append(freq)

        #adding matches to global dict
        for k, v in freq.items():
            self._global_freq[k] += 1  # sumamos uno, con esto decimos que en este documento esta ese token... 

        norm_frec = {}
        if len(freq) != 0 :
            M = freq[freq.max()]
            for k,v in freq.items():
                norm_frec[k] = v / M 

        self._norm_frec.append(norm_frec)

    def _clasify_documents(self):

        self.documents_as_vectors = np.array( [ 
            self.vectorizer.transform([" ".join(self.prepare_tokens(d.text)) ]).toarray()[0] for d in self._documents 
        ])

        self.kmeans=KMeans(n_clusters=self._total_clusters,random_state=0).fit(self.documents_as_vectors)
        #clusters_for_documents=self.kmeans.predict(self.documents_as_vectors)
        for i in range(self._len):
            centroid = self.kmeans.predict([self.documents_as_vectors[i]])[0]
            self.clasified_documents[centroid].append(i)


    def _calc_normalized_freq(self,freq : FreqDist,term):
        
        M = freq.max() 
        return freq[term.lower()]/freq[M]

    def get_frec_in_doc(self,doc_index, term):
        if self._frec[doc_index].__contains__(term.lower()):
            return self._frec[doc_index][term.lower()]
        return 0

    def weight(self, term, doc):
        if self._frec[doc].__contains__(term.lower()):
            norm_frec = self._norm_frec[doc][term.lower()]
            idf = self.inverse_document_frequency(term.lower())
            return norm_frec * idf 
        return 0

    def q_weight(self,frec ,t):
        nf = self._calc_normalized_freq(frec,t) 
        return (self._alpha + (1-self._alpha)*nf) * self.inverse_document_frequency(t)
    
    def sim(self, tokens, doc_index):
        

        freq1 = FreqDist(tokens)
        
        sum1 = 0
        sum2 = 0
        sum3 = 0
        for k,_ in freq1.items():
            doc_weith = self.weight(k,doc_index)
            qry_weith = self.q_weight(freq1,k)
            sum1 += doc_weith * qry_weith
            sum2 += doc_weith **2
            sum3 += qry_weith **2
        
        # patch
        if (math.sqrt(sum2) + math.sqrt(sum3)) == 0:
            return 0

        return sum1/(math.sqrt(sum2) + math.sqrt(sum3))

    @staticmethod
    def prepare_tokens(text):
        stopws = stopwords.words('english')
        stemmer = PorterStemmer()
        return [ stemmer.stem(s,to_lowercase=True) for s in word_tokenize(text) if s not in stopws ] 

    def get_sim(self, q, quote=0.2) ->List[tuple]:
        sol=[]

        tokens = self.prepare_tokens(q)
        q_as_vector=self.vectorizer.transform([" ".join(tokens)]).toarray()[0]
        centroid=self.kmeans.predict([q_as_vector])[0]
        for i in self.clasified_documents[centroid] :
            # ordenar cada documento por orden de relevancia con q 
            value = self.sim(tokens,i) 
            if value > quote:
                sol.append((value, self._documents[i])) 
        sol.sort(reverse=True,key=lambda t:t[0])    
        return sol

    def inverse_document_frequency(self,term : str):
        frequency = self._global_freq[term]    # no es en la cantidad de documentos en los que aparece el termino????
        return 0 if frequency==0 else math.log10(self._len/frequency)

