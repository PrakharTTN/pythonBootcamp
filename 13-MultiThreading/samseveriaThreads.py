import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
import re
import time
from concurrent.futures import ThreadPoolExecutor

# Regular expressions for extracting information
SCIENTIFIC_NAME_PATTERN = re.compile(
    r"(?<=Scientific Name[-][  ])[\w']+([  ]*[\w']*)*", re.IGNORECASE
)
COMBO_PATTERN = re.compile(r"(?<=\d\.[  ])([\w]+(?!\.)([  ]*(?!\d)[\w]*)*)")
TYPE_PATTERN = re.compile(r"[ ]?(\w+)", re.IGNORECASE)
ALL_PLANTS = ["combo", "clump", "leaf", "plant"]


class Scraper:
    def __init__(self, base_url):
        self.base_url = base_url

    def cook_soup(self, url):
        """Fetches and parses HTML using BeautifulSoup."""

        try:
            response = requests.get(url)
            response.raise_for_status()
            return BeautifulSoup(response.content, "lxml")
        except requests.RequestException as e:
            print(f"⚠️ Request failed for {url}: {e}")
            return None

    def extract_product_name(self, product_text, is_combo):
        """Extracts the scientific name and list of combo names (if applicable)."""

        scientific_name = SCIENTIFIC_NAME_PATTERN.search(product_text)
        cleaned_name = (
            "Sanseveria" if not scientific_name else scientific_name.group().strip()
        )

        list_of_names = (
            [match[0].title() for match in COMBO_PATTERN.findall(product_text)]
            if is_combo
            else []
        )

        return cleaned_name, list_of_names

    def extract_type(self, all_types):
        """Determines if the product is a combo or a plant."""

        for name in TYPE_PATTERN.findall(all_types):
            if name.lower() in ALL_PLANTS:
                return name.title()
        return "Plant"

    def extract_price(self, product):
        """Extracts the price of the product."""

        price_tag = product.find("span", class_="price")
        return price_tag.text.strip() if price_tag else "N/A"

    def scrape_product(self, url, is_combo):
        """Scrapes product details from an individual product page."""

        soup = self.cook_soup(url)
        if soup:
            product_info = soup.find("div", class_="desc product-desc")
            if product_info:
                name, all_names = self.extract_product_name(product_info.text, is_combo)
                return {
                    "scientific_name": name,
                    "all_names": all_names,
                    "total_units": len(all_names) if is_combo else 1,
                }
        return {}

    def scrape_page(self, page_number):
        """Scrapes all products from a given page."""
        print(f"Currently Scraping Page {page_number}")
        url = f"{self.base_url}?page={page_number}"
        soup = self.cook_soup(url)

        if not soup:
            return []

        page_results = []
        for product in soup.find_all("div", class_="product-item-v5"):
            product_url = urljoin(url, product.find("a")["href"])
            product_title = product.find("h4", class_="title-product").text.strip()
            is_combo = "combo" in product_title.lower()
            product_type = self.extract_type(product_title)
            price = self.extract_price(product)

            product_info = self.scrape_product(product_url, is_combo)

            page_results.append(
                {
                    "Product Title": product_title,
                    "Scientific Name": product_info.get("scientific_name", "N/A"),
                    "Type": product_type,
                    "Total Units": product_info.get("total_units", 1),
                    "All Names": product_info.get(
                        "all_names", []
                    ),  # Store list of names
                    "Price": price,
                    "URL": product_url,
                }
            )

        return page_results

    def dump_to_excel(self, all_data):
        """Writes scraped data to an Excel file with separate sheets per page."""

        with pd.ExcelWriter("Fermosa_extact.xlsx") as writer:
            for page_number, page_data in all_data.items():
                # Find max combo names count to create separate columns
                max_names = (
                    max(len(item["All Names"]) for item in page_data)
                    if page_data
                    else 0
                )

                # Create new columns for each combo name
                for i in range(1, max_names + 1):
                    for item in page_data:
                        item[f"Name{i}"] = (
                            item["All Names"][i - 1]
                            if i - 1 < len(item["All Names"])
                            else "-"
                        )

                # Remove original list column before saving
                for item in page_data:
                    del item["All Names"]

                df = pd.DataFrame(page_data)
                df.to_excel(writer, sheet_name=f"page-{page_number}", index=False)
                print(f"Data saved to sheet: page-{page_number}")


if __name__ == "__main__":

    scraper = Scraper(base_url="https://fermosaplants.com/collections/sansevieria")
    total_pages = 7

    print("Starting threads scraping")

    # Store results in a dictionary for each page
    all_scraped_data = {}
    start = time.time()

    with ThreadPoolExecutor(max_workers=7) as executor:
        results = executor.map(scraper.scrape_page, range(1, total_pages + 1))
    end = time.time()

    # Store the data with respective page numbers
    for page_number, page_data in enumerate(results, start=1):
        all_scraped_data[page_number] = page_data

    # Write to Excel with separate sheets
    if all_scraped_data:
        scraper.dump_to_excel(all_scraped_data)
        print("Scraping complete. Data saved.")
    else:
        print("Problem in scraping.")
    print(end - start, " seconds taken.")
