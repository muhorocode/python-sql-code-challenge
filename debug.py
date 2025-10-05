from lib.database_utils import create_tables, get_connection
from lib.author import Author
from lib.magazine import Magazine

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

def test_magazine():
    print('\n=== Testing Magazine Class ===')
    
    # Test creating a new magazine
    magazine1 = Magazine("Tech Today", "Technology")
    print(f'Before save: {magazine1}')
    
    # Test saving to database
    magazine1.save()
    print(f'After save: {magazine1}')
    
    # Test finding by ID
    found_magazine = Magazine.find_by_id(magazine1.id)
    print(f'Found magazine: {found_magazine}')
    
    # Test creating another magazine
    magazine2 = Magazine("Fashion Weekly", "Fashion")
    magazine2.save()
    print(f'Second magazine: {magazine2}')
    
    # Test updating magazine properties (should work unlike Author)
    magazine1.name = "Tech Tomorrow"
    magazine1.category = "Science"
    magazine1.save()
    print(f'Updated magazine: {magazine1}')
    
    # Test validation - empty name should fail
    try:
        invalid_magazine = Magazine("", "Category")
    except ValueError as e:
        print(f'✅ Name validation works: {e}')
    
    # Test validation - empty category should fail
    try:
        invalid_magazine2 = Magazine("Name", "")
    except ValueError as e:
        print(f'✅ Category validation works: {e}')

if __name__=='__main__':
    test_database()
    test_author()
    test_magazine()