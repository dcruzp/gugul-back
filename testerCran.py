from email.utils import quote
from readcrancollection import *
from typing import *
from document_handler import DocumentsHandler
from output import DocumentOutput  


#ver q esta pasando aqui :(
def tester_cran (quote = 0.5,alpha=0.5):
  print("Testing Vectorial Model (alpha=",alpha,", quote=",quote,")")

  documents:List['document'] = build_cran_collection()
  queries:defaultdict = read_cran_query()
  relevants: defaultdict = read_cran_rel()
  
  doc_handler = DocumentsHandler(documents, alpha=alpha)

 
  output = DocumentOutput()
  for query_id,query  in queries.items():
    print(query_id, end="                  \r", flush=True)
    given_docs = { d[1].id for d in doc_handler.get_sim(query,quote)}   # REC
    if (relevants.__contains__(query_id)):
      given_corr = { item[0] for item in relevants[query_id]}  # REL

    # for sorting RR
    #intersection = [ (item[0],item[1].id) for item in given_docs if item[1].id in given_corr ] # RR

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


def main():

  output = tester_cran(quote=0.25)
  output.PrintAverages()
  output = tester_cran(quote=0.45)
  output.PrintAverages() 
  output = tester_cran(quote=0.6)
  output.PrintAverages() 

  #manual_search()
  


if __name__ == '__main__':
  main()

