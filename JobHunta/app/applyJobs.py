from . import db

# Gets list of jobs by a given u_id, returns a list of job postings
def get_applied(u_id):

    # Getting db and cursor
    conn = db.get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM job, applied WHERE applied.user_id = '%s' AND applied.job_id = job.id;" % (u_id))

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

# Adds job posting to applied
def add_to_applied(u_id, job_posting):
    # Getting db and cursor
    conn = db.get_db()
    cur = conn.cursor()

    job_id = job_posting['url']


    cur.execute("SELECT * FROM job WHERE  id = '%s';" % (job_id))

    # If no job with that id exists, add that job the list of jobs
    if len(cur.fetchall()) == 0:
        job_data = (job_posting['id'],
                    job_posting['title'],
                    job_posting['job_type'],
                    job_posting['description'],
                    job_posting['location'],
                    job_posting['company'],
                    job_posting['url'],
                    job_posting['salary'])


        cur.execute("INSERT INTO job VALUES (?, ?, ?, ?, ?, ?, ?, ?) ;", job_data)

    cur.execute("SELECT * FROM applied WHERE  job_id = '%s' AND user_id = '%s';" % (job_id, u_id))
    data = cur.fetchall()
    if len(data) == 0:
        cur.execute("INSERT INTO applied VALUES (?, ?, 0, 0, 0);", (u_id, job_id))
    else:
        flag = 0
        for i, res in enumerate(data[0]):
            if res == 1:
                flag = i

        if flag == 0:
            cur.execute("UPDATE applied SET responded = 1 WHERE job_id = '%s' AND user_id = '%s';" % (job_id, u_id))

        elif flag == 2:
            cur.execute("UPDATE applied SET interviewed = 1 WHERE job_id = '%s' AND user_id = '%s';" % (job_id, u_id))

        elif flag == 3:
            cur.execute("UPDATE applied SET finalised = 1 WHERE job_id = '%s' AND user_id = '%s';" % (job_id, u_id))

        else:
            pass
    conn.commit()
    db.close_db()

    return True

# Checks if job has already been applied to
def already_applied(u_id, job_id):
    conn = db.get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM applied WHERE user_id = '%s' AND job_id = '%s';" % (u_id, job_id))

    if len(cur.fetchall()) == 0:
        db.close_db()
        return (0, 0, 0, 0)

    cur.execute("SELECT SUM(responded), SUM(interviewed), SUM(finalised) FROM applied WHERE job_id = '%s' AND user_id = '%s';" % (job_id, u_id))

    data = cur.fetchall()
    data = data[0]
    db.close_db()
    return (1, data[0], data[1], data[2])

# Removes job posting to applied
def remove_from_applied(u_id, job_posting):
    conn = db.get_db()
    cur = conn.cursor()

    job_id = job_posting['url']

    cur.execute("SELECT * FROM applied WHERE user_id = '%s' AND job_id = '%s';" % (u_id, job_id))

    if len(cur.fetchall()) == 0:
        db.close_db()
        return

    cur.execute("DELETE FROM applied WHERE  user_id = '%s' AND job_id = '%s';" % (u_id, job_id))

    conn.commit()
    db.close_db()
    return

# Returns a tuple of number of users interviewed/applied etc
def get_num_applied(job_id):
    conn = db.get_db()
    cur = conn.cursor()

    print(job_id)
    cur.execute("SELECT * FROM applied WHERE job_id = '%s';" % (job_id))

    print(cur.rowcount)
    if len(cur.fetchall()) == 0:
        db.close_db()
        return (0, 0, 0, 0)

    cur.execute("SELECT COUNT(*), SUM(responded), SUM(interviewed), SUM(finalised) FROM applied WHERE job_id = '%s';" % (job_id))

    data = cur.fetchall()
    data = data[0]
    db.close_db()
    return (data[0], data[1], data[2], data[3])
