from enum import Enum
from pprint import pprint
from typing import * 
from pathlib import Path
from documents import document
from collections import defaultdict
import typer

class ReadState(Enum):
  NEWFILE = 0
  TITLE = 1
  AUTHORS = 2
  PUB = 3
  TEXT = 4



def build_cran_collection()-> List['document']:

  docs: List[document] = []
  texts: List[str] = [] 
  cran_file = Path("./test_collections/cran/cran.all.1400")

  if not cran_file.exists():
    raise FileNotFoundError(f"{cran_file} does not exist")

  header_state = {
    ".I": ReadState.NEWFILE,
    ".T": ReadState.TITLE,
    ".A": ReadState.AUTHORS,
    ".B": ReadState.PUB,
    ".W": ReadState.TEXT,
  }

  with open(cran_file, "r") as cran_f:
    state = None
    title, authors , pub , text = [] ,[] ,[] ,[]
    doc_id = None
    for line in cran_f:
      in_header = False
      for header, stt in header_state.items():
        if line.startswith(header):
          state= stt
          in_header = True
          break
      
      if state == ReadState.NEWFILE:
        if doc_id is not None:

          id = int(doc_id)
          docs.append(document( id = id, 
                                title= " ".join(title), 
                                author=" ".join(authors), 
                                pub=" ".join(pub),
                                text= " ".join(text))
                      )

          assert id == len(docs)
          texts.append(" ".join(text))
          title , authors, pub , text = [], [], [], []
        doc_id = line[3:-1]
      
      if state is None or in_header:
        continue
      if state ==ReadState.TITLE:
        title.append(line.strip())
      elif state == ReadState.AUTHORS:
        authors.append(line.strip())
      elif state == ReadState.PUB:
        pub.append(line.strip())
      elif state == ReadState.TEXT:
        text.append(line.strip())
  
  id = int(doc_id)
  docs.append(document( id = id, 
                        title= " ".join(title), 
                        author=" ".join(authors), 
                        pub=" ".join(pub),
                        text= " ".join(text))
                      )
  return docs 



# esta es para leer todas las querys de los documentos 
# que hay en el fichero de  querys que esta indexadas 
# como mismo estan el el documento 
def read_cran_query() -> defaultdict:
  queries_file = Path("./test_collections/cran/cran.qry")
  relevants_file = Path("./test_collections/cran/cranqrel")
  if not queries_file.exists():
    raise typer.Exit(f"{queries_file} does not exist.")
  if not relevants_file.exists():
    raise typer.Exit(f"{relevants_file} does not exist.")

  typer.echo('Parsing querys ....')
  queries = defaultdict(str) 
  with open(str(queries_file),'r') as qry_f:
    query_text = []
    qry_id = None
    trulest_id = 1   # id asociado a la posicion de aparicion 
    for line in qry_f:
      if line.startswith('.I'):
        if query_text:
          # queries.append(" ".join(query_text))
          #queries[int(qry_id)] = " ".join(query_text)
          queries[trulest_id] = " ".join(query_text)  # usamos el id asociado a la posicion de aparicion
          trulest_id+=1
          query_text = []

        qry_id = line[3:-1]
        continue
      if line.startswith('.W'):
        continue
      if line.strip() != "":
        query_text.append(line.strip())
    if query_text:
      #queries[int(qry_id)] = " ".join(query_text)
      queries[int(qry_id)] = " ".join(query_text)
  return queries

# esto es para leer las relevancias de cada documento
# para cada una d elas querys 
def read_cran_rel() -> defaultdict:
  relevants_file = Path("./test_collections/cran/cranqrel")

  typer.echo('Parsing relevants ....')
  relevants = defaultdict(int)

  with open (str(relevants_file),'r')as rel_f:
    for line in rel_f:
      query , doc_id, rel = [int(item) for item in line.split()]
      if query not in relevants : 
        relevants[query] = [(doc_id,rel)]
      else:
        relevants[query].append((doc_id,rel))

  return relevants

#querys = read_cran_query()
#for k , v in querys.items():
#  print (k, ' -> ', v)