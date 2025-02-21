import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
import re


class Scraper:

    def __init__(self, base_url):

        self.base_url = base_url
        self.scientific_name_pattern = re.compile(
            r"""(?<=Scientific[ ]Name[-][  ])[\w']+([  ]*[\w']*)*""", re.IGNORECASE
        )
        self.combo_pattern = re.compile(
            r"""(?<=\d\.[  ])([\w]+(?!\.)([  ]*(?!\d)[\w]*)*)"""
        )
        self.type_pattern = re.compile(r"[ ]?(\w+)", re.IGNORECASE)

        self.type_plant = ["combo", "clump", "leaf", "plant"]

    def extract_product_name(self, product_text, is_combo):
        """This is to extract Scientific names and name in combos"""
        scientific_name = self.scientific_name_pattern.search(product_text)
        cleaned_scientific_name = (
            "Sanseveria" if scientific_name is None else scientific_name.group()
        )
        cleaned_scientific_name = re.sub(r"[\xa0]+", " ", cleaned_scientific_name)

        # Extract combo names if combo
        list_of_names = []
        if is_combo:
            list_of_names = [
                str(match[0]).title()
                for match in self.combo_pattern.findall(product_text)
            ]

        return cleaned_scientific_name, list_of_names

    def extract_type(self, all_types):
        """This is to extract which type of plant it is
        ["combo", "clump", "leaf", "plant"]"""
        for name in self.type_pattern.findall(all_types):
            if name.lower() in self.type_plant:
                return name.title()
        return "Plant"

    def extract_price(self, product):
        """This is to extract price"""

        price = product.find("span", class_="price")
        return price.text if price else "N/A"

    def cook_soup(self, url):
        try:
            webpage = requests.get(url=url)
            sp = BeautifulSoup(webpage.content, "lxml")
            return sp

        except Exception:
            print("Error occured during GET request.")
            return None

    def scrape_product(self, url, is_combo):
        """In this we scrape each individual product on the page"""

        if sp := self.cook_soup(url):  # walrus operator op in the chat
            for product in sp.find_all("div", class_="desc product-desc"):
                # Extract scientific name and combo names
                cleaned_scientific_name, list_of_names = self.extract_product_name(
                    product.text, is_combo
                )

                # Calculate unit count if combo
                unit = len(list_of_names) if is_combo else 1

                return {
                    "scientific_name": cleaned_scientific_name.strip(),
                    "all_names": list_of_names,
                    "total_units": unit,
                }
        return {}

    def scrape_page(self, page_number):
        """This function creates the main list of dictionaries
        in which we scrape all the data by calling methods"""

        url = f"{self.base_url}?page={page_number}"

        if sp := self.cook_soup(url):

            list_final = []
            ctr = 1

            for product in sp.find_all("div", class_="product-item-v5"):
                # Get the URL of the product
                urls = product.find("a")["href"]
                is_combo = False
                # Get the product name
                names = product.find("h4", class_="title-product")

                if "combo" in names.text.lower():
                    is_combo = True

                names_dict = self.scrape_product(urljoin(url, urls), is_combo)

                # Get the type
                types = self.extract_type(names.text)

                # Get the price
                price = self.extract_price(product)

                list_final.append(
                    {
                        "Product Title": names.text.strip(),
                        "Scientific name": names_dict["scientific_name"],
                        "Type": types,
                        "All_Names": names_dict["all_names"],
                        "Total Units": names_dict["total_units"],
                        "Price": price,
                        "URL": urljoin(url, urls),
                    }
                )

            return list_final

        return

    def dump_to_excel(self, final_list, page_number, writer):
        """Dumping the dictionary into excel"""

        max_names = max([len(item["All_Names"]) for item in final_list])

        # Dynamically create 'Name1', 'Name2', ..., 'NameN' columns
        for i in range(1, max_names + 1):
            for item in final_list:
                item[f"Name{i}"] = (
                    item["All_Names"][i - 1] if i - 1 < len(item["All_Names"]) else "-"
                )

        # Drop 'All Names' column after separating it into individual columns
        for item in final_list:
            del item["All_Names"]
        print(final_list)
        # Convert final_list to DataFrame
        dataframe = pd.DataFrame(final_list)

        # Write to Excel sheet for this page
        sheet_name = f"page-{page_number}"
        dataframe.to_excel(writer, sheet_name=sheet_name, index=False)
        print(f"Data dumped into sheet: {sheet_name}.")


if __name__ == "__main__":

    scraper = Scraper(base_url="https://fermosaplants.com/collections/sansevieria")
    total_pages = 7  # Scrape all 7 pages

    with pd.ExcelWriter("fermosa_data.xlsx") as writer:
        for i in range(1, total_pages + 1):
            print(f"Scraping Page {i}...")
            list_final = scraper.scrape_page(i)
            scraper.dump_to_excel(list_final, i, writer)
