from tester import tester
from collection_reader.readcrancollection import *
from typing import *


def run_tests():

  print("Probando cran_collection con 1,4,8 y 16 clusters...")

  documents:List['document'] = build_cran_collection()
  queries:defaultdict = read_cran_query()
  relevants: defaultdict = read_cran_rel()

  cqr = (documents,queries,relevants)

  output = tester(cqr,clusters=1)
  output.PrintAverages()
  output = tester(cqr,clusters=4)
  output.PrintAverages()
  output = tester(cqr,clusters=8)
  output.PrintAverages() 
  output = tester(cqr,clusters=16)
  output.PrintAverages() 

if __name__ == "__main__":
    run_tests()