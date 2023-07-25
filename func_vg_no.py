from bs4 import BeautifulSoup as bs
import requests
import json


def pars_func()-> None:
    '''
    Function create new dict with all news from site vg.no
    '''

    headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        }
    
    # url = 'https://www.vg.no/tag/oslo'
    url = 'https://www.vg.no/nyheter'
    r = requests.get(url=url, headers=headers)
    soup = bs(r.text, 'lxml')
    news_room = soup.find_all('article', itemtype="https://schema.org/NewsArticle")
    
    news_dict = {}
        
    for news in news_room:
        news_url = news.get('id')
        news_id = news.get('id').split('/')[-1]
        if news_id.startswith('article'):
            # news_url = getattr(news.find('href'),'text', None)
            news_url = news.find('href')
            print(news_url)
        else: 
            head_line_news = getattr(news.find('h3', class_="hyperion-css-m7ex9y"),'text', None)
            time_news = getattr(news.find('div', class_='timestamp friendly hyperion-css-c0pnpc'),'text', None)
            desk_news = getattr(news.find('span', class_="hyperion-css-vfhos6"),'text', None)
        # if time_news is not None and head_line_news is not None and desk_news is not None:
        #     print(f'{time_news} || {head_line_news} "\n" {desk_news}')
                    
                    
            news_dict[news_id] = {
                    'url': news_url,
                    'time_news': time_news,
                    'head_line_news' : head_line_news,
                    'desk_news' : desk_news
                }
        
    with open('vg.json', 'w') as f:
        json.dump(news_dict, f, indent=4, ensure_ascii=False)

def check_update()-> dict:
    '''
    Return dict with new wes
    '''
    with open('vg.json') as file:
        news_dict = json.load(file)
    
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        }

    url = 'https://www.vg.no/nyheter'
    r = requests.get(url=url, headers=headers)
    soup = bs(r.text, 'lxml')
    news_room = soup.find_all('article', itemtype="https://schema.org/NewsArticle")
    fresh_news = {}
    for news in news_room:
        news_url = news.get('id')
        news_id = news.get('id').split('/')[-1]
        if news_id in news_dict:
            continue
        else:
            head_line_news = getattr(news.find('h3', class_="hyperion-css-m7ex9y"),'text', None)
            time_news = getattr(news.find('div', class_='timestamp friendly hyperion-css-c0pnpc'),'text', None)
            desk_news = getattr(news.find('span', class_="hyperion-css-vfhos6"),'text', None)
                    
        news_dict[news_id] = {
                    'url': news_url,
                    'time_news': time_news,
                    'head_line_news' : head_line_news,
                    'desk_news' : desk_news
                }
        fresh_news[news_id] = {
                    'url': news_url,
                    'time_news': time_news,
                    'head_line_news' : head_line_news,
                    'desk_news' : desk_news
                }
        
    with open('vg.json', 'w') as f:
        json.dump(news_dict, f, indent=4, ensure_ascii=False)

    return fresh_news

        

def main():
    pars_func()
    check_update()

if __name__=='__main__':
    # pars_func()
    main()