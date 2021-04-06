from . import db

# Gets list of jobs by a given u_id, returns a list of job postings
def get_watchlist(u_id):

    # Getting db and cursor
    conn = db.get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM job, watchlist WHERE watchlist.user_id = ? AND watchlist.job_id = job.id;", u_id)

    results = []

    for row in cur.fetchall():
        curr_job = {}
        curr_job['id'] = row['id']
        curr_job['title'] = row['title']
        curr_job['job_type'] = row['job_type']
        curr_job['description'] = row['description']
        curr_job['company'] = row['company']
        curr_job['location'] = row['location']
        curr_job['salary'] = row['salary']
        curr_job['created'] = row['created']

        results.append(curr_job)

    db.close_db()

    return results

# Adds job posting to watchlist
def add_to_watchlist(u_id, job_posting):
    # Getting db and cursor
    conn = db.get_db()
    cur = conn.cursor()

    job_id = job_posting['url']


    job_data = (job_posting['url'],
                job_posting['title'],
                job_posting['job_type'],
                job_posting['description'],
                job_posting['location'],
                job_posting['company'],
                job_posting['created'],
                job_posting['salary'])

    cur.execute("INSERT INTO job VALUES (?, ?, ?, ?, ?, ?, ?, ?) ;", job_data)
    cur.execute("INSERT INTO watchlist VALUES (?, ?);", (u_id, job_id))

    conn.commit()
    db.close_db()

    return True

# Checks if job is in the watchlist
def in_watchlist(u_id, job_id):
    conn = db.get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM watchlist WHERE u_id = ? AND job_id = ?", (u_id, job_id))

    result = cur.rowcount > 0

    db.close_db()

    return result

# Removes job posting to watchlist
def remove_from_watchlist(u_id, url):
    # Getting db and cursor
    conn = db.get_db()
    cur = conn.cursor()

    job_id = url
    cur.execute("DELETE FROM watchlist WHERE user_id = ? AND job_id = ?;", (u_id, job_id))

    conn.commit()
    db.close_db()

    return True
