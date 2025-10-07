from .database_utils import get_connection
from .author import Author
from .magazine import Magazine

# initialize new article instance
class Article:
    def __init__(self,title,author,magazine,id=None):
        self._id=id #store the db ID
        self._title=None # initialize _title as none
        self.title=title # use the setter to set the title
        self._author=author # store the author instance
        self._magazine=magazine # store the magazine instance

    # getter for articles id (read-only)
    @property
    def id(self):
        return self._id
    # getter for articles title
    @property
    def title(self):
        return self._title
    # setter for articles title with validation
    @title.setter
    def title(self,value):
        #check whether the title has already been set
        if hasattr(self,'_title') and self._title is not None:
            raise AttributeError('cant modify article title')
        #check whether it is a string and raise an error if not
        if not isinstance(value,str):
            raise TypeError('Article title must be a string')
        # confirm that the string is not empty
        if len(value)==0:
            raise ValueError('Article title must be longer than 0 characters')
        # storing the title when all the validation checks pass
        self._title=value

    # getter for article's author (read-only)
    @property
    def author(self):
        return self._author
    # getter for article's magazine (read-only)
    @property
    def magazine(self):
        return self._magazine


    # class method to create an article
    @classmethod
    def new_from_db(cls,row):
        # check if row has been returned
        if row is None:
            return None
        # get data from the row
        article_id=row[0]
        title=row[1]
        author_id=row[2]
        magazine_id=row[3]

        # fetch the author and magazine object using their ids

        author= Author.find_by_id(author_id)
        magazine=Magazine.find_by_id(magazine_id)

        #create and return new article instance
        return cls(title=title, author=author, magazine=magazine, id=article_id)

    #class method to find an article by their id
    @classmethod
    def find_by_id(cls,id):
        conn=get_connection()
        cursor=conn.cursor()
        # execute a select query to find the article by id
        cursor.execute("SELECT * FROM articles WHERE id=?", (id,))
        # fetch the first row from the result that matches
        row = cursor.fetchone()
        # close the connection
        conn.close()
        # create and return an article instance from the row
        return cls.new_from_db(row)

    # instance method to save the article to the db
    def save(self):
        conn=get_connection()
        cursor=conn.cursor()
        #check if the article already exists in the db
        if self._id is None:
            #insert article into the db since it does not exist
            cursor.execute("INSERT INTO articles (title, author_id, magazine_id) VALUES (?,?,?)", 
                         (self._title, self._author.id, self._magazine.id))
            #get the id of the newly inserted article
            self._id=cursor.lastrowid
            print(f'created new article with ID: {self._id}')
        else:
            #article exists and needs to be updated
            cursor.execute("UPDATE articles SET title=?, author_id=?, magazine_id=? WHERE id=?",
            (self._title, self._author.id, self._magazine.id, self._id))
            print(f'updated article with ID: {self._id}')
        #save the changes and close the connection
        conn.commit()
        conn.close()

    #string rep of the article for easy debugging
    def __repr__(self):
        return f'<Article id={self._id} title={self._title} author={self._author.name} magazine={self._magazine.name}>'