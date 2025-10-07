from lib.database_utils import create_tables, get_connection
from lib.author import Author
from lib.magazine import Magazine
from lib.article import Article

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
    author1 = Author("Elijah Kamanga")
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

def test_article():
    print('\n=== Testing Article Class ===')
    
    # First create author and magazine for the article
    author = Author("Alice Johnson")
    author.save()
    
    magazine = Magazine("Science Weekly", "Science")
    magazine.save()
    
    # Test creating a new article
    article1 = Article("Python in today's world", author, magazine)
    print(f'Before save: {article1}')
    
    # Test saving to database
    article1.save()
    print(f'After save: {article1}')
    
    # Test finding by ID
    found_article = Article.find_by_id(article1.id)
    print(f'Found article: {found_article}')
    
    # Test creating another article with same author, different magazine
    magazine2 = Magazine("Tech News", "Technology")
    magazine2.save()
    
    article2 = Article("Python Tips", author, magazine2)
    article2.save()
    print(f'Second article: {article2}')
    
    # Test article properties
    print(f'Article title: {article1.title}')
    print(f'Article author: {article1.author.name}')
    print(f'Article magazine: {article1.magazine.name}')
    
    # Test validation - empty title should fail
    try:
        invalid_article = Article("", author, magazine)
    except ValueError as e:
        print(f'✅ Title validation works: {e}')
    
    # Test read-only title
    try:
        article1.title = "New Title"
    except AttributeError as e:
        print(f'✅ Title is read-only: {e}')

if __name__=='__main__':
    test_database()
    test_author()
    test_magazine()
    test_article()