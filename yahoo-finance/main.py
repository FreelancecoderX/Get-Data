from config import logger

from datetime import datetime

from bs4 import BeautifulSoup
import pandas as pd
import requests


class NewsScraper:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_page(self, url: str) -> BeautifulSoup:
        """
        Get the webpage content from the specified URL and return it as a BeautifulSoup object.

        Args:
            url (str): The URL of the webpage to download.

        Returns:
            BeautifulSoup: The parsed HTML content of the webpage.
        """
        logger.info(f"Downloading webpage: {url}\n")
        response = requests.get(url)

        if not response.ok:
            logger.error(
                f"Failed to load {url} with status code {response.status_code}\n"
            )
            raise Exception(
                f"Failed to load {url} with status code {response.status_code}\n"
            )

        soup = BeautifulSoup(response.text, "html.parser")
        return soup

    def get_news_tags(self, soup: BeautifulSoup) -> list:
        """
        Get news tags from the BeautifulSoup object.

        Args:
            soup (BeautifulSoup): The BeautifulSoup object containing the parsed HTML.

        Returns:
            list: A list of news tags extracted from the page.
        """
        logger.info("Extracting news tags from page\n")

        return soup.find_all("div", {"class": "Ov(h) Pend(44px) Pstart(25px)"})

    def parse_news(self, div_tag) -> dict:
        """
        Parse news from a div tag and return a dictionary containing the source, title, URL, and content.

        Parameters:
            div_tag: The div tag containing the news information.

        Returns:
            A dictionary with the keys "source", "title", "url", and "content" containing the parsed news information.
        """
        logger.info("Parsing news from a div tag\n")

        source = div_tag.find("div").text
        title = div_tag.find("a").text
        url = self.base_url + div_tag.find("a")["href"]
        content = div_tag.find("p").text

        return {"source": source, "title": title, "url": url, "content": content}

    def scrape_news(self, path: str = None) -> pd.DataFrame:
        """
        Scrapes news data from a website and saves it to a CSV file. If no path is provided, a default filename based on the current date is used. Returns a pandas DataFrame containing the scraped news data.

        Parameters:
            path (str, optional): The path to save the CSV file. Defaults to None.

        Returns:
            pandas.DataFrame: The DataFrame containing the scraped news data.
        """
        if path is None:
            date = datetime.now().strftime("%Y-%m-%d")
            path = f"stock_market_news_{date}.csv"

        full_url = self.base_url + "/topic/stock-market-news/"

        logger.info(f"Starting news scraping for URL: {full_url}\n")

        doc = self.get_page(url=full_url)
        div_tags = self.get_news_tags(soup=doc)

        news = [self.parse_news(div) for div in div_tags]

        df = pd.DataFrame(news)
        df.to_csv(path, index=False)

        logger.info(f"News data saved to {path}\n")

        return df


if __name__ == "__main__":
    scraper = NewsScraper(base_url="https://finance.yahoo.com")
    news_df = scraper.scrape_news()
