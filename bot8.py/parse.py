import requests
from bs4 import BeautifulSoup

def parse_news():
    url = "https://m.akipress.org/"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")

    data = soup.find_all("div", class_="nowr_elem")

    for d in data in range:   
        news = d.find("a",class_="nowr_title" ).text