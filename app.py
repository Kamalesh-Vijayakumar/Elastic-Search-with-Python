from flask import Flask, request, jsonify
from flask_cors import CORS
from elasticsearch import Elasticsearch
import pandas as pd
import numpy as np

app = Flask(__name__)
CORS(app)  

# Elasticsearch connection
es = Elasticsearch("http://localhost:9200")

# Loading the data
try:
    df = pd.read_csv("C://Employee Sample Data 1.csv", encoding='cp1252')  
except UnicodeDecodeError:
    df = pd.read_csv("C://Employee Sample Data 1.csv", encoding='utf-8', errors='ignore')  

df.drop_duplicates(subset='Employee ID', keep='first', inplace=True) #removing duplicates  
df.replace({np.nan: None}, inplace=True)  # Replacing Nan

index_name = "employees"


if es.indices.exists(index=index_name):
    es.indices.delete(index=index_name)
    print(f"Index {index_name} deleted.")

# index
es.indices.create(index=index_name, ignore=400)
print(f"Index {index_name} created.")

# Indexing clean data
for index, row in df.iterrows():
    document = row.to_dict()
    try:
        es.index(index=index_name, body=document)
    except Exception as e:
        print("Error indexing document:", e)
        break

# Search endpoint
@app.route('/search', methods=['POST'])
def search():
    data = request.json
    search_query = data['query']
    response = es.search(
        index=index_name,
        body={
            "query": {
                "multi_match": {
                    "query": search_query,
                    "fields": ["Employee ID","Full Name", "Job Title", "Department"] 
                }
            }
        }
    )
    return jsonify(response['hits']['hits'])

# CRUD Endpoints
@app.route('/create', methods=['POST'])
def create_document():
    doc = request.json
    res = es.index(index=index_name, body=doc)
    return jsonify(res)

@app.route('/document/<id>', methods=['GET'])
def get_document(id):
    res = es.get(index=index_name, id=id)
    return jsonify(res['_source'])

@app.route('/update/<id>', methods=['POST'])
def update_document(id):
    update_body = request.json
    res = es.update(index=index_name, id=id, body={"doc": update_body})
    return jsonify(res)

@app.route('/delete/<id>', methods=['DELETE'])
def delete_document(id):
    res = es.delete(index=index_name, id=id)
    return jsonify(res)

# Error handling
@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify(error=str(e)), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
