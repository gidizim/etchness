from flask import Flask
from flask import render_template, url_for

from newsapi import NewsApiClient
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
