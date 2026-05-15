import requests
from bs4 import BeautifulSoup
import json

BASE_URL = "https://www.shl.com/solutions/products/product-catalog/"


def scrape_catalog():
    response = requests.get(BASE_URL)

    soup = BeautifulSoup(response.text, "html.parser")

    assessments = []

    cards = soup.find_all("a")

    for card in cards:
        href = card.get("href")

        if href and "/products/product-catalog/view/" in href:

            name = card.get_text(strip=True)

            if not name:
                continue

            full_url = "https://www.shl.com" + href

            assessments.append({
                "name": name,
                "url": full_url,
                "description": name,
                "test_type": "Unknown"
            })

    # remove duplicates
    unique = []
    seen = set()

    for item in assessments:
        if item["url"] not in seen:
            unique.append(item)
            seen.add(item["url"])

    with open("catalog.json", "w") as f:
        json.dump(unique, f, indent=4)

    print(f"Saved {len(unique)} assessments")


if __name__ == "__main__":
    scrape_catalog()
