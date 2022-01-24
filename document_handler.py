import math
import nltk

class DocumentsHandler:
    def __init__(self,documents, alpha=0.5):
        self.documents = documents
        self._frec = []
        self._norm_frec = []
        self._calc_freq_in_all_documents()
        self._alpha = alpha
        pass

    def _calc_freq_in_all_documents(self):
        for d in self.documents:
            self.add_document(d)        
            
    #siendo doc un dict
    def add_document(self,doc):
        print(doc)
        tokens = [ s.lower() for s in doc["text"].split() ]
        freq = nltk.FreqDist(tokens)
        self._frec.append(freq)

        M = freq.max() 
        norm_frec = {}
        for k,v in freq.items():
            norm_frec[k] = v / freq[M]
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
        tokens = [ s.lower() for s in q.split() ]
        freq1 = nltk.FreqDist(tokens)
        
        sum1 = 0
        sum2 = 0
        sum3 = 0
        for k,v in freq1.items():
            sum1 += self.weight(k,doc_index) * self.q_weight(freq1,k)  
            sum2 += self.weight(k,doc_index)**2
            sum3 += self.q_weight(freq1,k)**2
        
        # patch
        if (math.sqrt(sum2) + math.sqrt(sum3)) == 0:
            return 0

        return sum1/(math.sqrt(sum2) + math.sqrt(sum3))

    def get_sim(self, q):
        sol=[]
        for i in range(len(self.documents)):
            # ordenar cada documento por orden de relevancia con q 
            value = self.sim(q,i) 
            sol.append((value, self.documents[i])) 
        sol.sort(reverse=True,key=lambda t:t[0])    
        return sol

    def inverse_document_frequency(self,term : str):
        frequency =0
        for d in self.documents:
            if term in d["text"]:
                frequency+=1
        return 0 if frequency==0 else math.log10(len(self.documents)/frequency)

