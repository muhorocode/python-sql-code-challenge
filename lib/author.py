from .database_utils import get_connection

class Author:
# initialize a new author instance
    def __init__(self,name,id=None):
# store the db ID (none for new authors)
        self._id=id
# initialize _name as none
        self._name=None
# use the setter to set the name (with validation)
        self.name=name

# getter for authors id (read-only)
    @property
    def id(self):
        return self._id

# getter for authors name
    @property
    def name(self):
        return self._name

# setter for authors name with validation
    @name.setter
    def name(self,value):
# check whether the name has already been set
        if hasattr(self,'_name') and self._name is not None:
            raise AttributeError("Can't modify author name")

# validate that it is a string and raise an error if not
        if not isinstance(value,str):
            raise TypeError('Author name must be a string')

# validate that the string is not empty
        if len(value)==0:
            raise ValueError('Authors name must be longer than 0 characters')
# store the name when all the validation checks pass
        self._name=value

# class method to create an author instance from a db row
    @classmethod
    def new_from_db(cls,row):
# checks whether a row was returned
        if row is None:
            return None # return None if no row was found

# create and return a new author instance
        return cls(name=row[1], id=row[0])

# class method to find an author by id
    @classmethod
    def find_by_id(cls,id):
# connect to the db
        conn=get_connection()
# cursor to execute the query
        cursor=conn.cursor()
# execute a select query to find the author by id
        cursor.execute("SELECT * FROM authors WHERE id=?",(id,))
# fetch the first row from the result that matches
        row=cursor.fetchone()
# close the connection
        conn.close()
# create and return an author instance from the row
        return cls.new_from_db(row)

# instance method to save the author to the db
    def save(self):
# connection to the db
        conn=get_connection()
# cursor to execute the sql
        cursor=conn.cursor()
# check whether the author already has an id or not
        if self._id is None:
# means the author is new and needs to be inserted
            cursor.execute("INSERT INTO authors (name) VALUES (?)",
            (self._name,))
# get the id of the newly inserted author
            self._id=cursor.lastrowid
            print(f'created new author with ID: {self._id}')
        else:
# author exists and needs to be updated
            cursor.execute(
                "UPDATE authors SET name= ? WHERE id=?",
                (self._name,self._id)
            )
            print(f'updated author ID: {self._id}')

# commit the changes and close the connection
        conn.commit()
        conn.close()

# the relationship method to get all the articles by this author
    def articles(self):
        conn=get_connection()
        cursor=conn.cursor()
# find all articles where the author id matches this author id
        cursor.execute("SELECT * FROM articles WHERE author_id=?", (self._id,))
        rows=cursor.fetchall() # get all matching rows
        conn.close()

# convert rows to article objects and return them
        from .article import Article
        return [Article.new_from_db(row) for row in rows]

    # relationship method to get all the magazines this author has written for
    def magazines(self):
        conn=get_connection()
        cursor=conn.cursor()
        # usage of join to get all magazines that have articles by this author and DISTINCT to remove duplicates
        cursor.execute('''
            SELECT DISTINCT m.* FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            WHERE a.author_id=?
        ''', (self._id,))
        # fetch all matching rows
        rows=cursor.fetchall()
        conn.close()
        # convert rows to magazine objects and return them
        from .magazine import Magazine
        return [Magazine.new_from_db(row) for row in rows]
    
    # method to create a new article for this author
    def add_article(self, title, magazine):
        from .article import Article
        # create a new article instance with this author and the given magazine
        new_article = Article(title=title, author=self, magazine=magazine)
        # save the new article to the db
        new_article.save()
        # return the newly created article
        return new_article
    
    # method to get unique categories of magazines this author has written for
    def topic_areas(self):
        # get all magazines this author has written for
        author_magazines = self.magazines()
        # extract unique categories from the magazines
        categories = []
        for magazine in author_magazines:
            if magazine.category not in categories:
                categories.append(magazine.category)
        # return list of unique categories
        return categories
# string rep of the author for debugging and printing
    def __repr__(self):
        return f'<Author id={self._id} name={self._name}>'