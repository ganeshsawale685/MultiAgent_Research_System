from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
from dotenv import load_dotenv
from rich import print
load_dotenv()

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

#Tool Creation
@tool
def web_search(query : str) -> str:
    """Search the Web for recent and reliable information on a topic . Returns Titles,URLs and snippets"""
    results = tavily_client.search(query=query,search_depth="basic",max_results=5)

    data =[]
    for r in results['results']:
        data.append(
            f'Title : {r['title']} \n URL :{r['url']} \n Snippet : {r['content'][:300]}\n'
        )

    return "\n-------\n".join(data)

# print(web_search.invoke("What is the recent new of sport ?"))

@tool
def scrape_url(url:str)-> str:
    "Scrape and return clean text content from a given URL for deep reading "
    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/154.0.0.0 Safari/537.36"
            ),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        }
        resp = requests.get(url,timeout=8,headers=headers)
        soup = BeautifulSoup(resp.text,"html.parser")

        for tag in soup(['script','style','nav','footer']):
            tag.decompose()

        return soup.get_text(separator=" ",strip=True)[:3000]

    except Exception as e:
        return f"Could not scrape URL : {str(e)}"

