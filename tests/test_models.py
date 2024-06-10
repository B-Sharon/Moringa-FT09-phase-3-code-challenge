import unittest
from models.author import Author
from models.article import Article
from models.magazine import Magazine

class TestModels(unittest.TestCase):
    def test_author_creation(self):
        author = Author(1, "John Doe")
        self.assertEqual(author.name, "John Doe")
        self.assertEqual(author.id, 1)
    
    def test_author_id_setter(self):
        author = Author(1, "John Doe")
        with self.assertRaises(TypeError):
            author.id = "invalid_id"

    def test_author_name_setter(self):
        with self.assertRaises(TypeError):
            Author(1, 123)
        with self.assertRaises(ValueError):
            Author(1, "")
        author = Author(1, "John Doe")
        with self.assertRaises(AttributeError):
            author.name = "Jane Doe"

    def test_article_creation(self):
        article = Article(1, "Test Title", "Test Content", 1, 1)
        self.assertEqual(article.title, "Test Title")

    def test_article_creation_without_id(self):
        article = Article(None, "New Title", "New Content", 1, 1)
        self.assertIsNotNone(article.id)

    def test_magazine_creation(self):
        magazine = Magazine(1, "Tech Weekly", "Technology")
        self.assertEqual(magazine.name, "Tech Weekly")
        self.assertEqual(magazine.category, "Technology")

    def test_magazine_articles(self):
        
        magazine = Magazine(1, "Tech Weekly", "Technology")
        articles = magazine.articles
        self.assertIsInstance(articles, list)
    
    def test_magazine_contributors(self):
        
        magazine = Magazine(1, "Tech Weekly", "Technology")
        contributors = magazine.contributors
        self.assertIsInstance(contributors, list)
    
    def test_magazine_contributing_authors(self):
        
        magazine = Magazine(1, "Tech Weekly", "Technology")
        major_contributors = magazine.contributing_authors()
        self.assertTrue(
            all(len([article for article in magazine.articles if article.author.id == contributor.id]) > 2 for contributor in major_contributors)
        )

if __name__ == "__main__":
    unittest.main()
