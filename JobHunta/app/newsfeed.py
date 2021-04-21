from . import db
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



def save_most_recent_search(string):
    if (string == None):
        string = "Australia Jobs"
    
    conn = db.get_db()
    cur = conn.cursor()
    cur.execute("SELECT search FROM most_recent_searches;")

    data = cur.fetchall()
    if len(data) != 0:
        cur.execute("UPDATE most_recent_searches SET search = '%s';" % (string))

    cur.execute("UPDATE most_recent_searches SET search = '%s';" % (string))
    conn.commit()
    db.close_db()


def get_most_recent_search():

    conn = db.get_db()
    cur = conn.cursor()
    cur.execute("SELECT search FROM most_recent_searches")
    string = cur.fetchall()
    
    if (string == None):
        string = "Australia Jobs"
        cur.execute("UPDATE most_recent_searches SET search = '%s';" % (string))
    
    conn.commit()
    db.close_db()

    return string