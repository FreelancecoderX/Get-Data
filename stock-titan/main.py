import asyncio
import aiohttp
import re
from datetime import date, datetime, timedelta
import pandas as pd
from bs4 import BeautifulSoup
import nest_asyncio

nest_asyncio.apply()

BASE_URL = "https://www.stocktitan.net"


async def fetch(url, session):
    async with session.get(url) as response:
        return await response.text()


async def process_article(article_url, session, data):
    html = await fetch(article_url, session)
    soup = BeautifulSoup(html, "html.parser")
    article = soup.find("div", class_="article")
    title = soup.find("h1")
    datetime = soup.find("time")
    impact_bar_container = soup.find("div", class_="impact-bar-container")
    impact = (
        impact_bar_container.find("span", class_="rhea-score")
        if impact_bar_container is not None
        else None
    )
    sentiment_bar_container = soup.find("div", class_="sentiment-bar-container")
    sentiment = (
        sentiment_bar_container.find("span", class_="rhea-score")
        if sentiment_bar_container is not None
        else None
    )
    news_card_summary = soup.find("div", class_="news-card-summary")
    summary = (
        news_card_summary.find("div", id="summary")
        if news_card_summary is not None
        else None
    )

    result = {
        "title": title.text.strip() if title is not None else "",
        "datetime": datetime.get("datetime") if datetime is not None else "",
        "impact_score": impact.text.strip().split("(")[-1].split(")")[0]
        if impact is not None
        else "",
        "sentiment": sentiment.text.strip().split("(")[-1].split(")")[0]
        if sentiment is not None
        else "",
        "summary": summary.get_text().strip() if summary is not None else "",
        "article": re.sub("\s+", " ", article.get_text()).strip()
        if article is not None
        else "",
    }

    data.append(result)


async def process_date(date_str, session, data):
    url = f"https://www.stocktitan.net/news/{date_str}/"
    html = await fetch(url, session)
    soup = BeautifulSoup(html, "html.parser")
    news_rows = soup.find_all("div", class_="news-row")
    all_links = [
        BASE_URL + row.find("a", class_="feed-link").get("href") for row in news_rows
    ]
    tasks = []
    for article_url in all_links:
        tasks.append(process_article(article_url, session, data))
    await asyncio.gather(*tasks)


async def main():
    async with aiohttp.ClientSession() as session:
        data = []
        loop = asyncio.get_event_loop()
        tasks = [
            loop.create_task(
                process_date(
                    str(date.fromisoformat(str(date.today())) - timedelta(days=i)),
                    session,
                    data,
                )
            )
            for i in range(4)
        ]
        await asyncio.gather(*tasks)

        df = pd.DataFrame(data)
        date_str = datetime.now().strftime("%Y-%m-%d")
        path = f"stocktitan_{date_str}.csv"
        df.to_csv(path, index=False)


if __name__ == "__main__":
    asyncio.run(main())
