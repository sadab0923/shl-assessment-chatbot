import json
import requests
from bs4 import BeautifulSoup


BASE_URL = "https://www.shl.com/solutions/products/product-catalog/"


def get_catalog_page():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(BASE_URL, headers=headers)

    if response.status_code != 200:
        print("Failed to fetch catalog")
        return None

    return response.text


def extract_assessments(html):

    soup = BeautifulSoup(html, "html.parser")

    links = soup.find_all("a")

    assessments = []
    visited_urls = set()

    for link in links:

        href = link.get("href")

        if not href:
            continue

        if "/products/product-catalog/view/" not in href:
            continue

        name = link.get_text(strip=True)

        if not name:
            continue

        full_url = "https://www.shl.com" + href

        # skip duplicate entries
        if full_url in visited_urls:
            continue

        visited_urls.add(full_url)

        assessments.append({
            "name": name,
            "url": full_url,
            "description": name,
            "test_type": "Unknown"
        })

    return assessments


def save_catalog(data):

    with open("catalog.json", "w") as file:
        json.dump(data, file, indent=4)

    print(f"Saved {len(data)} assessments")


def main():

    html = get_catalog_page()

    if not html:
        return

    assessments = extract_assessments(html)

    save_catalog(assessments)


if __name__ == "__main__":
    main()
