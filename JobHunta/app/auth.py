from . import db

# Attempts to signup with user details, returns a user id to be used as a token
def signup(email, password, first_name, last_name):
    data = (email, password, first_name, last_name)

    # Getting db and cursor
    conn = db.get_db()
    cur = conn.cursor()

    # Creating user and obtaining u_id
    cur.execute("INSERT INTO user (email, password, first_name, last_name) VALUES (?, ?, ?, ?);", data)
    cur.execute("SELECT id FROM user WHERE email = ? AND password = ?;", email, password)
    u_id = cur.fetch()[0]

    conn.commit()
    db.close_db()

    return u_id

# Attempts to log in returns boolean on whether it was successful or not
def login(email, password):
    conn = db.get_db()
    cur = conn.cursor()

    # Getting expected password
    cur.execute("SELECT password FROM user WHERE email = ?;", email)

    expected_password = cur.fetch()[0]

    # Saving changes and disconnecting from DB
    conn.commit()
    db.close_db()

    return expected_password == password


# Since we aren't doing token checking atm, there is no token to invalidate
def logout(token):
    return True
