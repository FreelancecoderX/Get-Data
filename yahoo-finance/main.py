from playwright.sync_api import sync_playwright

url = "https://finance.yahoo.com/topic/stock-market-news/?guccounter=1"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(url)
    print(page.title())