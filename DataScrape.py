import requests
import pymongo
import json
import time
from bs4 import BeautifulSoup

connection = pymongo.MongoClient("mongodb://localhost")
buzzfeed_html='http://www.buzzfeed.com/trending?'

with open('keys.txt','r') as file:
    lines=file.readlines()

ny_times_html='http://api.nytimes.com/svc/news/v3/content/all/all.json?&limit=50&api-key='+lines[0].strip()
npr_html='http://api.npr.org/query?id=1002&fields=title&dateType=story&output=JSON&numResults=50&apiKey='+lines[1].strip()

def list_insert_into_mongo(db,collection,list_of_dicts):
    headlines=connection[db][collection]
    try:  
        for x in list_of_dicts:
            headlines.replace_one(x,x,upsert=True)

    except Exception as e:
        print('Unexpected error'+str(type(e))+str(e))
    
    print('Collection has '+str(headlines.count())+' Dicts')

def ny_api_request(ny_times_html):
    x=json.loads(requests.get(ny_times_html).text)
    stories=x['results']
    ny_heads=[]

    for title in stories:
        ny_heads.append({'title':title['title'],'site':'ny_times'})
    return ny_heads

def npr_api_request(npr_html):
    x=json.loads(requests.get(npr_html).text)
    stories=x['list']['story']
    npr_heads=[]

    for title in stories:
        npr_heads.append({'title':title['title']['$text'],'site':'npr'})
    return npr_heads

def buzzfeed_web_scrape(html):
    contents=requests.get(html)
    return BeautifulSoup(contents.text,"html.parser")

def get_buzzfeed_titles(soup_contents):
    stories=soup_contents.find_all('a',class_="trending-post-title")
    buzz_heads=[]

    for title in stories:
        buzz_heads.append({'title':title.contents[0],'site':'buzzfeed'})
    return buzz_heads

def scrape_and_request():
    buzz_heads=get_buzzfeed_titles(buzzfeed_web_scrape(buzzfeed_html))
    npr_heads=npr_api_request(npr_html)
    ny_heads=ny_api_request(ny_times_html)

    list_insert_into_mongo('News','Headlines',buzz_heads+npr_heads+ny_heads)
    

if __name__ =="__main__":
    while True:
        scrape_and_request()
        time.sleep(1800)
        
