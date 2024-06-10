from database.connection import get_db_connection

class Magazine:
    def __init__(self, id, name, category):
        self._id = id
        self.name = name
        self.category = category

    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, id):
        if not isinstance(id, int):
            raise TypeError("id must be of type int")
        self._id = id
        
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        if not isinstance(name, str):
            raise TypeError("name must be of type str")
        if not (2 <= len(name) <= 16):
            raise ValueError("name must be between 2 and 16 characters")
        self._name = name
    
    @property
    def category(self):
        return self._category
    
    @category.setter
    def category(self, value):
        if isinstance(value, str):
            if len(value):
                self._category = value
            else:
                ValueError("Category must be longer than 0 characters")
        else:
            TypeError("Category must be a string")
    
    @property
    def articles(self):
        """Return all articles associated with a Magazine"""
        from models.article import Article
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT articles.id, articles.title, articles.content, articles.author_id, articles.magazine_id
            FROM articles
            WHERE articles.magazine_id = ?
        """, (self.id,))
        articles = cursor.fetchall()
        conn.close()
        if articles:
            return [Article(article["id"], article['title'], article['content'], article['author_id'], article['magazine_id']) for article in articles]
        else:
            return []
    
    @property
    def contributors(self):
        """Return all authors associated with a Magazine"""
        from models.author import Author
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT authors.id, authors.name
            FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
        """, (self.id,))
        authors = cursor.fetchall()
        conn.close()
        if authors:
            return [Author(author["id"], author['name']) for author in authors]
        else:
            return []

    def article_titles(self):
        return [article.title for article in self.articles]

    def contributing_authors(self):
        if self.contributors:
            contributing = [contributor for contributor in self.contributors if len([article for article in self.articles if article.author.id == contributor.id]) > 2]
            return contributing
        else:
            return None
    
    def contributing_authors(self):
        """
        Return a list of authors who have written more than 2 articles for the magazine.
        Returns None if no such authors exist.
        """
        if self.contributors:
            major_contributors = [contributor for contributor in self.contributors if len([article for article in self.articles if article.author.id == contributor.id]) > 2]
            if major_contributors:
                return major_contributors
        return None

    def __repr__(self):
        article_titles = ", ".join([article.title for article in self.articles]) if self.articles else "None"
        contributor_titles = ", ".join([contributor.name for contributor in self.contributors]) if self.contributors else "None"
        major_contributor_names = ", ".join([contributor.name for contributor in self.contributing_authors()]) if self.contributing_authors() else "None"
        
        return f'MAGAZINE: {self.name} || ID: {self.id} || ARTICLES: {article_titles} || CONTRIBUTORS: {contributor_titles} || MAJOR CONTRIBUTORS: {major_contributor_names}'
