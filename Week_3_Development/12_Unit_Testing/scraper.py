import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
import re

# Compiled all the regex without the class, basically these are constants
SCIENTIFIC_NAME_PATTERN = re.compile(
    r"""(?<=Scientific[ ]Name[-][  ])[\w']+([  ]*[\w']*)*""", re.IGNORECASE
)
COMBO_PATTERN = re.compile(r"""(?<=\d\.[  ])([\w]+(?!\.)([  ]*(?!\d)[\w]*)*)""")
TYPE_PATTERN = re.compile(r"[ ]?(\w+)", re.IGNORECASE)

ALL_PLANTS = ["combo", "clump", "leaf", "plant"]


class Scraper:

    def __init__(self, base_url):
        self.base_url = base_url

    def extract_product_name(self, product_text, is_combo):
        scientific_name = SCIENTIFIC_NAME_PATTERN.search(product_text)
        cleaned_scientific_name = (
            "Sanseveria" if scientific_name is None else scientific_name.group()
        )
        cleaned_scientific_name = re.sub(r"[ ]+", " ", cleaned_scientific_name)

        list_of_names = []
        if is_combo:
            list_of_names = [
                str(match[0]).title() for match in COMBO_PATTERN.findall(product_text)
            ]

        return cleaned_scientific_name, list_of_names

    def extract_type(self, all_types):
        for name in TYPE_PATTERN.findall(all_types):
            if name.lower() in ALL_PLANTS:
                return name.title()
        return "Plant"

    def extract_price(self, product):
        price = product.find("span", class_="price")
        return price.text if price else "N/A"

    def cook_soup(self, url):
        try:
            webpage = requests.get(url=url)
            webpage.raise_for_status()
            return BeautifulSoup(webpage.content, "lxml")
        except requests.RequestException as e:
            print(f"Error occurred during GET request: {e}")
            return None

    def scrape_product(self, url, is_combo):

        if sp := self.cook_soup(url):
            for product in sp.find_all("div", class_="desc product-desc"):
                cleaned_scientific_name, list_of_names = self.extract_product_name(
                    product.text, is_combo
                )
                unit = len(list_of_names) if is_combo else 1
                return {
                    "scientific_name": cleaned_scientific_name.strip(),
                    "all_names": list_of_names,
                    "total_units": unit,
                }
        return {"Product": "Empty"}

    def scrape_page(self, page_number):
        url = f"{self.base_url}?page={page_number}"
        if sp := self.cook_soup(url):

            list_final = []
            for product in sp.find_all("div", class_="product-item-v5"):
                urls = product.find("a")["href"]
                is_combo = (
                    "combo" in product.find("h4", class_="title-product").text.lower()
                )
                names_dict = self.scrape_product(urljoin(url, urls), is_combo)
                types = self.extract_type(
                    product.find("h4", class_="title-product").text
                )
                price = self.extract_price(product)

                list_final.append(
                    {
                        "Product Title": product.find(
                            "h4", class_="title-product"
                        ).text.strip(),
                        "Scientific name": names_dict.get("scientific_name", "N/A"),
                        "Type": types,
                        "All_Names": names_dict.get("all_names", []),
                        "Total Units": names_dict.get("total_units", 1),
                        "Price": price,
                        "URL": urljoin(url, urls),
                    }
                )
            return list_final
        return [{f"Page{page_number}": "Empty"}]

    def dump_to_excel(self, final_list, page_number, writer):
        max_names = max((len(item["All_Names"]) for item in final_list), default=0)

        for i in range(1, max_names + 1):
            for item in final_list:
                item[f"Name{i}"] = (
                    item["All_Names"][i - 1] if i - 1 < len(item["All_Names"]) else "-"
                )

        for item in final_list:
            del item["All_Names"]

        dataframe = pd.DataFrame(final_list)
        sheet_name = f"page-{page_number}"
        dataframe.to_excel(writer, sheet_name=sheet_name, index=False)
        print(f"Data dumped into sheet: {sheet_name}.")


if __name__ == "__main__":

    scraper = Scraper(base_url="https://fermosaplants.com/collections/sansevieria")
    total_pages = 7

    with pd.ExcelWriter("fermosa_data.xlsx") as writer:
        for i in range(1, total_pages + 1):
            print(f"Scraping Page {i}...")
            list_final = scraper.scrape_page(i)
            if list_final:
                scraper.dump_to_excel(list_final, i, writer)
