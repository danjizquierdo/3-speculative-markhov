from bs4 import BeautifulSoup
import requests
import time

class Scraper:
    def __init__(self,genre):
        self._genre=genre
    
    @property
    def genre(self):
        return self._genre
    @genre.setter
    def genre(self,value):
        self._genre=value

    def go_scrape(self):
        url="https://www.goodreads.com/"
        param="shelf/show/"+self._genre
        titles=[]
        descriptions=[]
        book_links=[]
        for page in range(1,26):
                req = requests.get(url+param+f'?page={page}')
                soup=BeautifulSoup(req.content,'html.parser')
                links=soup.find_all("a",{'class': 'bookTitle'})
                links=list(set(links))
                for link in links:
                    titles.append(link.string)
                    book_links.append(link['href'])
        for book in book_links:
            req=requests.get(url+book)
            soup=BeautifulSoup(req.content,'html.parser')
            div=soup.find(id='description')
            span=div.select("span:nth-of-type(2)")
            try:
                description=span[0].text
                descriptions.append(description)
            except:
                descriptions.append('None')
        return titles,descriptions

