import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd


def xlsx_dump(list_final):
    with pd.ExcelWriter("ScrapedData.xlsx") as writer:
        for i in range(1, 8):
            dataframe = pd.DataFrame(list_final[i - 1])
            dataframe.to_excel(writer, sheet_name=f"page {i}")


def main():
    # For page number (For now provided 1, can input from user)
    number = 7
    final_list = []
    for i in range(1, 8):
        url = f"https://fermosaplants.com/collections/sansevieria?page={i}"

        # Send request to the URL
        webpage = requests.get(url=url)
        sp = BeautifulSoup(webpage.content, "html.parser")

        sub_list = []
        type_plant = ["combo", "clump", "leaf", "plant"]

        # Loop through all product items
        for product in sp.find_all("div", class_="product-item-v5"):
            # Get the URL of the product
            urls = product.find("a")["href"]

            # Get the product name
            names = product.find("h4", class_="title-product")

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

            sub_list.append(
                {
                    "Name": names.text.strip(),
                    "Type": types,
                    "Total Units": unit,
                    "Price": price.text,
                    "URL": urljoin(url, urls),
                }
            )

        final_list.append(sub_list)
    print(final_list)
    xlsx_dump(final_list)
    print("Successfully Scraped Data and dumped into xlsx file.")


if __name__ == "__main__":
    main()
