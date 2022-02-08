import time
import requests
from bs4 import BeautifulSoup as bs

file=open("jobs.tsv",'w')

response = requests.get('https://www.kijiji.it/offerte-di-lavoro/offerta/informatica-e-web')

content=bs(response.text,"html.parser")
print(content.title.string)

pages= content.find("h4",{"class": "pagination-hed"}).string
tokens = pages.split(' ')
last_page=int(tokens[3])

#-------------writing on file----------------
for i in range(1,last_page+1):
    if i>1:
        response = requests.get('https://www.kijiji.it/offerte-di-lavoro/offerta/informatica-e-web/?p='+str(i))
        content=bs(response.text,"html.parser")
    works = content.findAll("div", {"class": "item-content"})
    for work in works:
        title=work.find("a",{"class": "cta"}).string.strip()
        description=work.find("p",{"class": "description"}).string.strip().replace("\n"," ")
        location=work.find("p",{"class": "locale"}).string.strip()
        timestamp=work.find("p",{"class": "timestamp"}).string.strip()
        url=work.find("a",{"class": "cta"}).get("href")

        file.write(title+'\t'+description+'\t'+location+'\t'+timestamp+'\t'+url+'\n')
    time.sleep(0.5)

print("Content written on file: jobs.tsv")

file.close()






