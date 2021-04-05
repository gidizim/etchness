from flask.templating import render_template_string
from server.newsfeed import getNews
from server.getJobs import get_combined_results, get_careerjet_results
from flask import Flask
from flask import json, jsonify, render_template, request, url_for
app = Flask(__name__)

app.run(debug=True)

@app.route('/')
def hello_world():
    return render_template('home.html')

@app.route('/newsfeed')
def get_news():
    articles = getNews()
    return render_template('newsfeed.html', articles=articles)

@app.route('/components/<file>')
def get_component(file="home.html"):
    return render_template("components/" + file)

@app.route('/<file>')
def get_html(file="home.html"):
    return render_template(file)

# testing client ip
# get_careerjet_results('software', 'sydney', 1, 'p', 10)
# print(request.remote_addr)
# print(request.environ['REMOTE_ADDR'])
# print(request.environ.get('REMOTE_ADDR'))


# browser gets data
# @app.route('/search')
# def get_search_results(descrip, location, full_time, part_time, page):
#     return render_template('results.html', jobs=jobs)

# get_combined_results('software', 'Sydney', '', 1, '', '', 100000, 1)

# search_request = {}
#     if request.method == 'GET':
#         print("in get")
#         print(search_request)
        
#         full_time = 0
#         part_time = 1
#         if search_request['job_type'] == 'Full Time':
#             full_time = 1
#             part_time = 0
#         # response = get_careerjet_results(browser, client_ip, descrip, location, page, job_type, page_size):
#         # print(response)
#         jobs = get_combined_results(search_request['description'], search_request['location'], full_time, part_time, search_request['page'])
#         print("printing jobs")
#         print(jobs)
#         return jsonify({'result': str(jobs)})

@app.route('/search', methods=['GET', 'POST'])
def get_search_details():
    if request.method != 'POST':
        return
    print("in post")
    client_ip = request.remote_addr
    client_useragent = request.headers.get('User-Agent')
    print(client_ip)
    print(client_useragent)

    data = request.get_json(force=True)
    print(data)
    descrip = data['description']
    print(descrip)
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
    print(job_type)
    print("printing jobs")
    
    response = get_careerjet_results(client_useragent, client_ip, descrip, data['location'], data['page'], job_type, 20)
    print(response)
    # jobs = get_combined_results(descrip, data['location'], full_time, part_time, data['page'])
    # print(jobs)
    return 'Success', 200