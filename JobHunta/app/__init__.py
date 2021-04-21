from mmap import ACCESS_DEFAULT
from flask.templating import render_template_string
from .newsfeed import getNews, get_keywords, add_to_searched
from .getJobs import get_combined_results, get_github_results, get_careerjet_results, get_adzuna_results
from flask import Flask
from flask import render_template, request, url_for, redirect, session, flash, jsonify
from flask_mail import Mail, Message
from flask_paginate import Pagination, get_page_parameter
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from . import auth
from .popular import get_popular_jobs, append_popular_job, clear_popular_job
from .watchlist import get_watchlist, add_to_watchlist, remove_from_watchlist, reset_watchlist, in_watchlist
from .user import get_user_details, get_user_id, set_user_details, reset_password
from .applyJobs import get_num_applied, already_applied, add_to_applied, remove_from_applied, get_applied
import os
import re
import string
import random
import time

app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
)
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME = 'Jobhunta.Etchness@gmail.com',
    MAIL_PASSWORD = 'SENG2021!'
)

# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

db.init_app(app)
app.secret_key= b'\x8b\x13\xac\xcc\x9b(\xdc\xf6\x80^T\xc9y\xd2n\x9d'
popup = -1
@app.route('/')
def get_home():
    global popup
    # Show top 5 results
    jobs = get_popular_jobs()
    u_id = session.get('user_id')
    if u_id is None:
        popup = -1
        reset_watchlist()
        if jobs != []:
            print("there are jobs")
            # if not logged in and popular jobs have been stored in db
            return render_template('home.html', jobs=jobs[:5], login=0);
        else:
            print("there are no jobs")
            # if not logged in and jobs are empty then we add
            jobs = get_github_results('software', '', True , 1)
            print(len(jobs))
            for job in jobs:
                append_popular_job(job)
        return render_template('home.html', jobs=jobs[:5], login=0);
            
    jobs = get_popular_jobs()
    keywords = get_keywords(u_id)
    print("in reverse")
    keywords.reverse()
    print(keywords)
    print(set(keywords))
    print(len(jobs))

    # if logged in then reset jobs if keywords exist
    if keywords != []:
        jobs = []
        print("has keywords")
        # get the most recent 3 searched words
        for keyword in list(set(keywords))[:3]:
            # result = get_adzuna_results(keyword, 'Sydney', '', 1, 1, 100)
            # if result == 'invalid':
            #     print("got github jobs")
            result = get_github_results(keyword, '', True , 1)
            for job in result:
                jobs.append(job)
            
    print(len(jobs))

    # already been shown once
    if popup == 1:
        popup = 0
    elif popup == -1:
        popup = 1

    print(popup);
    for job in jobs[:5]:
        added = in_watchlist(u_id, job['url'])
        print('in watchlist')
        print(added)
        job['in_watchlist'] = 1 if added else 0

    return render_template('home.html', jobs=jobs[:5], login=1)

# List of articles is empty when server is first set up
articles = []
ARTICLES_PER_PAGE = 5
@app.route('/newsfeed', methods=['GET', 'POST'])
def get_news():
    global articles
    u_id = session.get('user_id')
    # initial display of newsfeed
    if not articles:
        # for logged in user
        keywords = get_keywords(u_id)
        keywords.reverse()
        if u_id and keywords:    
            print(set(keywords))
            # get the most recent 3 words
            newsfeed = []
            for keyword in list(set(keywords))[:3]:
                for news in getNews(keyword, 'en', 3)['articles']:
                    newsfeed.append(news)
            articles = { 'articles': newsfeed }

        # for other users
        else:
            articles = getNews('Australian jobs', 'en', 3)

    page = request.args.get(get_page_parameter(), type=int, default=1)
    i = (page - 1) * ARTICLES_PER_PAGE
    pagination = Pagination(page=page, per_page=ARTICLES_PER_PAGE, total=len(articles['articles']), record_name='articles')
    
    curr_articles = articles['articles'][i : i + ARTICLES_PER_PAGE]
    if request.method != 'POST':
        return render_template('newsfeed.html', articles=curr_articles, pagination=pagination)

    data = request.get_json(force=True)
    description = data['description']
    category = data['category']
    from_day = data['ntime']
    country = data['location']

    # searched_keywords = description + ' ' + category + ' ' + country
    searched_keywords = description
    if u_id:
        add_to_searched(u_id, searched_keywords.strip()) 

    articles = getNews(searched_keywords.strip(), 'en', from_day)
    curr_articles = articles['articles'][i : i + ARTICLES_PER_PAGE]
    return render_template('newsfeed.html', articles=curr_articles, pagination=pagination)
        
   


@app.route('/components/<file>')
def get_component(file):
    global articles
    login = 0
    u_id = session.get('user_id')
    if u_id is not None:
        login = 1
        articles = []
    return render_template("components/" + file, login=login)

@app.route('/<file>')
def get_html(file="home.html"):
    return render_template(file)

