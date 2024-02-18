from datetime import datetime
import logging

from bs4 import BeautifulSoup
import pandas as pd
import requests

#  Set up logging with stream handler and INFO level
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

class NewsScraper:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_page(self, url: str) -> BeautifulSoup:
        """Download webpage and parse with BeautifulSoup"""
        logger.info(f"Downloading webpage: {url}\n")
        response = requests.get(url)

        if not response.ok:
            logger.error(f"Failed to load {url} with status code {response.status_code}\n")
            raise Exception(f"Failed to load {url} with status code {response.status_code}\n")

        soup = BeautifulSoup(response.text, "html.parser")
        return soup

    def get_news_tags(self, soup: BeautifulSoup) -> list:
        """Get all news tags from the page"""
        logger.info("Extracting news tags from page\n")

        return soup.find_all("div", {"class": "Ov(h) Pend(44px) Pstart(25px)"})

    def parse_news(self, div_tag) -> dict:
        """Parse news tags and return news object"""
        logger.info("Parsing news from a div tag\n")

        source = div_tag.find("div").text
        title = div_tag.find("a").text
        url = self.base_url + div_tag.find("a")["href"]
        content = div_tag.find("p").text

        return {"source": source, "title": title, "url": url, "content": content}

    def scrape_news(self, path: str = None) -> pd.DataFrame:
        """Scrape news from base_url and return dataframe"""
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

