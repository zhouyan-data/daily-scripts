import requests
from bs4 import BeautifulSoup
import time

def get_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.encoding = r.apparent_encoding
        return r.text
    except Exception as e:
        print(f"出错: {e}")
        return None

def parse_titles(html):
    soup = BeautifulSoup(html, 'html.parser')
    titles = soup.find_all('h2')
    return [t.get_text().strip() for t in titles if t.get_text().strip()]

if __name__ == '__main__':
    url = input("输入目标网址: ")
    html = get_page(url)
    if html:
        titles = parse_titles(html)
        for i, t in enumerate(titles, 1):
            print(f"{i}. {t}")
        time.sleep(1)
