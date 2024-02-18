from config import logger

from datetime import datetime
from glob import glob
import re

from bs4 import BeautifulSoup
import pandas as pd
import requests


class ArticleScraper:
    def __init__(self, base_path="yahoo-finance/*.csv"):
        self.base_path = base_path

    def scrape_articles(self) -> pd.DataFrame:
        """
        Scrape articles from the base path and update the dataframe with the articles.

        Parameters:
        - self: the class instance

        Return:
        - df: the dataframe with articles
        """
        # read in data from path
        path = glob(self.base_path)
        if not path:
            logger.error("No CSV files found in the path.\n")
            return

        df = pd.read_csv(path[0])
        logger.info("CSV file loaded successfully.\n")

        # Update dataframe with articles
        df["article"] = df["url"].apply(self.get_article)
        return df

    def get_article(self, url: str) -> str:
        """
        Retrieves the content of an article from the specified URL.

        Parameters:
        url (str): The URL of the article.

        Returns:
        str: The content of the article.
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            logger.info(f"Article retrieved successfully from {url}\n")
        except requests.RequestException as e:
            logger.error(f"Request failed: {e}\n")
            return ""

        soup = BeautifulSoup(response.text, "html.parser")
        div_tag = soup.find("div", {"class": "caas-body"})
        if div_tag:
            article = div_tag.get_text().strip()
            article = re.sub(r"\s+", " ", article)
            return article
        else:
            logger.warning(f"No article content found for URL: {url}\n")
            return ""


if __name__ == "__main__":
    scraper = ArticleScraper()
    articles_df = scraper.scrape_articles()
    date = datetime.now().strftime("%Y-%m-%d")
    if articles_df is not None:
        articles_df.to_csv(f"data/scraped_articles_{date}.csv", index=False)
        logger.info("Scraped articles saved to scraped_articles.csv\n")
