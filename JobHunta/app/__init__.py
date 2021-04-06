from flask.templating import render_template_string
# from .newsfeed import getNews
from .getJobs import get_combined_results, get_adzuna_results, get_careerjet_results
from flask import Flask
from flask import json, jsonify, render_template, request, url_for
from . import db
from . import auth
from flask_paginate import Pagination, get_page_parameter
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

jobs = []
JOBS_PER_PAGE = 15
@app.route('/results', methods=['GET', 'POST'])
def get_job_results():
    global jobs
    page = request.args.get(get_page_parameter(), type=int, default=1)
    i = (page - 1) * JOBS_PER_PAGE
    curr_jobs = jobs[i : i + JOBS_PER_PAGE]
    pagination = Pagination(page=page, per_page=JOBS_PER_PAGE, total=len(jobs), record_name='jobs')

    if request.method != 'POST':
        print("in get")
        return render_template('results.html', jobs=curr_jobs, pagination=pagination)
    ip = request.remote_addr
    useragent = request.headers.get('User-Agent')

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
    
    curr_jobs = jobs[i : i + JOBS_PER_PAGE]
    print(len(jobs))
    return render_template('results.html', jobs=curr_jobs, pagination=pagination)
    

job = {}
# GET method - 404 not found depending on params given
@app.route('/jobposting', methods=['GET', 'POST'])
def get_job():
    global job

    if request.method == 'POST':
        data = request.get_json(force=True)
        print(data)
        job = data
        # job['title'] = data['title']
        # job['location'] = data['location']
        # job['company'] = data['company']
        # job['description'] = data['description']
        # job['created'] = data['created']
        # job['job_type'] = data['job_type']
        # job['url'] = data['url']
        
    if request.method == 'GET':
        print("in get")
    
    return render_template('jobposting.html', job=job)



@app.route('/addToWatchlist', methods=['GET', 'POST'])
def add_to_watchlist():
    # call db function
    return 'Success', 200

@app.route('/removeFromWatchlist', methods=['GET', 'POST'])
def remove_from_watchlist():
    # call db function
    return 'Success', 200

if __name__ == "__main__":
    app.run(debug=True)
