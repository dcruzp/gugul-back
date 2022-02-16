import math
from re import I
import nltk
from documents import document
from typing import * 
from collections import defaultdict
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

class DocumentsHandler:
    def __init__(self,documents : List['document'], alpha=0.5):
        self._global_freq = nltk.FreqDist()
        self._len = len(documents)
        self._documents:List['document'] = documents
        self._frec = []
        self._norm_frec = []
        self._calc_freq_in_all_documents()
        self._alpha = alpha
        pass

    def _calc_freq_in_all_documents(self):
        for d in self._documents:
            self.add_document(d)
            
    #siendo doc un dict
    def add_document(self,doc:document):
        #print(doc)
        # tokens = [ s.lower() for s in doc.text.split()]
        tokens = word_tokenize(doc.text)

        # eliminando los stopwords
        clean_tokens = tokens[:]
        for token in tokens:
            if token in stopwords.words('english'):
                clean_tokens.remove(token)

        #lematizar
        stemmer_tokens = [] 
        stemmer = PorterStemmer()
        for token in clean_tokens:
            stemmer_tokens.append(stemmer.stem(token,to_lowercase=True))
        

        freq = nltk.FreqDist(stemmer_tokens)
        self._frec.append(freq)

        #adding matches to global dict
        for k , v in freq.items():
            self._global_freq[k] += v

        norm_frec = {}
        try:
            M = freq.max() 
            for k,v in freq.items():
                norm_frec[k] = v / freq[M]
        except Exception:
            pass
        self._norm_frec.append(norm_frec)

    def _calc_normalized_freq(self,freq,term):
        
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
        f = self._calc_normalized_freq(frec,t) 
        return (self._alpha + (1-self._alpha)*f) * self.inverse_document_frequency(t)
    
    def sim(self, q, doc_index):
        #tokens = [ s.lower() for s in q.split() ]

        stopws = stopwords.words('english')
        stemmer = PorterStemmer()

        # tomamos los primitivos de las palabras en minuscula que no esten en las stopwords...
        tokens = [ stemmer.stem(s,to_lowercase=True) for s in word_tokenize(q) if s not in stopws ] 

        freq1 = nltk.FreqDist(tokens)
        
        sum1 = 0
        sum2 = 0
        sum3 = 0
        for k,v in freq1.items():
            doc_weith = self.weight(k,doc_index)
            qry_weith = self.q_weight(freq1,k)
            sum1 += doc_weith * qry_weith
            sum2 += doc_weith **2
            sum3 += qry_weith **2
        
        # patch
        if (math.sqrt(sum2) + math.sqrt(sum3)) == 0:
            return 0

        return sum1/(math.sqrt(sum2) + math.sqrt(sum3))

    def get_sim(self, q, quote=0.1) ->List[tuple]:
        sol=[]
        for i in range(self._len):
            # ordenar cada documento por orden de relevancia con q 
            value = self.sim(q,i) 
            if value > quote:
                sol.append((value, self._documents[i])) 
        sol.sort(reverse=True,key=lambda t:t[0])    
        return sol

    def inverse_document_frequency(self,term : str):
        # frequency =0
        # for d in self.documents:
        #     if term in d.text:
        #         frequency+=1
        frequency = self._global_freq[term]
        return 0 if frequency==0 else math.log10(self._len/frequency)

