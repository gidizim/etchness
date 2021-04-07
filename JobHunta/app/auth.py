from . import db
from werkzeug.security import check_password_hash, generate_password_hash
from random import seed, randint

# Attempts to signup with user details, returns a user id to be used as a token
def signup(email, password, first_name, last_name):
    data = (email, password, first_name, last_name)

    # Getting db and cursor
    conn = db.get_db()
    cur = conn.cursor()

    # Checking if user already exists
    cur.execute("SELECT * FROM user WHERE email = '%s';" % email)

    if len(cur.fetchall()) > 0:
        db.close_db()

        # Raise error
        raise ValueError("Account with Email exists")

    # Creating user and obtaining u_id
    cur.execute("INSERT INTO user (email, password, first_name, last_name) VALUES (?, ?, ?, ?);", data)
    cur.execute("SELECT id FROM user WHERE email = '%s' AND password = '%s';" % (email, password))
    u_id = cur.fetchone()[0]

    conn.commit()
    db.close_db()

    return u_id

# Attempts to log in returns u_id
def login(email, password):
    conn = db.get_db()
    cur = conn.cursor()

    cur.execute("SELECT id, password FROM user WHERE email = '%s';" % email)

    data = cur.fetchall()
    if len(data) == 0:
        db.close_db()
        raise ValueError("No user with given email")

    # Getting u_id
    (u_id, expected_password) = data[0]

    # Checking password
    if not check_password_hash(expected_password, password):
        db.close_db()
        raise ValueError("Incorrect password")

    # Saving changes and disconnecting from DB
    db.close_db()
    return u_id


def generate_reset_token(email):
    conn = db.get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM user WHERE email = '%s';" % email)

    data = cur.fetchall()
    if len(data) == 0:
        db.close_db()
        raise ValueError("No user with given email")

    cur.execute("SELECT * FROM password_reset WHERE email = '%s';" % email)

    token = ""
    for i in range(4):
        token += str(randint(0, 9))

    data = cur.fetchall()

    if len(data) == 0:
        cur.execute("INSERT INTO password_reset VALUES (?, ?);", (email, token))

    else:
        cur.execute("UPDATE password_reset SET token = '%s' WHERE email = '%s';" % (token, email))

    conn.commit()
    db.close_db()

    return token

def check_reset_token(email, token):
    conn = db.get_db()
    cur = conn.cursor()

    if len(token) != 4:
        raise ValueError("Invalid Token")

    cur.execute("SELECT * FROM password_reset WHERE email = '%s' AND token = '%s';" % (email, token))

    data = cur.fetchall()

    db.close_db()
    return len(data) == 1
