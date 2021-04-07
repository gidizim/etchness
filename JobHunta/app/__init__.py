from flask.templating import render_template_string
from .newsfeed import getNews
from .getJobs import get_combined_results, get_github_results
from flask import Flask
from flask import render_template, request, url_for, redirect, session, flash
from flask_paginate import Pagination, get_page_parameter
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from . import auth
from .popular import get_popular_jobs, append_popular_job, clear_popular_job
from .watchlist import get_watchlist, add_to_watchlist, remove_from_watchlist, reset_watchlist
import os
import re
from .watchlist import get_watchlist, add_to_watchlist, remove_from_watchlist, in_watchlist
# TODO need to add view functionality for if user is logged in or not


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
app.secret_key= b'\x8b\x13\xac\xcc\x9b(\xdc\xf6\x80^T\xc9y\xd2n\x9d'

@app.route('/')
def get_home():
    # Show top 5 results
    jobs = get_popular_jobs()    
    print(jobs)
    u_id = session.get('user_id')
    login = 0
    for job in jobs:
        if u_id is None:
            # update db
            reset_watchlist()
            job['in_watchlist'] = 0
        else:
            login = 1
            added = in_watchlist(u_id, job['url'])
            job['in_watchlist'] = 1 if added else 0
        print(job['in_watchlist'])
    
    if jobs == []:
        index = 1
        data = get_github_results('software', 'Sydney', False, 1)
        for job in data:
            info = {
                'title': job['title'],
                'job_type': job['type'],
                'description': job['description'],
                'location': job['location'],
                'company': job['company'],
                'created': job['created_at'],
                'url': job['url'],
                'salary': 'Unknown',
                'in_watchlist': 0,
            }
            jobs.append(info)
            append_popular_job(info)

            index += 1


    return render_template('home.html', jobs=jobs[:6], login=login)

@app.route('/newsfeed')
def get_news():
    articles = getNews("jobs", "en", 3)
    return render_template('newsfeed.html', articles=articles['articles'][:5])

@app.route('/components/<file>')
def get_component(file):
    login = 0
    u_id = session.get('user_id')
    if u_id is not None:
        login = 1
    return render_template("components/" + file, login=login)

@app.route('/<file>')
def get_html(file="home.html"):
    return render_template(file)

jobs = []
JOBS_PER_PAGE = 15
@app.route('/results', methods=['GET', 'POST'])
def get_job_results():
    global jobs
    
    u_id = session.get('user_id')
    if u_id is not None:
        login = 1
    
    page = request.args.get(get_page_parameter(), type=int, default=1)
    i = (page - 1) * JOBS_PER_PAGE
    pagination = Pagination(page=page, per_page=JOBS_PER_PAGE, total=len(jobs), record_name='jobs')
    curr_jobs = jobs[i : i + JOBS_PER_PAGE]
    for job in curr_jobs:
        if in_watchlist(u_id, job['url']):
            job['in_watchlist'] = 1


    if request.method != 'POST':
        print("in get")
        return render_template('results.html', jobs=curr_jobs, pagination=pagination, login=login)
            
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
    
    print(len(jobs))
    return render_template('results.html', jobs=curr_jobs, pagination=pagination, login=login)
    

job = {}
prev = None
@app.route('/jobposting', methods=['GET', 'POST'])
def get_job():
    global job
    global prev
    login = 0
    
    if request.method == 'POST':
        data = request.get_json(force=True)
        print(data)
        job = data['job']
        prev = data['prev']

    u_id = session.get('user_id')
    if u_id is not None:
        login = 1
    
    return render_template('jobposting.html', job=job, prev=prev, login=login)


@app.route('/addToWatchlist', methods=['GET', 'POST'])
def add_watchlist_job():
    u_id = session.get('user_id')
    if u_id is not None:
        # call db function
        add_to_watchlist(u_id, request.get_json()['job'])
    else:
        redirect(url_for('get_home'))
    return 'Success', 200

@app.route('/removeFromWatchlist', methods=['GET', 'POST'])
def remove_watchlist_job():
    u_id = session.get('user_id')
    if u_id is not None:
        # call db function
        remove_from_watchlist(u_id, request.get_json()['url'])
    else:
        redirect(url_for('get_home'))

    return 'Success', 200

@app.route('/watchlist')
def get_watchlist_jobs():
    u_id = session.get('user_id')
    if u_id is not None:
        print("logged in")
        jobs = get_watchlist(u_id)
    else:
        redirect(url_for('get_home'))
    return render_template('watchlist.html', jobs=jobs)

@app.route('/profile')
def get_profile():
    return render_template('profile.html')

@app.before_request
def before_request_func():
    print("before_request is running!")
    u_id = session.get('user_id')
    if u_id is not None:
        print("logged in")

@app.route('/login', methods=['GET', 'POST'])
def get_login():
    if request.method == 'POST':
        email = request.form.get('login_email')
        password = request.form.get('login_pw')
        try:
            session.clear()
            u_id = auth.login(email, password)
            session['user_id'] = u_id
            return redirect(url_for('get_home'))
        except:
            flash("Invalid email or password")
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def get_signup():
    if request.method == 'POST':
        fname = request.form.get('reg_fname')
        lname = request.form.get('reg_lname')
        email = request.form.get('reg_email')
        pw = request.form.get('reg_pw')
        pw2 = request.form.get('reg_pw2')
        regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
        error = None
        if pw != pw2:
            error = "Passwords does not match"
        elif (not re.search(regex, email)):
            error = "Invalid email address"
        if error == None:
            try:
                u_id = auth.signup(email, generate_password_hash(pw, method='sha256') ,fname, lname)
                session['user_id'] = u_id
                return redirect(url_for('get_home'))
            except Exception as e:
                print("Exception raised", e)
                flash(e)
        else:
            flash(error)

    return render_template('signup.html')
        
@app.route('/resetpassword')
def get_resetpw():
    return render_template('resetpw.html')

@app.route('/db_testing')
def test_db():
    return render_template("home.html")

@app.route('/logout')
def get_logout():
    session.pop('user_id', None) 
    reset_watchlist();
    return redirect(url_for('get_home'))

if __name__ == "__main__":
    app.run(debug=True)
