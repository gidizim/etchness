from . import db
from newsapi import NewsApiClient
from datetime import date, timedelta
newsapi = NewsApiClient(api_key='9a581e460ddd45f6aa51e889efcb4dae')

def getNews(keyword, lang, from_days): 
    print(from_days)
    print(keyword)
    articles = newsapi.get_everything(q=keyword,
                                        language=lang,
                                        page=1,
                                        from_param=date.today() - timedelta(days=int(from_days)),
                                        to=date.today(),
                                        sources="abc-news-au, news-com-au",
                                        domains="9news.com.au, News.com.au, smh.com.au, theguardian.com")
    print('articles has ' + str(len(articles['articles'])))
    return articles

def add_to_searched(u_id, keyword):
    if (keyword == None):
        keyword = "Australia Jobs"
    
    conn = db.get_db()
    cur = conn.cursor()
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

    conn.commit()
    db.close_db()

    return keywords
