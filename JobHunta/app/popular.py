from . import db

#
def get_popular_jobs():
    conn = db.get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM job, popular WHERE popular.job_id = job.id;")

    results = []

    for row in cur.fetchall():

        curr_job = {}
        curr_job['id'] = row['id']
        curr_job['title'] = row['title']
        curr_job['job_type'] = row['job_type']
        curr_job['description'] = row['description']
        curr_job['location'] = row['location']
        curr_job['company'] = row['company']
        curr_job['created'] = row['created']
        curr_job['url'] = row['url']
        curr_job['salary'] = row['salary']

        results.append(dict(curr_job))


    db.close_db()


    return results

# Creates an entry
def append_popular_job(job_posting):

    conn = db.get_db()
    cur = conn.cursor()

    job_id = job_posting['url']
    
    job_data = (job_id,
                job_posting['title'],
                job_posting['job_type'],
                job_posting['description'],
                job_posting['location'],
                job_posting['company'],
                job_posting['created'],
                job_posting['url'],
                job_posting['salary'])


    cur.execute("INSERT INTO job VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?) ;", job_data)
    cur.execute("INSERT INTO popular VALUES ( ? ) ;", (job_id,))

    conn.commit()

    db.close_db()

# Removes all jobs from popular list
def clear_popular_job():
    conn = db.get_db()
    cur = conn.cursor()

    cur.execute("DELETE FROM popular;")

    conn.commit()

    db.close_db()
