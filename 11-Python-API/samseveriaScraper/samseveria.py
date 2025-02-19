import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd


# For page number (For now provided 1, can input from user)
number = 1
url = f"https://fermosaplants.com/collections/sansevieria?page={number}"

# Send request to the URL
webpage = requests.get(url=url)
sp = BeautifulSoup(webpage.content, "html.parser")

listfinal = []
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

    listfinal.append(
        {
            "Name": names.text.strip(),
            "Type": types,
            "Total Units": unit,
            "Price": price.text,
            "URL": urljoin(url, urls),
        }
    )

dataframe = pd.DataFrame(listfinal)
dataframe.to_excel(f"scraped_data_page{number}.xlsx")

print("Successfully Scraped Data and dumped into xlsx file.")
