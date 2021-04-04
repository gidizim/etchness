from flask import Flask
from flask import render_template, url_for
from newsapi import NewsApiClient
from getJobs import get_combined_results

newsapi = NewsApiClient(api_key='db0f90a0065445e786863c1ce792fef6')

top_headlines = newsapi.get_top_headlines(q='bitcoin',
                                          category='business',
                                          language='en',
                                          country='us')

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('home.html')

@app.route('/components/<file>')
def get_component(file="home.html"):
    return render_template("components/" + file)

@app.route('/<file>')
def get_html(file="home.html"):
    return render_template(file)

# browser gets data
@app.route('/search')
def get_search_results(descrip, location, full_time, part_time, contract, permanent, salary_min, page):
    return get_combined_results(descrip, location, full_time, part_time, contract, permanent, salary_min, page)


# get_combined_results('software', 'Sydney', '', 1, '', '', 100000, 1)