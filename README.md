# webscrapper

This code is a Python script that scrapes the website "The Verge" (used as example in this script) for its latest articles, and stores them either in a SQLite database or a CSV file.




The script defines a class called Article which inherits from declarative_base(), a class from the SQLAlchemy library. Article represents a single news article and has attributes for id, url, headline, author, and date.




The VergeScraper class contains methods for scraping articles from the website, saving them to a CSV file, and saving them to a SQLite database. It has a constructor that initializes instance variables for the Verge URL, the list of articles to be scraped, and a database engine.


The scrape_articles() method sends a GET request to the Verge URL and parses the HTML content using BeautifulSoup. It then extracts the relevant information from each article, creates an Article object with that information, and appends it to the self.articles list.



The save_csv() method saves the articles in self.articles to a CSV file with a specified filename. It writes each article's id, URL, headline, author, and date to a new row in the file using the csv.DictWriter class.



The save_articles_to_database() method saves the articles in self.articles to a SQLite database using SQLAlchemy's session object. It creates a new session and adds each article to the session, and then commits the session to the database.


The get_articles_from_database() method retrieves all articles from the SQLite database and returns them as a list of Article objects.


To use the VergeScraper class, a user can create an instance of the class, passing in the filename of the database they wish to use. They can then call the scrape_articles() method to retrieve the latest articles from the Verge website, the save_csv() method to save the articles to a CSV file, and the save_articles_to_database() method to save the articles to a SQLite database. Users can also call the get_articles_from_database() method to retrieve articles from the database they saved.
