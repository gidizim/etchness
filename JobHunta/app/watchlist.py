from . import db

# Gets list of jobs by a given u_id, returns a list of job postings
def get_watchlist(u_id):

    # Getting db and cursor
    conn = db.get_db()
    cur = conn.cursor()

    cur.execute("""SELECT * FROM job, watchlist WHERE watchlist.user_id = '%s' AND watchlist.job_id = job.id AND watchlist.job_id NOT IN (SELECT id FROM job, applied WHERE applied.user_id = '%s' AND applied.job_id = job.id);""" % (u_id, u_id))

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
        curr_job['url'] = row['url']
        curr_job['created'] = row['created']
        curr_job['in_watchlist'] = row['in_watchlist']

        results.append(curr_job)

    db.close_db()

    return results

# Adds job posting to watchlist
def add_to_watchlist(u_id, job_posting):
    # Getting db and cursor
    conn = db.get_db()
    cur = conn.cursor()

    job_id = job_posting['url']

    in_watchlist = True

    job_data = (job_id,
                job_posting['title'],
                job_posting['job_type'],
                job_posting['description'],
                job_posting['location'],
                job_posting['company'],
                job_posting['created'],
                job_posting['url'],
                job_posting['salary'],
                in_watchlist)

    cur.execute("SELECT * FROM watchlist WHERE user_id = '%s' AND job_id = '%s';" % (u_id, job_id))

    data = cur.fetchall()
    if (len(data) == 0):
        cur.execute("INSERT INTO watchlist VALUES (?, ?);", (u_id, job_id))

    cur.execute("SELECT * FROM job WHERE id = '%s';" % job_id)
    result = cur.fetchall()
    # only add if not already in job list
    if len(result) == 0:
        cur.execute("INSERT INTO job VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?) ;", job_data)
    # update in_watchlist to True
    else:
        cur.execute("UPDATE job SET in_watchlist = ? WHERE id = ?;", (in_watchlist, job_id))

    conn.commit()
    db.close_db()

    return True

# Checks if job is in the watchlist
def in_watchlist(u_id, job_id):
    conn = db.get_db()
    cur = conn.cursor()
    print(u_id)
    print(job_id)
    cur.execute("SELECT * FROM watchlist WHERE user_id = '%s' AND job_id = '%s';" % (u_id, job_id))

    result = cur.fetchall()

    db.close_db()

    return len(result) > 0

# Removes job posting from watchlist
def remove_from_watchlist(u_id, job_id):
    # Getting db and cursor
    conn = db.get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM watchlist WHERE user_id = '%s' AND job_id = '%s';" % (u_id, job_id))
    cur.execute("UPDATE job SET in_watchlist = ? WHERE id = ?;", (False, job_id))

    if cur.rowcount != 0:
        cur.execute("DELETE FROM watchlist WHERE user_id = '%s' AND job_id = '%s';" % (u_id, job_id))
        conn.commit()


    db.close_db()

    return True

# reset in_watchlist in job table
def reset_watchlist():
    # Getting db and cursor
    conn = db.get_db()
    cur = conn.cursor()

    cur.execute("UPDATE job SET in_watchlist = ? WHERE in_watchlist = ?;", (False, True))

    db.close_db()
