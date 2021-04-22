from newsapi import NewsApiClient
from datetime import date, timedelta
newsapi = NewsApiClient(api_key='9a581e460ddd45f6aa51e889efcb4dae')

def getNews(keyword, lang, from_days): 
    articles = newsapi.get_everything(q=keyword,
                                        language=lang,
                                        page=1,
                                        from_param=date.today() - timedelta(days=from_days),
                                        to=date.today(),
                                        sources="abc-news-au, news-com-au",
                                        domains="9news.com.au, News.com.au, smh.com.au, theguardian.com")
    return articles