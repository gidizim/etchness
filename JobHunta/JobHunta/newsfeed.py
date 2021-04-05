from newsapi import NewsApiClient
from datetime import date, timedelta
newsapi = NewsApiClient(api_key='db0f90a0065445e786863c1ce792fef6')

def getNews(keyword, lang, from_days): 
    articles = newsapi.get_everything(q=keyword,
                                          language=lang,
                                          page=1,
                                          from_param=date.today() - timedelta(days=from_days),
                                          to=date.today(),
                                          sources="abc-news-au, news-com-au",
                                          domains="9news.com.au, gizmodo.com.au, News.com.au, smh.com.au, theguardian.com")
    return articles
