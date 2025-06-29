import requests
from bs4 import BeautifulSoup

def scrape_website_metadata(url: str) -> dict:
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.title.string.strip() if soup.title else "No title found"
        description_tag = soup.find("meta", attrs={"name": "description"})
        description = description_tag["content"].strip() if description_tag and description_tag.get("content") else "No description found"

        return {
            "url": url,
            "title": title,
            "description": description
        }

    except Exception as e:
        return {
            "error": str(e),
            "url": url
        }
