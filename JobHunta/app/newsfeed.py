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

def add_to_searched(u_id, keyword):
    if (keyword == None):
        keyword = "Australia Jobs"
    
    conn = db.get_db()
    cur = conn.cursor()
    # TODO: prevent duplicates
    cur.execute("INSERT INTO searched_keywords VALUES (?, ?);", (u_id, keyword))

    conn.commit()
    db.close_db()


def get_keywords(u_id):

    conn = db.get_db()
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM searched_keywords WHERE user_id = '%s';" % u_id);

    keywords = []
    for row in cur.fetchall():
        keywords.append(row['keyword']);
    print(keywords);

    conn.commit()
    db.close_db()

    return keywords
