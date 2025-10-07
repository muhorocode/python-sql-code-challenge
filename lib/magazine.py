from .database_utils import get_connection

class Magazine:
    # initialize a new magazine instance
    def __init__(self, name, category, id=None):
        # store the db ID (none for new magazines)
        self._id = id
        # initialize _name as none
        self._name = None
        # initialize _category as none
        self._category = None
        # set name and categories with validation
        self.name = name
        self.category = category

    # getter for magazines id (read-only)
    @property
    def id(self):
        return self._id
    
    # getter for magazines name
    @property
    def name(self):
        return self._name
    
    # setter for magazines name with validation
    @name.setter
    def name(self, value):
        # validate whether it is a string and raise an error if not
        if not isinstance(value, str):
            raise TypeError('Magazine name must be a string')
        # validate that the string is not empty
        if len(value) == 0:
            raise ValueError('Magazine name must be longer than 0 characters')
        # store the name when all the validation checks pass
        self._name = value
    
    # getter for magazines category
    @property
    def category(self):
        return self._category
    
    # setter for magazines category with validation
    @category.setter
    def category(self, value):
        # validate whether it is a string and raise an error if not
        if not isinstance(value, str):
            raise TypeError('Magazine category must be a string')
        # validate that the string is not empty
        if len(value) == 0:
            raise ValueError('Magazine category must be longer than 0 characters')
        # store the category when all the validation checks pass
        self._category = value

    # class method to create a magazine instance from a db row
    @classmethod
    def new_from_db(cls, row):
        # check whether row was returned
        if row is None:
            return None
        # create and return a new magazine instance
        return cls(name=row[1], category=row[2], id=row[0])

    # class method to find a magazine by id
    @classmethod
    def find_by_id(cls, id):
        # db connection
        conn = get_connection()
        # cursor to execute the query
        cursor = conn.cursor()
        # execute a select query to find the magazine by id
        cursor.execute("SELECT * FROM magazines WHERE id=?", (id,))
        # fetch the first row from the result that matches
        row = cursor.fetchone()
        # close the connection
        conn.close()
        # create and return a magazine instance from the row
        return cls.new_from_db(row)

    # instance method to save the magazine to the db
    def save(self):
        # db connection
        conn = get_connection()
        # cursor to execute the query
        cursor = conn.cursor()
        # check whether the magazine already has an id or not
        if self._id is None:
            # means the magazine is new and needs to be inserted
            cursor.execute("INSERT INTO magazines (name, category) VALUES (?,?)",
                         (self._name, self._category))
            # get the id of the newly inserted magazine
            self._id = cursor.lastrowid
            print(f'created new magazine with ID: {self._id}')
        else:
            # magazine already exists and needs to be updated
            cursor.execute("UPDATE magazines SET name=?, category=? WHERE id=?",
                         (self._name, self._category, self._id))
            print(f'updated magazine ID: {self._id}')
        
        # commit the changes and close the connection
        conn.commit()
        conn.close()

    # relationship method to get all the articles in this magazine
    def articles(self):
        conn=get_connection()
        cursor=conn.cursor()
        # find all articles where the magazine id matches this magazine id
        cursor.execute("SELECT * FROM articles WHERE magazine_id=?", (self._id,))
        #get all matching rows
        rows=cursor.fetchall()
        conn.close()
        #convert rows to article objects and return them
        from .article import Article
        return [Article.new_from_db(row) for row in rows]

    #relationship method to get all the authors that have written for this magazine
    def contributors(self):
        conn=get_connection()
        cursor=conn.cursor()
        # find all authors that have written articles for this magazine using a join query
        cursor.execute('''
            SELECT DISTINCT a.id, a.name FROM authors a
            JOIN articles ar ON a.id = ar.author_id
            WHERE ar.magazine_id=?
        ''', (self._id,))
        rows=cursor.fetchall() # get all matching rows
        conn.close()
        # convert rows to author objects and return them
        from .author import Author
        return [Author.new_from_db(row) for row in rows]
    
    # method to get all article titles in this magazine
    def article_titles(self):
        conn = get_connection()
        cursor = conn.cursor()
        # select only titles from articles in this magazine
        cursor.execute("SELECT title FROM articles WHERE magazine_id=?", (self._id,))
        # get all matching rows
        rows = cursor.fetchall()
        conn.close()
        # extract titles from rows
        return [row[0] for row in rows]

    # method to get authors who wrote more than 2 articles for this magazine
    def contributing_authors(self):
        conn = get_connection()
        cursor = conn.cursor()
        # use GROUP BY and HAVING to find authors with more than 2 articles in this magazine
        cursor.execute('''
            SELECT a.id, a.name FROM authors a
            JOIN articles ar ON a.id = ar.author_id
            WHERE ar.magazine_id=?
            GROUP BY a.id
            HAVING COUNT(ar.id) > 2
        ''', (self._id,))
        rows = cursor.fetchall()  # get all matching rows
        conn.close()
        # convert rows to author objects and return them
        from .author import Author
        return [Author.new_from_db(row) for row in rows]
    # string representation of the magazine for debugging and printing
    def __repr__(self):
        return f'<Magazine id={self._id} name={self._name} category={self._category}>'