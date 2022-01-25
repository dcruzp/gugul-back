from flask import Flask,jsonify
from time import sleep

from document_handler import DocumentsHandler
from documents import DOCUMENTS
from readcrancollection import  build_cran_collection

app = Flask(__name__)


crancollection = build_cran_collection()

doc_handler = DocumentsHandler(crancollection)


@app.route("/api/v1/query/<q>")
def SearchQ(q):
    
    #buscar los documentos mas similares a q
    sol = [
        {"value":d[0],"title": d[1].title, "id":d[1].id, "preview":d[1].text[:20]+"..."}
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
    index = index -1 
    response = jsonify({ 
        "title": crancollection[index].title,
        "body":crancollection[index].text,
        "id": crancollection[index].id,
    })

    response.headers.add('Access-Control-Allow-Origin', '*')

    return response
    
app.run(debug=True)
