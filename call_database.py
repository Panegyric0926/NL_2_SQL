import requests

API_URL = "http://localhost:9000"

def insert_record(query, tables_involved, structure, code):
    url = f"{API_URL}/insert"
    payload = {
        "Query": query,
        "Tables_Involved": tables_involved,
        "Structure": structure,
        "Code": code
    }
    response = requests.post(url, json=payload)
    print("Insert Response:", response.status_code, response.json())

def query_record(query, structure, tables):
    url = f"{API_URL}/query"
    payload = {
        "Query": query,
        "Structure": structure,
        "Tables": tables
    }
    response = requests.post(url, json=payload)
    print("Query Response:", response.status_code, response.json()['match'])
    return response.json()
