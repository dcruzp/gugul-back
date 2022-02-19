from readcrancollection import *
from typing import *
from document_handler import DocumentsHandler


def tester_cran ():
  documents:List['document'] = build_cran_collection()
  queries:defaultdict = read_cran_query()
  relevants: defaultdict = read_cran_rel()
  
  doc_handler = DocumentsHandler(documents)

  for query_id , query in queries.items():
    
    #given_docs = [item[1].id for item in doc_handler.get_sim(query)]
    given_docs = doc_handler.get_sim(query)
    given_corr = [item[0] for item in relevants[query_id] ]

    # print ('documentos que me devolvio el algoritmo' , given_docs)
    # print ('documentos esperados , con valores de relavancia 1 y 2',given_corr)
    intersection = [ (item[0],item[1].id) for item in given_docs if item[1].id in given_corr ] 

    #intersection = list(set(given_corr) & set(given_docs))

    #print ('para la query (',query_id,') los documentos correctos devueltos fueron \n', intersection," (",len(intersection),"/",len(given_corr),") ")
    print ('para la query (',query_id,') los documentos correctos devueltos fueron (',len(intersection),"/",len(given_corr),") -- documentos extras:",len(given_docs) - len(intersection))

def main():
  
  tester_cran()

  return

  documents:List['document'] = build_cran_collection()

  handler = DocumentsHandler(documents)
  
  while True:
        print("-"*20)
        pattern = input("Search: ")

        count = 0
        for value, doc in handler.get_sim(pattern):
            if value == 0:
                break
            count += 1
            print("(",value,")  id (",doc.id,") -- | ",doc.text[:40])
        print(count)
        print()
        print("busqueda finalizada :D")



if __name__ == '__main__':
  main()

