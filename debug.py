from lib.database_utils import create_tables, get_connection

def test_database():
    print('printing database...')
    create_tables()

    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables=cursor.fetchall()
    print('tables created:', tables)
    conn.close()

if __name__=='__main__':
    test_database()