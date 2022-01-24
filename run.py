from flask import Flask,jsonify
from time import sleep

from document_handler import DocumentsHandler
from documents import DOCUMENTS

app = Flask(__name__)

doc_handler = DocumentsHandler(DOCUMENTS)


@app.route("/api/v1/query/<q>")
def SearchQ(q):
    
    #buscar los documentos mas similares a q
    sol = [
        {"value":d[0],"title": "TheTitle", "id":d[1]["id"], "preview":d[1]["text"][0:min(20,len(d[1]["text"]))]+"..."}
        for d in doc_handler.get_sim(q) 
        if d[0] != 0
    ]
    
    print(">>>>>>>>>>>>>>", q)
    print(sol)

    
    response = jsonify( sol )

    response.headers.add('Access-Control-Allow-Origin', '*')
    return response        

@app.route("/api/v1/document/<int:index>")
def SeeDocument(index):

    response = jsonify({ 
        "title": DOCUMENTS[index]["title"],
        "body":DOCUMENTS[index]["text"],
        "id": DOCUMENTS[index]["id"]
    })

    response.headers.add('Access-Control-Allow-Origin', '*')

    return response
    
app.run(debug=True)
