from DataScrape import list_insert_into_mongo
import json
import requests

with open('keys.txt','r') as file:
    lines=file.readlines()


def npr_api_request(npr_html,year,month,day):
    x=json.loads(requests.get(npr_html).text)
    npr_heads=[]

    try:
        stories=x['list']['story']
        for title in stories:
            npr_heads.append({'year':year,'month':month,'day':day,'title':title['title']['$text']})
        print('Completed'+str(day)+' '+str(month)+' '+str(year))
    
    except Exception as e:
        print('Check'+str(day)+' '+str(month)+' '+str(year))

    return npr_heads

def get_npr_html(year,month,day):
    html='http://api.npr.org/query?id=1002&fields=title&date='+str(year)+'-'+str(month)+'-'+str(day)+'&dateType=story&output=JSON&numResults=50&apiKey='+lines[1].strip()
    return html


def get_npr_titles(y_start,y_end,m_start,m_end,d_start,d_end,d_inc=1):
    all_queries=[]
    for year in range(y_start,y_end):
        for month in range(m_start,m_end):
            for day in range(d_start,d_end,d_inc):
                html=get_npr_html(year,month,day)
                all_queries=all_queries+npr_api_request(html,year,month,day)
    list_insert_into_mongo('NPR','NPR',all_queries)


if __name__ =="__main__":
    get_npr_titles(2015,2016,2,3,2,3,1)
