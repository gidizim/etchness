import requests

def get_github_results(descrip, location, full_time, page):
    baseURL = "https://jobs.github.com/positions.json"
    params = {
        'description': descrip,
        'location': location,
        # full time or part time
        'full_time': full_time,
        # each page has 50 results
        'page': page
    }
    return requests.get(baseURL, params = params).json()

ADZUNA_API = "fee7b067359bebd25438ecd0db7c5f95"
ADZUNA_ID = "0c843767"

def get_adzuna_results(descrip, location, full_time, part_time, contract, permanent, salary_min, page):
    # assuming that we are only getting jobs in australia
    country = "au"
    # return results in json
    baseURL = "http://api.adzuna.com/v1/api/jobs/" + country + "/search/" + str(page)
    params = {
        'app_id': ADZUNA_ID,
        'app_key': ADZUNA_API,
        'results_per_page': 20,
        'what': descrip,
        'where': location,
        'sort_by': 'relevance',
        'full_time': full_time,
        'part_time': part_time,
        'contract': contract,
        'permanent': permanent,
        'salary_include_unknown': 1,
        'salary_min': salary_min
    }
    return requests.get(baseURL, params = params).json()
    

def get_combined_results(descrip, location, full_time, part_time, contract, permanent, salary_min, page):
    job_results = []
    adzuna_resp = get_adzuna_results(descrip, location, full_time, part_time, contract, permanent, salary_min, page)
    github_resp = get_github_results(descrip, location, full_time, page)

    for job in github_resp:
        info = {
            'id': job['id'],
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

    for job in adzuna_resp['results']:
        if 'salary_is_predicted' in job.keys(): 
            salary = 'Unknown'
        else:
            salary = job['salary_min']

        info = {
            'id': job['id'],
            'title': job['title'],
            'job_type': job['contract_time'],
            'description': job['description'],
            'location': job['location']['display_name'],
            'company': job['company']['display_name'],
            'created': job['created'],
            'url': job['redirect_url'],
            'salary': salary
        }
        job_results.append(info)

    return job_results

# get_github_results('software', 'Sydney', False, 1)
# get_adzuna_results('software', 'Sydney', '', 1, '', '', 100000, 1)
