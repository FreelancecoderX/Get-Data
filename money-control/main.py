import logging
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd


class ArticleScraper:
    def __init__(self, base_url: str, start_page: int = 1, end_page: int = 2):
        self.base_url = base_url
        self.start_page = start_page
        self.end_page = end_page
        self.setup_logger()

    def setup_logger(self):
        """
        Set up the logger for the class, including setting the log level and adding a stream handler with a specific formatter.
        """
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def scrape(self):
        """
        Scrape the specified range of pages for articles, parse the content, and save the result to a CSV file.
        """
        all_articles = []
        for i in range(self.start_page, self.end_page):
            page_url = f"{self.base_url}/page-{i}/"
            self.logger.info(f"Scraping URL: {page_url}\n")
            page_content = self.fetch_page(page_url)
            articles = self.parse_articles(page_content)
            self.logger.info(f"Articles: {articles}\n")
            all_articles.extend(articles)

        self.logger.info(f"All articles saved from articles: {all_articles}\n")
        self.save_to_csv(all_articles)

    def fetch_page(self, url: str) -> BeautifulSoup:
        """
        Fetches a web page using the given URL and returns a BeautifulSoup object representing the parsed HTML content.

        Args:
            url (str): The URL of the web page to fetch.

        Returns:
            BeautifulSoup: A BeautifulSoup object representing the parsed HTML content of the fetched web page.
        """
        response = requests.get(url)
        response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
        return BeautifulSoup(response.content, "html.parser")

    def parse_articles(self, soup: BeautifulSoup) -> list:
        """
        Parses the articles from the BeautifulSoup object and returns a list of article dictionaries containing title, link, date, and summary.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object containing the parsed HTML.

        Returns:
            list: A list of article dictionaries, each containing title, link, date, and summary.
        """
        news_items = soup.find_all("li", class_="clearfix")
        self.logger.info(f"Found {len(news_items)} news items.\n")
        articles = []
        for news_item in news_items:
            summary_elem = news_item.find("p")
            summary = summary_elem.text.strip() if summary_elem else None

            date_elem = news_item.find("span", class_="date")
            date = date_elem.text.strip() if date_elem else None

            a_tag = news_item.find("a", href=True)
            link = a_tag['href'].strip() if a_tag else None
            title = a_tag.text.strip() if a_tag else None

            if not all([title, link, date, summary]):
                self.logger.warning(f"Missing information for news item: {news_item}\n")
                continue

            article = {"title": title, "link": link, "date": date, "summary": summary}
            articles.append(article)

        if not articles:
            self.logger.error("No articles were parsed. Check if the website structure has changed.")
        else:
            self.logger.info(f"Parsed {len(articles)} articles.\n")

        return articles

    def save_to_csv(self, articles):
        """
        Save the given articles to a CSV file.

        Args:
            self: The object itself.
            articles: A list of articles to be saved to the CSV file.

        Returns:
            None
        """
        df = pd.DataFrame(articles)
        date_str = datetime.now().strftime("%Y-%m-%d")
        path = f"data/money_control_data_{date_str}.csv"
        df.to_csv(path, index=False)
        self.logger.info(f"Data saved to {path}\n")


if __name__ == "__main__":
    scraper = ArticleScraper(
        base_url="https://www.moneycontrol.com/news/business/stocks",
        start_page=29,
        # end_page=31,
    )
    scraper.scrape()
