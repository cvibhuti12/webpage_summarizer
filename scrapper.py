import requests

from bs4 import BeautifulSoup
import pandas as pd

def extract_text(url):
    response = requests.get(url)
    
    if response.status_code != 200:
        return "Failed to retrieve the page"
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    content = soup.find('div', {'id': 'bodyContent'})
    
    paragraphs = content.find_all('p')
    
    text_content = "\n".join([para.get_text() for para in paragraphs])
    
    return text_content