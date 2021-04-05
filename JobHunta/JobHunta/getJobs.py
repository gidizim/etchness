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
    return requests.get(baseURL, params = params).json()

ADZUNA_API = 'fee7b067359bebd25438ecd0db7c5f95'
ADZUNA_ID = '0c843767'

def get_adzuna_results(descrip, location, full_time, part_time, page):
    # assuming that we are only getting jobs in australia
    country = 'au'
    # return results in json
    baseURL = 'http://api.adzuna.com/v1/api/jobs/' + country + '/search/' + str(page)
    params = {
        'app_id': ADZUNA_ID,
        'app_key': ADZUNA_API,
        'results_per_page': 15,
        'what': descrip,
        'where': location,
        'sort_by': 'relevance',
        'full_time': full_time,
        'part_time': part_time,
        'salary_include_unknown': 1,
        # eg url has this in params
        'content-type': 'application/json'
    }
    headers = {
        'Accept': 'application/json',
        'Content-type': 'application/json'
    }

    response = requests.get(baseURL, params = params, headers = headers)
    # try:
    #     resp_content = response.json()
    # except ValueError:
    #     resp_content = response.content
    #     print(resp_content)
    # return resp_content
    if 'json' in response.headers.get('Content-Type'):
        return response.json()
    else:
        print('Response content is not in JSON format.')
        return 'invalid'

CAREERJET_ID = 'ace0afe5820cf82e55eea526ed3aeb39'

def get_careerjet_results(client_useragent, client_ip, descrip, location, page, job_type):
    cj  =  CareerjetAPIClient("en_AU");
    # baseURL = 'https://www.careerjet.com.au'
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
                        'pagesize'   : 15
                      })

    return result_json

def get_combined_results(useragent, ip, descrip, location, full_time, part_time, job_type, page):
    job_results = []
    adzuna_resp = get_adzuna_results(descrip, location, full_time, part_time, page)
    github_resp = get_github_results(descrip, location, full_time, page)
    careerjet_resp = get_careerjet_results(useragent, ip, descrip, location, page, job_type)
    for job in github_resp:
        info = {
            # 'id': job['id'],
            'title': job['title'],
            'job_type': job['type'],
            'description': job['description'],
            'location': job['location'],
            'company': job['company'],
            'created': job['created_at'],
            'url': job['url'],
            'salary': 'Unknown'
        }
        job_results.append(info)

    for job in careerjet_resp['jobs']:
        if job_type == 'f':
            jobtype = 'Full Time'
        elif job_type == 'p':
            jobtype = 'Part Time'
        else:
            jobtype = 'Unknown'
        info = {
            # 'id': None,
            'title': job['title'],
            'job_type': jobtype,
            'description': job['description'],
            'location': job['locations'],
            'company': job['company'],
            'created': job['date'],
            'url': job['url'],
            'salary': job['salary']
        }
        job_results.append(info)


    if adzuna_resp == 'invalid': return job_results
    for job in adzuna_resp['results']:
        if 'display_name' in job['company'].keys(): 
            company = job['company']['display_name']
        else:
            company = 'Unknown'
            
        if 'salary_is_predicted' in job.keys(): 
            salary = 'Unknown'
        else:
            salary = job['salary_min']

        info = {
            # 'id': job['id'],
            'title': job['title'],
            'job_type': job['contract_time'],
            'description': job['description'],
            'location': job['location']['display_name'],
            'company': company,
            'created': job['created'],
            'url': job['redirect_url'],
            'salary': salary
        }
        job_results.append(info)

    return job_results

# get_github_results('software', 'Sydney', False, 1)
# print (get_adzuna_results('software', 'Sydney', '', 1, 1))
# print (get_combined_results('software', 'Sydney', '', 1, 1))
