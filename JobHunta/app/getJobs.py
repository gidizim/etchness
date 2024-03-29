import requests
from flask import jsonify, request
from careerjet_api import CareerjetAPIClient

def get_github_results(descrip, location, full_time, page):
    baseURL = 'https://jobs.github.com/positions.json'
    params = {
        'description': descrip,
        'location': location,
        # full time or part time
        'full_time': full_time,
        # each page has 50 results
        'page': page
    }
    results = requests.get(baseURL, params = params).json()
    job_results = []
    
    for job in results:
        info = {
            'title': job['title'],
            'job_type': job['type'],
            'description': job['description'],
            'location': job['location'],
            'company': job['company'],
            'created': job['created_at'],
            'url': job['url'],
            'salary': 'Unknown',
            'in_watchlist': 0
        }
        job_results.append(info)
    return job_results;

ADZUNA_API = 'fee7b067359bebd25438ecd0db7c5f95'
ADZUNA_ID = '0c843767'

def get_adzuna_results(descrip, location, full_time, part_time, page, salary):
    baseURL = 'https://api.adzuna.com/v1/api/jobs/au/search/1'
    params = {
        'app_id': ADZUNA_ID,
        'app_key': ADZUNA_API,
        'results_per_page': 30,
        'what': descrip,
        'where': location,
        'sort_by': 'relevance',
        'salary_min': salary,
        'salary_include_unknown': 1,
        'content-type': 'application/json'
    }
    
    if full_time and not part_time:
        params['full_time'] = 1
    elif part_time and not full_time:
        params['part_time'] = 1

    response = requests.get(baseURL, params = params)

    if response.status_code == 200: 
        results = response.json()
        job_results = []
        for job in results['results']:
            if 'display_name' in job['company'].keys(): 
                company = job['company']['display_name']
            else:
                company = 'Unknown'
                
            if 'salary_is_predicted' in job.keys(): 
                salary = 'Unknown'
            else:
                salary = job['salary_min']
                
            if 'contract_time' in job.keys(): 
                job_type = job['contract_time']
            else:
                job_type = 'Unknown'

            info = {
                'title': job['title'],
                'job_type': job_type,
                'description': job['description'],
                'location': job['location']['display_name'],
                'company': company,
                'created': job['created'],
                'url': job['redirect_url'],
                'salary': salary,
                'in_watchlist': 0
            }
            job_results.append(info)

        return job_results
    
    print('Response content is not in JSON format.')
    return 'invalid'

CAREERJET_ID = 'ace0afe5820cf82e55eea526ed3aeb39'

def get_careerjet_results(client_useragent, client_ip, descrip, location, page, job_type):
    cj  =  CareerjetAPIClient("en_AU");
    baseURL = 'https://www.careerjet.com.au/search/jobs?'
    result_json = cj.search({
                        'affid'       : CAREERJET_ID,
                        'user_agent'  : client_useragent,
                        'user_ip'     : client_ip,
                        'url'         : baseURL,
                        'location'    : location,
                        'keywords'    : descrip,
                        'page'        : page,
                        # full time or part time (f/p)
                        'contractperiod': job_type,
                        'pagesize'   : 50,
                      })
    results = result_json
    job_results = []
    
    if results['hits'] != 0:
        for job in results['jobs']:
            if job_type == 'f':
                jobtype = 'Full Time'
            elif job_type == 'p':
                jobtype = 'Part Time'
            else:
                jobtype = 'Unknown'
            info = {
                'title': job['title'],
                'job_type': jobtype,
                'description': job['description'],
                'location': job['locations'],
                'company': job['company'],
                'created': job['date'],
                'url': job['url'],
                'salary': 'Unknown',
                'in_watchlist': 0
            }
            job_results.append(info)

    return job_results

def get_combined_results(useragent, ip, descrip, location, full_time, part_time, job_type, page, salary):
    job_results = []
    adzuna_resp = get_adzuna_results(descrip, location, full_time, part_time, page, salary)
    github_resp = get_github_results(descrip, location, full_time, page)
    careerjet_resp = get_careerjet_results(useragent, ip, descrip, location, page, job_type)
    print("github " + str(len(github_resp)))
    print("adzuna " + str(len(adzuna_resp)))
    print("careerjet " + str(len(careerjet_resp)))
    for job in github_resp:
        job_results.append(job)
    for job in adzuna_resp:
        job_results.append(job)
    for job in careerjet_resp:
        job_results.append(job)
    return job_results
