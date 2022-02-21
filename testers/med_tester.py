from tester import tester
from collection_reader.readmedcollection import *
from typing import *

def run_tests():
  print("Probando med_collection...")

  documents:List['document'] = build_med_collection()
  queries:defaultdict = read_med_query()
  relevants: defaultdict = read_med_rel()

  cqr = (documents,queries,relevants)

  output = tester(cqr,clusters=4,quote=0.30)
  output.PrintAverages() 

if __name__ == "__main__":
    run_tests()