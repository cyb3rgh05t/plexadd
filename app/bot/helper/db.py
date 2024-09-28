import sqlite3

from app.bot.helper.dbupdater import check_table_version, update_table

DB_URL = 'app/config/app.db'
DB_TABLE = 'clients'

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("Connected to DataBase")
    except Error as e:
        print("Error in connecting to DataBase")
    finally:
        if conn:
            return conn

def checkTableExists(dbcon, tablename):
    dbcur = dbcon.cursor()
    dbcur.execute("""SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='{0}';""".format(tablename.replace('\'', '\'\'')))
    if dbcur.fetchone()[0] == 1:
        dbcur.close()
        return True
    dbcur.close()
    return False

conn = create_connection(DB_URL)

# Checking if table exists
if checkTableExists(conn, DB_TABLE):
	print('Table exists.')
else:
    conn.execute(
    '''CREATE TABLE "clients" (
    "id"	INTEGER NOT NULL UNIQUE,
    "discord_username"	TEXT NOT NULL UNIQUE,
    "email"	TEXT,
    "jellyfin_username" TEXT,
    PRIMARY KEY("id" AUTOINCREMENT)
    );''')

update_table(conn, DB_TABLE)

def save_user_email(username, email):
    if username and email:
        conn.execute(f"""
            INSERT OR REPLACE INTO clients(discord_username, email)
            VALUES('{username}', '{email}')
        """)
        conn.commit()
        print("User added to DataBase.")
    else:
        return "Username and email cannot be empty"

def save_user(username):
    if username:
        conn.execute("INSERT INTO clients (discord_username) VALUES ('"+ username +"')")
        conn.commit()
        print("User added to DataBase.")
    else:
        return "Username cannot be empty"
    
def save_user_jellyfin(username, jellyfin_username):
    if username and jellyfin_username:
        conn.execute(f"""
            INSERT OR REPLACE INTO clients(discord_username, jellyfin_username)
            VALUES('{username}', '{jellyfin_username}')
        """)
        conn.commit()
        print("User added to db.")
    else:
        return "Discord and Jellyfin usernames cannot be empty"

def save_user_all(username, email, jellyfin_username):
    if username and email and jellyfin_username:
        conn.execute(f"""
            INSERT OR REPLACE INTO clients(discord_username, email, jellyfin_username)
            VALUES('{username}', '{email}', '{jellyfin_username}')
        """)
        conn.commit()
        print("User added to db.")
    elif username and email:
        save_user_email(username, email)
    elif username and jellyfin_username:
        save_user_jellyfin(username, jellyfin_username)
    elif username:
        save_user(username)
    else:
        return "Discord username must all be provided"

def get_useremail(username):
    if username:
        try:
            cursor = conn.execute('SELECT discord_username, email from clients where discord_username="{}";'.format(username))
            for row in cursor:
                email = row[1]
            if email:
                return email
            else:
                return "No email found"
        except:
            return "Error in fetching from DataBase"
    else:
        return "username cannot be empty"

def get_jellyfin_username(username):
    """
    Get jellyfin username of user based on discord username

    param   username: discord username

    return  jellyfin username
    """
    if username:
        try:
            cursor = conn.execute('SELECT discord_username, jellyfin_username from clients where discord_username="{}";'.format(username))
            for row in cursor:
                jellyfin_username = row[1]
            if jellyfin_username:
                return jellyfin_username
            else:
                return "No users found"
        except:
            return "Error in fetching from DataBase"
    else:
        return "Username cannot be empty"

def remove_email(username):
    """
    Sets email of discord user to null in database
    """
    if username:
        conn.execute(f"UPDATE clients SET email = null WHERE discord_username = '{username}'")
        conn.commit()
        print(f"Email removed from user {username} in DataBase")
        return True
    else:
        print(f"Username cannot be empty.")
        return False

def remove_jellyfin(username):
    """
    Sets jellyfin username of discord user to null in database
    """
    if username:
        conn.execute(f"UPDATE clients SET jellyfin_username = null WHERE discord_username = '{username}'")
        conn.commit()
        print(f"Jellyfin username removed from user {username} in DataBase")
        return True
    else:
        print(f"Username cannot be empty.")
        return False


def delete_user(username):
    if username:
        try:
            conn.execute('DELETE from clients where discord_username="{}";'.format(username))
            conn.commit()
            return True
        except:
            return False
    else:
        return "Username cannot be empty"

def read_all():
    cur = conn.cursor()
    cur.execute("SELECT * FROM clients")
    rows = cur.fetchall()
    all = []
    for row in rows:
        #print(row[1]+' '+row[2])
        all.append(row)
    return all