from . import db

# Returns a dictionary of user details from the database
def get_user_details(u_id):
    conn = db.get_db()
    cur = conn.cursor()


    cur.execute("SELECT * FROM user WHERE id = '%s';" % u_id)

    data = cur.fetchall()
    if len(data) == 0:
        db.close_db()

        raise ValueError("Invalid user id")

    data = data[0]
    result = {}
    result['email'] = data['email']
    result['password'] = '**********'
    result['first_name'] = data['first_name']
    result['last_name'] = data['last_name']

    db.close_db()

    return result

# Updates the given user's information in db
def set_user_details(u_id, email, first_name, last_name):
    conn = db.get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM user WHERE email = '%s';" % email)

    data = cur.fetchall()
    if len(data) != 0:
        db.close_db()

        raise ValueError("Account with Email already taken")

    cur.execute("UPDATE user SET email = '%s', first_name = '%s', last_name = '%s' WHERE id = '%s';"
                % (email, first_name, last_name, u_id))

    conn.commit()
    db.close_db()

def reset_password(u_id, hashed_password):
    conn = db.get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM user WHERE id = '%s';" % u_id)

    data = cur.fetchall()
    if len(data) == 0:
        db.close_db()

        raise ValueError("Invalid user id")

    cur.execute("UPDATE user SET password = '%s' WHERE id = '%s';"
                % (hashed_password, u_id))

    conn.commit()
    db.close_db()







