import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
import re


def xlsx_dump(final_list, number):
    # Handle dynamic "Name1", "Name2", ... columns for the 'All Names' field
    # We will create 'Name1', 'Name2', ..., 'Name10' columns for 'All Names' values

    # Find the maximum number of names for the dynamic columns
    max_names = max([len(item["All_Names"]) for item in final_list], default=0)

    # Dynamically create 'Name1', 'Name2', ..., 'NameN' columns
    for i in range(1, max_names + 1):
        for item in final_list:
            # Ensure we only access "All_Names" if the index exists
            item[f"Name{i}"] = (
                item["All_Names"][i - 1] if i - 1 < len(item["All_Names"]) else None
            )
    # Drop 'All Names' column after separating it into individual columns
    for item in final_list:
        del item["All_Names"]

    # Convert final_list to DataFrame
    dataframe = pd.DataFrame(final_list)

    # Write to Excel file
    dataframe.to_excel(f"scraped_data_page{number}.xlsx", index=False)
    print(f"Successfully Scraped Data and dumped into xlsx file for page {number}.")


# def xlsx_dump(final_list, number):

#     dataframe = pd.DataFrame(final_list)

#     dataframe.to_excel(f"scraped_data_page{number}.xlsx")

#     print("Successfully Scraped Data and dumped into xlsx file.")


def url_scrape(url, is_combo, ctr):

    webpage = requests.get(url=url)
    sp = BeautifulSoup(webpage.content, "lxml")

    for product in sp.find_all("div", class_="desc product-desc"):

        scientifc_name_pattern = re.compile(
            r"""(?<=Scientific[ ]Name[-][  ])[\w']+([  ]*[\w']*)*""", re.IGNORECASE
        )
        scientific_name = scientifc_name_pattern.search(product.text)

        if scientific_name is None:
            scientific_name = "Sanseveria"
        else:
            scientific_name = scientific_name.group()
        cleaned_scientifc_name = scientific_name

        cleaned_scientifc_name = re.sub(r"[\xa0]+", " ", scientific_name)
        unit = 1

        list_of_names = []
        # Get the product name
        if is_combo:
            combo_pattern = re.compile(
                r"""(?<=\d\.[  ])([\w]+(?!\.)([  ]*(?!\d)[\w]*)*)"""
            )
            # combo_pattern = re.compile(r"(?<=\d\.)([A-Za-z\s]+)(?=,|\n|$)")

            # cleaned_combo_names = re.sub(r"[\xa0]+", " ", product.text)
            list_of_names = [match[0] for match in combo_pattern.findall(product.text)]
            unit = len(list_of_names)
        print(f"Combo No. {ctr}\n\n")
        dict = {
            "scientific_name": cleaned_scientifc_name.strip(),
            "all_names": list_of_names,
            "total_units": unit,
        }
        print(dict, "\n")
        return dict


def main():
    # For page number (For now provided 1, can input from user)
    for i in range(1, 2):
        number = i
        url = f"https://fermosaplants.com/collections/sansevieria?page={number}"

        # Send request to the URL
        webpage = requests.get(url=url)
        sp = BeautifulSoup(webpage.content, "html.parser")

        list_final = []
        type_plant = ["combo", "clump", "leaf", "plant"]

        ctr = 1
        # Loop through all product items
        for product in sp.find_all("div", class_="product-item-v5"):
            # Get the URL of the product
            urls = product.find("a")["href"]
            is_combo = False
            # Get the product name
            names = product.find("h4", class_="title-product")

            print(names.text, "\n\n")

            if "combo" in names.text.lower():
                is_combo = True

            names_dict = url_scrape(urljoin(url, urls), is_combo, ctr)
            ctr += 1
            list_of_names = names.text.lower().replace("(", "").replace(")", "").split()

            # Get the type
            types = "Plant"
            for i in list_of_names:
                if i in type_plant:
                    types = i
                    break

            # Get units if combo
            unit = 1
            for i in list_of_names:
                if i.isdigit():
                    unit = i
                    break

            # Get the price
            price = product.find("span", class_="price")

            list_final.append(
                {
                    "Product Title": names.text.strip(),
                    "Scientific name": names_dict["scientific_name"],
                    "Type": types,
                    "All_Names": names_dict["all_names"],
                    "Total Units": names_dict["total_units"],
                    "Price": price.text,
                    "URL": urljoin(url, urls),
                }
            )
    print(list_final)
    xlsx_dump(list_final, number)


if __name__ == "__main__":
    main()
