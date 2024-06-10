from database.connection import get_db_connection

class Author:
    def __init__(self, id, name):
        self._id = id
        self.name = name
    
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
            raise TypeError("Name must be of type str")
        if len(name) == 0:
            raise ValueError("Name must be longer than zero characters")
        if hasattr(self, '_name'):
            raise AttributeError("Name cannot be changed once given")
        self._name = name
    
    @property
    def articles(self):
        """Return all articles associated with an author"""
        from models.article import Article
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT articles.id, articles.title, articles.content, articles.author_id, articles.magazine_id
            FROM articles
            WHERE articles.author_id = ?
            """, (self.id,))
        articles = cursor.fetchall()
        conn.close()
        if articles:
            return [Article(article["id"], article['title'], article['content'], article['author_id'], article['magazine_id']) for article in articles]
        else:
            return []
    
    @property
    def magazines(self):
        """Return all magazines associated with an author"""
        from models.magazine import Magazine
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT magazines.id, magazines.name, magazines.category
            FROM magazines
            JOIN articles ON magazines.id = articles.magazine_id
            WHERE articles.author_id = ?
            """, (self.id,))
        magazines = cursor.fetchall()
        conn.close()
        if magazines:
            return [Magazine(magazine["id"], magazine['name'], magazine['category']) for magazine in magazines]
        else:
            return []

    def __repr__(self):
        article_titles = ", ".join([article.title for article in self.articles]) if self.articles else "No articles"
        magazine_titles = ", ".join([magazine.name for magazine in self.magazines]) if self.magazines else "No magazines"
        return f'AUTHOR: {self.name} || id: {self.id} || ARTICLES: {article_titles} || MAGAZINES: {magazine_titles} '
