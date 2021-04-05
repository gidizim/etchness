from flask.templating import render_template_string
from .newsfeed import getNews
from .getJobs import get_combined_results, get_combined_results, get_careerjet_results
from flask import Flask
from flask import json, jsonify, render_template, request, url_for
from . import db
from . import auth

import os

app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
)

# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

db.init_app(app)

@app.route('/')
def get_home():
    return render_template('home.html')

@app.route('/newsfeed')
def get_news():
    articles = getNews("jobs", "en", 3)
    return render_template('newsfeed.html', articles=articles['articles'][:5])

@app.route('/components/<file>')
def get_component(file="home.html"):

    return render_template("components/" + file)

@app.route('/<file>')
def get_html(file="home.html"):
    return render_template(file)

@app.route('/results', methods=['GET', 'POST'])
def get_job_results():
    if request.method != 'POST':
        return 'Invalid'
    ip = request.remote_addr
    useragent = request.headers.get('User-Agent')
    print(ip)
    print(useragent)

    data = request.get_json(force=True)
    print(data)
    descrip = data['description']
    full_time = 1
    part_time = 1
    job_type = ''
    if data['job_type'] == 'Full Time':
        full_time = 1
        part_time = 0
        job_type = 'f'
    elif data['job_type'] == 'Part Time':
        full_time = 0
        part_time = 1
        job_type = 'p'

    if data['description'] == 'None':
        descrip = ''
    
    jobs = get_combined_results(useragent, ip, descrip, data['location'], full_time, part_time, job_type, data['page'])
    return render_template('results.html', jobs=jobs[:15])

if __name__ == "__main__":
    app.run()
