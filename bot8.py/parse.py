import requests
from bs4 import BeautifulSoup

count_news = 0

def parse_news():
    count_news = 0
    url = 'https://vesti.kg/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    all_news = soup.find_all("div", class_="itemBody")[:5]
    news_list = []

    n ="""
    """
    for news in all_news:
        count_news += 1
        title = news.text.strip()
        link = news.find("a")['href'] if news.find('a') else url
        full_link = link if link.startswith("http") else f"https://vesti.kg/"
        news_list.append(f"{count_news}: {title} {full_link}{n}")
    return news_list    
