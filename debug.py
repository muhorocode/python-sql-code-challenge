from lib.database_utils import create_tables, get_connection
from lib.author import Author

def test_database():
    print('=== Testing Database ===')
    create_tables()

    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables=cursor.fetchall()
    print('tables created:', tables)
    conn.close()

def test_author():
    print('\n=== Testing Author Class ===')
    
# Test creating a new author
    author1 = Author("John Doe")
    print(f'Before save: {author1}')
    
# Test saving to database
    author1.save()
    print(f'After save: {author1}')
    
# Test finding by ID
    found_author = Author.find_by_id(author1.id)
    print(f'Found author: {found_author}')
    
# Test creating another author
    author2 = Author("Jane Smith")
    author2.save()
    print(f'Second author: {author2}')
    
# Test validation - this should fail
    try:
        invalid_author = Author("")
    except ValueError as e:
        print(f'✅ Validation works: {e}')

if __name__=='__main__':
    test_database()
    test_author()