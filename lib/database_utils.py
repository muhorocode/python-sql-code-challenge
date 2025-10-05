# database connection setup
import sqlite3

DB_FILE='magazine.db'

# function to be used to connect to the database
def get_connection():
    return sqlite3.connect(DB_FILE)

# creating the db tables with the proper foreign key constraints

def create_tables():
# connection to the db
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
# creating the authors table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS authors(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL)''')
# creating the magazines table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS magazines(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL)''')

# creating the articles table with foreign keys to authors and magazines
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS articles(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author_id INTEGER,
            magazine_id INTEGER,
            FOREIGN KEY (author_id) REFERENCES authors(id),
            FOREIGN KEY (magazine_id) REFERENCES magazines(id))''')
# save the changes and close the connection
    conn.commit()
    conn.close()
    print("Database created successfully!")
    