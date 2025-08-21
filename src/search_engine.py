
import os
import requests
import json
import yaml
from readability import Document
from bs4 import BeautifulSoup
import requests
with open("config/api.yaml", "r") as f:
    config = yaml.safe_load(f)


CONFIG = {
    'api_key': config['brightdata']['api_key'],
    'zone': 'serp_api1',
}


def fetch_texts_from_search():
    urls = fetch_result_urls()
    print(f"🔗 Found {len(urls)} URLs")
    results = []

    for url in urls[:3]:  # 限制前3个结果以节省请求量
        print(f"🌐 Fetching content from: {url}")
        text = extract_clean_text(url)
        results.append(f"URL: {url}\n{text[:1000]}...\n")  # 可限制字数
    return "\n\n---\n\n".join(results)

def fetch_and_extract_snippets():
    """
    Fetches search results using Bright Data API and extracts title, description, and URL.
    """
    try:
        if CONFIG['api_key'] == 'YOUR_API_KEY':
            print('⚠️ Please set your actual API key before making requests')
        
        print(f"🔄 Fetching {CONFIG['search_engine_query_url']} through Bright Data SERP API...")

        response = requests.post(
            'https://api.brightdata.com/request',
            headers={
                'Authorization': f"Bearer {CONFIG['api_key']}",
                'Content-Type': 'application/json'
            },
            json={
                'zone': CONFIG['zone'],
                'url': CONFIG['search_engine_query_url'],
                'format': 'json'
            }
        )

        if not response.ok:
            raise Exception(f"HTTP error! Status: {response.status_code}")
        
        data = response.json()
        print('✅ Request successful! Extracting results...')

        results = []
        for page in data.get("results", []):
            for result in page.get("page", {}).get("results", []):
                title = result.get("title", "")
                desc = result.get("description", "")
                url = result.get("url", "")
                results.append(f"Title: {title}\nSnippet: {desc}\nURL: {url}\n")

        return "\n".join(results) if results else "No results found."

    except Exception as error:
        print(f'❌ Error: {error}')
        raise error
    
def fetch_result_urls(quiry):
    """
    使用 BrightData 搜索并返回结果页面的 URL 列表
    """
    response = requests.post(
        'https://api.brightdata.com/request',
        headers={
            'Authorization': f"Bearer {CONFIG['api_key']}",
            'Content-Type': 'application/json'
        },
        json={
            'zone': CONFIG['zone'],
            'url': 'https://www.google.com/search?q=' + quiry,
            'format': 'json'
        }
    )

    data = response.json()
    urls = []
    for page in data.get("results", []):
        for result in page.get("page", {}).get("results", []):
            url = result.get("url", "")
            if url:
                urls.append(url)
    return urls



def extract_clean_text(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        resp = requests.get(url, headers=headers, timeout=10)
        doc = Document(resp.text)
        cleaned_html = doc.summary()
        soup = BeautifulSoup(cleaned_html, "html.parser")
        text = soup.get_text(separator="\n", strip=True)
        return text
    except Exception as e:
        return f"[Error fetching {url}]: {e}"
    
    