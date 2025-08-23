import os
import requests
import json
import yaml
from langchain_community.docstore.document import Document
from bs4 import BeautifulSoup
import requests
import urllib.parse

with open("src/config/api.yaml", "r") as f:
    config = yaml.safe_load(f)


CONFIG = {
    'api_key': config['brightdata']['api_key'],
    'zone': config['brightdata']['zone'],
}


def fetch_docs_from_search(query):
    docs = fetch_result_description(query)
    docs_list = []
    for doc in docs:
        docs_list.append(Document(
            page_content=doc.get("description", ""),
            metadata={
                "title": doc.get("title", ""),
            }
        ))
    return docs_list


def fetch_result_description(query):
    query = urllib.parse.quote("Finance "+query)
    search_url = f"https://www.google.com/search?q={query}&brd_json=1"
    
    response = requests.post(
        "https://api.brightdata.com/request",
        headers={
            "Authorization": f"Bearer {CONFIG['api_key']}",
            "Content-Type": "application/json"
        },
        json={
            "url": search_url,
            'zone': CONFIG['zone'],
            "format": "json"
        }
    )
    
    
    # with open("search_results.json", "w") as f:
    #     json.dump(json.loads(response.json()["body"]),f, indent=4)
    # exit()
    
    while safe_json(response) is None:
        response = requests.post(
        "https://api.brightdata.com/request",
        headers={
            "Authorization": f"Bearer {CONFIG['api_key']}",
            "Content-Type": "application/json"
        },
        json={
            "url": search_url,
            'zone': CONFIG['zone'],
            "format": "json"
        }
        )
        print("Retrying...")
        
    data = json.loads(response.json()["body"])["organic"]
        

    docs = []
    for web in data[:5]:
        docs.append({
            "title": web.get("title", ""),
            "description": web.get("description", ""),
            "url": web.get("link", "")
        })
    with open("src/knowledgebase/online/search_results.json", "r") as f:
        existing_data = json.load(f)
    existing_data.extend(docs)
    with open("src/knowledgebase/online/search_results.json", "w") as f:
        json.dump(existing_data, f, indent=4)
    
    return existing_data
    

def fetch_result_urls(query):


    query = urllib.parse.quote(query)
    search_url = f"https://www.google.com/search?q={query}&brd_json=1"
    
    response = requests.post(
        "https://api.brightdata.com/request",
        headers={
            "Authorization": f"Bearer {CONFIG['api_key']}",
            "Content-Type": "application/json"
        },
        json={
            "url": search_url,
            'zone': CONFIG['zone'],
            "format": "json"
        }
    )
    
    data = json.loads(response.json())
    
    
    urls = []
    for page in data.get("results", []):
        for result in page.get("page", {}).get("results", []):
            url = result.get("url", "")
            if url:
                urls.append(url)
    return urls

def safe_json(response):
    try:
        data = json.loads(response.json()["body"])["organic"]
        return data
    except:
        print("Error in fetching search results")
        print(response)
        print(response.json())
    
        return None