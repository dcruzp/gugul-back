DOCUMENTS =[
  {"id":0,"title":"Title", "text":"Hola my friend me llamo jose jose y esta es mi historia",},
  {"id":1,"title":"Title", "text":"hola wenas me llamo rodolfo nariz",},
  {"id":2,"title":"Title", "text":"guasa papus  me llamo tuxi el grande",},
]

class ducument:
  def __init__(self,id:int, title:str, autor:str, pub:str, text:str) -> None:
    self.id = id
    self.title = title.lower()
    self.autor = autor.lower()
    self.pub = pub.lower()
    self.text = text.lower()