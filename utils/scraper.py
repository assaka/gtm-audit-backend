# file: utils/scraper.py
import requests
import trafilatura
import json


# List of URLs to scrape
urls = [
    "https://www.simoahava.com/analytics/variable-guide-google-tag-manager/",
    "https://www.simoahava.com/analytics/what-are-tags/",
    "https://www.simoahava.com/analytics/trigger-guide-google-tag-manager/"
]



# Custom headers to simulate a browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/90.0.4430.212 Safari/537.36"
}

def fetch_articles():
    texts = []

    for url in urls:
        print(f"🔍 Fetching: {url}")
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                downloaded = response.text
                text = trafilatura.extract(downloaded)
                if text:
                    print(f"✅ Content extracted from: {url}")
                    texts.append({"url": url, "content": text})
                else:
                    print(f"⚠️ No content extracted from: {url}")
            else:
                print(f"❌ HTTP Error {response.status_code} for {url}")
        except Exception as e:
            print(f"❌ Error fetching {url}: {e}")

    return texts

def save_articles(texts, filename="gtm_articles.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(texts, f, ensure_ascii=False, indent=2)
    print(f"\n✅ {len(texts)} articles saved to {filename}")

if __name__ == "__main__":
    articles = fetch_articles()
    save_articles(articles)

import os

if os.path.exists("gtm_articles.json"):
    print("🎉 File saved successfully: gtm_articles.json")
else:
    print("❌ File was not saved. Please check your path or write permissions.")
