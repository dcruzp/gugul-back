import path_adder
from output import DocumentOutput  
from collection_reader.readcrancollection import *
from typing import *
from document_handler import DocumentsHandler

##
## cqr = (document_collection, queries, relevant_queries)
##
def tester (cqr ,quote = 0.45,alpha=0.5, clusters=4):
  print("Testing Vectorial Model (alpha=",alpha,", quote=",quote,", clusters=",clusters,")")

  documents,queries,relevants = cqr 
  
  print("Procesando Documentos....", flush=True,end=" ")
  doc_handler = DocumentsHandler(documents, alpha=alpha,clusters=clusters)
  print("DONE!")
 
  output = DocumentOutput()
  for query_id,query  in queries.items():
    print(query_id, end="                  \r", flush=True)

    given_docs = { d[1].id for d in doc_handler.get_sim(query,quote)}   # REC
    if (relevants.__contains__(query_id)):
      given_corr = { item[0] for item in relevants[query_id] }  # REL


    RR = given_corr & given_docs
    NR = given_corr - RR
    RI = given_docs - RR

    #print("id:",query_id,": (",len(RR),"/",len(given_corr),") RI:",len(RI))

    output.RR.append(RR) 
    output.NR.append(NR) 
    output.RI.append(RI) 

  return output



def manual_search():


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

