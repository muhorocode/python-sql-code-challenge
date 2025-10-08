# Object Relations Code Challenge - Articles

Python project for managing authors, magazines, and articles using raw SQL (no SQLAlchemy).

### Phase 1: Setup
- Project structure created
- Virtual environment set up
- Git repository initialized

### Phase 2: Database
- SQLite database connection (`database_utils.py`)
- Tables created: authors, magazines, articles
- Foreign key constraints working

### Phase 3: Classes
- **Author class**: Create, save, find by ID. Name is read-only.
- **Magazine class**: Create, save, find by ID. Name and category can be updated.
- **Article class**: Create, save, find by ID. Title is read-only. Links authors to magazines.

### Phase 4: Relationships
- **Author relationships**: Get articles by author, magazines they've written for, topic areas
- **Magazine relationships**: Get articles in magazine, contributing authors, article titles
- **Advanced queries**: Authors with 2+ articles per magazine, unique categories per author

## How to Run

1. Activate virtual environment: `source venv/bin/activate`
2. Test current work: `python debug.py` and `pytest -q`

## Files Structure

- `lib/database_utils.py` - Database setup
- `lib/author.py` - Author class
- `lib/magazine.py` - Magazine class  
- `lib/article.py` - Article class (completed)
- `debug.py` - For testing classes
- `tests/test_all.py` - Test suite