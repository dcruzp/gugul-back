from enum import Enum
from typing import * 
from pathlib import Path
from documents import document

class ReadState(Enum):
  NEWFILE = 0
  TITLE = 1
  AUTHORS = 2
  PUB = 3
  TEXT = 4


### esto retorna una lista de docuementos
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

docs = build_cran_collection()

for doc in docs:
  print(doc.id, ':---:', doc.title[:20],': ---> ' , doc.text[:40])