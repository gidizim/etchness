from . import db
from werkzeug.security import check_password_hash, generate_password_hash

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
        raise ValueError("Email already taken")

    # Creating user and obtaining u_id
    cur.execute("INSERT INTO user (email, password, first_name, last_name) VALUES (?, ?, ?, ?);", data)
    cur.execute("SELECT id FROM user WHERE email = '%s' AND password = '%s';" % (email, password))
    u_id = cur.fetchone()[0]

    conn.commit()
    db.close_db()

    return u_id

# Attempts to log in returns boolean on whether it was successful or not
def login(email, password):
    conn = db.get_db()
    cur = conn.cursor()

    cur.execute("SELECT id, password FROM user WHERE email = '%s';" % email)

    if len(cur.fetchall()) == 0:
        db.close_db()
        raise ValueError("No user with given email")


    (u_id, expected_password) = cur.fetchall()

    check_password_hash(expected_password, password)

    if not check_password_hash(expected_password, password):
        db.close_db()
        raise ValueError("Incorrect password")

    # Saving changes and disconnecting from DB
    db.close_db()
    return u_id


# Since we aren't doing token checking atm, there is no token to invalidate
def logout(token):
    return True