jobs = []
JOBS_PER_PAGE = 15
@app.route('/results', methods=['GET', 'POST'])
def get_job_results():
    global jobs
    login = 0
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
        else:
            job['in_watchlist'] = 0

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
    print(data)
    
    if u_id and descrip:
        add_to_searched(u_id, descrip)
        print(descrip)
    jobs = get_combined_results(useragent, ip, descrip, data['location'], full_time, part_time, job_type, data['page'], data['salary'])
    
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
        job = data['job']
        applications = get_num_applied(job['url'])
        (job['num_applied'], job['num_responded'], job['num_interviewed'], job['num_finalised']) = applications

        prev = data['prev']

    u_id = session.get('user_id')
    flag = 0

    if u_id is not None:
        applied = already_applied(u_id, job['url'])

        for i, res in enumerate(applied):
            if res == 1:
                flag = i + 1

        print("Flag", flag)

        login = 1
    
    return render_template('jobposting.html', job=job, prev=prev, login=login, u_id=u_id, flag=flag)

@app.route('/applyToJob', methods=['POST'])
def apply_to_job():
    data = request.get_json(force=True)
    add_to_applied(data['u_id'], data['jobposting'])

    return jsonify({})

@app.route('/removeFromJob', methods=['DELETE'])
def remove_from_job():
    data = request.get_json(force=True)
    remove_from_applied(data['u_id'], data['jobposting'])

    return jsonify({})

@app.route('/addToWatchlist', methods=['GET', 'POST'])
def add_watchlist_job():
    u_id = session.get('user_id')
    if u_id is not None:
        # call db function
        add_to_watchlist(u_id, request.get_json()['job'])
    else:
        return redirect(url_for('get_home'))
    return 'Success', 200

@app.route('/removeFromWatchlist', methods=['GET', 'POST'])
def remove_watchlist_job():
    u_id = session.get('user_id')
    if u_id is not None:
        # call db function
        remove_from_watchlist(u_id, request.get_json()['url'])
    else:
        return redirect(url_for('get_home'))

    return 'Success', 200

@app.route('/watchlist')
def get_watchlist_jobs():
    u_id = session.get('user_id')
    if u_id is not None:
        watchlist_jobs = get_watchlist(u_id)
        applied_jobs = get_applied(u_id)
    else:
        return redirect(url_for('get_login'))


    return render_template('watchlist.html', watchlist_jobs=watchlist_jobs, applied_jobs=applied_jobs)

@app.route('/profile', methods=['GET', 'POST'])
def get_profile():
    u_id = session.get('user_id')
    if u_id is None:
        return redirect(url_for('get_login'))

    if request.method == 'POST':
        user_info = get_user_details(u_id)
        email = request.form.get('pro_email')
        fname = request.form.get('pro_fname')
        lname = request.form.get('pro_lname')
        try:
            set_user_details(u_id, email.lower(), fname, lname)
            flash("Changes saved")
            
            return redirect(url_for('get_profile'))
        except Exception as e:
            flash(e)
    else:
        user_info = get_user_details(u_id)
        return render_template('profile.html', user_info=user_info)

@app.route('/login', methods=['GET', 'POST'])
def get_login():
    if request.method == 'POST':
        email = request.form.get('login_email')
        password = request.form.get('login_pw')
        try:
            session.clear()
            u_id = auth.login(email.lower(), password)
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
                u_id = auth.signup(email.lower(), generate_password_hash(pw, method='sha256') ,fname, lname)
                session['user_id'] = u_id
                return redirect(url_for('get_home'))
            except Exception as e:
                print("Exception raised", e)
                flash(e)
        else:
            flash(error)

    return render_template('signup.html')
sent = False
email = ''
verify = False
@app.route('/resetpw', methods = ['GET', 'POST'])
def get_resetpw():
    global sent
    global email 
    global verify
    if request.method == 'POST':
        print(request.form)
        # email = request.form.get('reset_email')
        if "email_button" in request.form:
            sent = False
            print("sent: " + str(sent))
            # generates 6 digit token
            token = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            email = request.form.get('reset_email')
            try:
                auth.add_reset_token(email.lower(), token)
                sent = True
                email = email
                mail = Mail(app)
                msg = Message()
                msg.subject = "JobHunta Password reset"
                msg.sender = "jobhunta.etchness@gmail.com"
                msg.recipients = [email]
                msg.html = render_template("resetpw_defaultmsg.html", token=token)
                mail.send(msg)
                return render_template("resetpw.html", sent=sent, verify=verify, email=email)
            except Exception as e:
                sent = False
                flash(e)
        elif "token_button" in request.form:

            token = request.form.get('reset_token')
            email = request.form.get('reset_email')
            
            if (auth.check_reset_token(email.lower(), token)):
                print("valid")
                verify = True
                return render_template('resetpw.html', sent=sent, verify=verify, email=email)
            else:
                flash("Token is invalid")
                return render_template('resetpw.html', sent=sent, verify=verify, email=email)
        elif "password_button" in request.form:
            pw = request.form.get('reset_pw')
            pw2 = request.form.get('reset_pw2')
            if (pw != pw2):
                flash("Passwords do not match")
            else:
                reset_password(get_user_id(email), generate_password_hash(pw, method='sha256'))
                return redirect(url_for('get_login'))
    return render_template('resetpw.html', sent=sent, verify=verify, email=email)

@app.route('/db_testing')
def test_db():
    return render_template("home.html")

@app.route('/logout')
def get_logout():
    global articles
    articles = []
    session.pop('user_id', None) 
    reset_watchlist()
    return redirect(url_for('get_home'))

if __name__ == "__main__":
    app.run(debug=True)
