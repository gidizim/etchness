from newsapi import NewsApiClient
from datetime import date, timedelta
newsapi = NewsApiClient(api_key='db0f90a0065445e786863c1ce792fef6')

def getNews(keyword, lang, from_days): 
    if from_days  == 'Day':
        from_days = 1
    elif from_days == 'Month':
        from_days = 30
    elif from_days == 'Year':
        from_days = 365
    articles = newsapi.get_everything(q=keyword,
                                        language=lang,
                                        page=1,
                                        from_param=date.today() - timedelta(days=int(from_days)),
                                        to=date.today(),
                                        sources="abc-news-au, news-com-au",
                                        domains="9news.com.au, News.com.au, smh.com.au, theguardian.com")
    return articles




def searchedNews(description,location, timeframe, category): 
    
    ntime = gettime(timeframe)
    articles = newsapi.get_everything(q=description  + category,
                                       
                                        page=1,
                                        sources="abc-news-au, news-com-au",
                                        domains="9news.com.au, News.com.au, smh.com.au, theguardian.com",
                                        #cant mix
                                        #sources='abc-news-au, news-com-au',
                                        language='en',
                                        from_param=ntime,
                                        to=date.today())
                                        
                                        #country=location)
                                        
                                        #domains="9news.com.au, News.com.au, smh.com.au, theguardian.com")
    
    return articles


def gettime(timeframe): 
    ntime = date.today()
    if timeframe == "day":
        ntime = date.today() - timedelta(days=1)
    elif timeframe == "month":
        ntime = date.today() - timedelta(days=30)
    elif timeframe == "year":
        ntime = date.today() - timedelta(days=365)
        
    return ntime
