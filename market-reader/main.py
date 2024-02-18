import requests

import pandas as pd

def stock_tickers()-> pd.DataFrame:
    url = "https://supabase-websocket.dev.marketreader.com/symbols"
    headers = {
        "authority": "supabase-websocket.dev.marketreader.com",
        "accept": "*/*",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "cache-control": "no-cache",
        "origin": "https://app.marketreader.com",
        "pragma": "no-cache",
        "referer": "https://app.marketreader.com/",
        "sec-ch-ua": '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": '"Android"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    return pd.DataFrame(response.json())

def get_stock_data(ticker: str)-> pd.DataFrame:

    url = f"https://supabase-websocket.dev.marketreader.com/outputs/longterm/{ticker.upper()}/5W"
    headers = {
        "authority": "supabase-websocket.dev.marketreader.com",
        "accept": "*/*",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzA4MzM4NTUwLCJzdWIiOiJjYzNhZWQzMC05NDAwLTQxY2MtYjE5OC03MTUzNzMzNTA5YTUiLCJlbWFpbCI6Inlla2VlbnJ5YmFja0BnbWFpbC5jb20iLCJwaG9uZSI6IiIsImFwcF9tZXRhZGF0YSI6eyJwcm92aWRlciI6ImVtYWlsIiwicHJvdmlkZXJzIjpbImVtYWlsIl19LCJ1c2VyX21ldGFkYXRhIjp7fSwicm9sZSI6ImF1dGhlbnRpY2F0ZWQiLCJhYWwiOiJhYWwxIiwiYW1yIjpbeyJtZXRob2QiOiJwYXNzd29yZCIsInRpbWVzdGFtcCI6MTcwODI1MjE1MH1dLCJzZXNzaW9uX2lkIjoiNWRhNmE2ZmQtYTg4NS00MjU5LTgzOTYtZjFkMzI0ZjJmMTkxIn0.6u5kWP3-735SLx2AaQhVo2X3L4YvSBLPsoe8qb3BGUI",
        "cache-control": "no-cache",
        "origin": "https://app.marketreader.com",
        "pragma": "no-cache",
        "referer": "https://app.marketreader.com/",
        "sec-ch-ua": '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": '"Android"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    return pd.DataFrame(response.json())

if __name__ == "__main__":
    tickers = stock_tickers()["symbol"].tolist()
    pd.DataFrame.concat([get_stock_data(ticker) for ticker in tickers]).to_csv("stock_data.csv", index=False)