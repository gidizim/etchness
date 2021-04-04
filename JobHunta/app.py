from flask.templating import render_template_string
from server.newsfeed import getNews
from server.getJobs import get_combined_results
from flask import Flask
from flask import render_template, url_for
app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('home.html')

@app.route('/newsfeed')
def get_news():
    articles = getNews()
    return render_template('newsfeed.html', articles=articles)

# browser gets data
@app.route('/search')
def get_search_results(descrip, location, full_time, part_time, contract, permanent, salary_min, page):
    jobs = get_combined_results(descrip, location, full_time, part_time, contract, permanent, salary_min, page)
    return render_template('results.html', jobs=jobs)

# get_combined_results('software', 'Sydney', '', 1, '', '', 100000, 1)

@app.route('/components/<file>')
def get_component(file="home.html"):
    return render_template("components/" + file)

@app.route('/<file>')
def get_html(file="home.html"):
    return render_template(file)
