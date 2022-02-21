
class document:
  def __init__(self,id:int, title:str, author:str, pub:str, text:str) -> None:
    self.id = id
    self.title = title.lower()
    self.author = author.lower()
    self.pub = pub.lower()
    self.text = text.lower()
