from . import db

# Gets list of jobs by a given u_id, returns a list of job postings
def get_applied(u_id):

    # Getting db and cursor
    conn = db.get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM jobs, applied WHERE applied.u_id = ? AND applied.job_id = job.id;", u_id)

    results = []

    for row in cur.fetchall():
        curr_job = {}
        curr_job['id'] = row['id']
        curr_job['title'] = row['title']
        curr_job['job_type'] = row['job_type']
        curr_job['description'] = row['description']
        curr_job['company'] = row['company']
        curr_job['url'] = row['url']
        curr_job['salary'] = row['salary']

        results.append(curr_job)

    db.close_db()

    return results

# Adds job posting to applied
def add_to_applied(u_id, job_posting):
    # Getting db and cursor
    conn = db.get_db()
    cur = conn.cursor()

    job_id = job_posting['id']

    cur.execute("SELECT * FROM job WHERE  job_id = ?;", job_id)

    if cur.rowcount != 0:


    job_data = (job_posting['id'],
                job_posting['title'],
                job_posting['job_type'],
                job_posting['description'],
                job_posting['location'],
                job_posting['company'],
                job_posting['url'],
                job_posting['salary'])


    cur.execute("INSERT INTO job VALUES ( ?, ?, ?, ?, ?, ?, ?, ?) ;", job_data)
    cur.execute("INSERT INTO applied VALUES (?, ?);", (u_id, job_id))

    conn.commit()
    db.close_db()

    return True

# Checks if job has already been applied to
def already_applied(u_id, job_id):
    conn = db.get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM applied WHERE user_id = ? AND job_id = ?;", (u_id, job_id))

    result = cur.rowcount > 0

    db.close_db()

    return result

# Removes job posting to applied
def remove_from_applied(u_id, job_posting):
    # Getting db and cursor
    conn = db.get_db()
    cur = conn.cursor()

    job_id = job_posting['id']

    cur.execute("SELECT * FROM applied WHERE user_id = ? AND job_id = ?;", (u_id, job_id))

    if cur.rowcount != 0:
        cur.execute("DELETE FROM applied WHERE user_id = ? AND job_id = ?;", (u_id, job_id))

        conn.commit()

    db.close_db()

    return True
