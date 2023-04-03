import requests
from bs4 import BeautifulSoup
import csv
import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True)
    url = Column(String)
    headline = Column(String)
    author = Column(String)
    date = Column(DateTime)

    def __init__(self, url, headline, author, date):
        self.url = url
        self.headline = headline
        self.author = author
        self.date = date

    def __repr__(self):
        return f"Article('{self.url}', '{self.headline}', '{self.author}', '{self.date}')"


class VergeScraper:
    def __init__(self, db_filename):
        self.url = "https://www.theverge.com"
        self.articles = []
        self.engine = create_engine(f'sqlite:///{db_filename}')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def scrape_articles(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, "html.parser")
        article_boxes = soup.find_all("div", class_="c-entry-box--compact__body")

        for i, box in enumerate(article_boxes):
            headline = box.find("h2", class_="c-entry-box--compact__title").text.strip()
            url = box.find("a", class_="c-entry-box--compact__image-wrapper")["href"]
            byline = box.find("div", class_="c-byline").text.strip()
            author, date = byline.split("•")
            author = author.strip()
            date = datetime.datetime.strptime(date.strip(), '%B %d, %Y')
            article = Article(url, headline, author, date)
            self.articles.append(article)

    def save_csv(self, filename):
        with open(filename, "w", newline="") as csvfile:
            fieldnames = ["id", "URL", "headline", "author", "date"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for i, article in enumerate(self.articles):
                writer.writerow({"id": i, "URL": article.url, "headline": article.headline, "author": article.author, "date": article.date})

    def save_articles_to_database(self):
        for i, article in enumerate(self.articles):
            self.session.add(article)
        self.session.commit()

    def get_articles_from_database(self):
        return self.session.query(Article).all()
