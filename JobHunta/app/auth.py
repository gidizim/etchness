from . import db

def signup(email, password, first_name, last_name):
    data = (email, password, first_name, last_name)
    conn = db.get_db()
    cur = conn.cursor()

    cur.execute("INSERT INTO user (email, password, first_name, last_name) VALUES (?, ?, ?, ?);", data)

    conn.commit()
    db.close_db()

    return email


def login(email, password):
    conn = db.get_db()
    cur = conn.cursor()

    cur.execute("SELECT password FROM user WHERE email = ?", email)

    expected_password = cur.fetch()[0]

    conn.commit()
    db.close_db()

    return expected_password == password


def logout(token):
    return True
