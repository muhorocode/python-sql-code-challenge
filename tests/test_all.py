import pytest

from lib import database_utils
from lib.database_utils import get_connection, create_tables
from lib.author import Author
from lib.magazine import Magazine
from lib.article import Article


@pytest.fixture(autouse=True)
def setup_isolated_db(tmp_path, monkeypatch):
    """
    Use a temporary SQLite database for each test to ensure isolation.
    Patches the DB_FILE used by get_connection and creates tables.
    """
    db_path = tmp_path / "test_magazine.db"
    monkeypatch.setattr(database_utils, "DB_FILE", str(db_path))
    create_tables()
    yield


# ----------------------
# Database setup tests
# ----------------------

def test_create_tables_creates_expected_tables():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
    tables = {row[0] for row in cur.fetchall()}
    conn.close()

    assert {"articles", "authors", "magazines"}.issubset(tables)


# ----------------------
# Author tests
# ----------------------

def test_author_create_save_and_find_by_id():
    author = Author("Alice")
    assert author.id is None

    author.save()
    assert isinstance(author.id, int)

    found = Author.find_by_id(author.id)
    assert found is not None
    assert found.id == author.id
    assert found.name == "Alice"


def test_author_name_is_read_only_and_validated():
    # read-only after initial set
    author = Author("Bob")
    author.save()
    with pytest.raises(AttributeError):
        author.name = "Robert"

    # validation on initialization
    with pytest.raises(TypeError):
        Author(123)  # type must be string
    with pytest.raises(ValueError):
        Author("")  # non-empty


# ----------------------
# Magazine tests
# ----------------------

def test_magazine_create_update_and_find_by_id():
    mag = Magazine("Tech Today", "Technology")
    assert mag.id is None

    mag.save()
    assert isinstance(mag.id, int)

    fetched = Magazine.find_by_id(mag.id)
    assert fetched is not None
    assert fetched.name == "Tech Today"
    assert fetched.category == "Technology"

    # update allowed for Magazine
    mag.name = "Tech Tomorrow"
    mag.category = "Science"
    mag.save()

    updated = Magazine.find_by_id(mag.id)
    assert updated.name == "Tech Tomorrow"
    assert updated.category == "Science"


def test_magazine_validations():
    # type validations
    with pytest.raises(TypeError):
        Magazine(123, "Category")
    with pytest.raises(TypeError):
        Magazine("Name", 456)

    # non-empty validations
    with pytest.raises(ValueError):
        Magazine("", "Category")
    with pytest.raises(ValueError):
        Magazine("Name", "")


# ----------------------
# Article tests
# ----------------------

def test_article_create_save_and_find_by_id():
    author = Author("Alice")
    author.save()

    mag = Magazine("Science Weekly", "Science")
    mag.save()

    article = Article("Python 101", author, mag)
    assert article.id is None

    article.save()
    assert isinstance(article.id, int)

    fetched = Article.find_by_id(article.id)
    assert fetched is not None
    assert fetched.title == "Python 101"
    assert fetched.author.id == author.id
    assert fetched.magazine.id == mag.id


def test_article_title_read_only_and_validated():
    author = Author("Carol")
    author.save()

    mag = Magazine("Data Monthly", "Data")
    mag.save()

    with pytest.raises(ValueError):
        Article("", author, mag)
    with pytest.raises(TypeError):
        Article(123, author, mag)

    article = Article("Valid Title", author, mag)
    article.save()
    with pytest.raises(AttributeError):
        article.title = "New Title"


# ----------------------
# Relationship tests
# ----------------------

def test_author_and_magazine_relationships_and_helpers():
    # authors
    a1 = Author("Author One")
    a1.save()
    a2 = Author("Author Two")
    a2.save()

    # magazines
    m1 = Magazine("Mag One", "Cat1")
    m1.save()
    m2 = Magazine("Mag Two", "Cat2")
    m2.save()

    # articles
    Article("T1", a1, m1).save()
    Article("T2", a1, m1).save()
    Article("T3", a1, m2).save()
    Article("T4", a2, m1).save()

    # Author.articles
    a1_titles = {art.title for art in a1.articles()}
    assert a1_titles == {"T1", "T2", "T3"}

    # Author.magazines (unique)
    a1_mag_names = {mag.name for mag in a1.magazines()}
    assert a1_mag_names == {"Mag One", "Mag Two"}

    # Author.topic_areas (unique categories)
    a1_topic_areas = set(a1.topic_areas())
    assert a1_topic_areas == {"Cat1", "Cat2"}

    # Magazine.articles
    m1_titles = {art.title for art in m1.articles()}
    assert m1_titles == {"T1", "T2", "T4"}

    # Magazine.contributors (unique authors)
    m1_contribs = {auth.name for auth in m1.contributors()}
    assert m1_contribs == {"Author One", "Author Two"}

    # Magazine.article_titles convenience list
    assert set(m1.article_titles()) == {"T1", "T2", "T4"}

    # Magazine.contributing_authors (>2 articles in this magazine)
    # current counts: a1 has 2 in m1, a2 has 1 in m1 -> none should qualify
    assert {auth.name for auth in m1.contributing_authors()} == set()

    # add one more article for a1 in m1 to push over threshold
    Article("T5", a1, m1).save()
    assert {auth.name for auth in m1.contributing_authors()} == {"Author One"}
