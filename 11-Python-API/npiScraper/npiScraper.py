'''Learn about National Provider Identifier (NPI) https://en.wikipedia.org/wiki/National_Provider_Identifier On the portal https://npiregistry.cms.hhs.gov/search, one can search for details associated with an NPI. For example, use 1114473527 for the 'NPI Number' input field and click on the "Search" button The task in this assignment is to create a Python API to fetch details corresponding to an NPI as JSON. On the search result page, details are displayed as a table with a column name, and its value should form a JSON key-value pair. If a column has a subfield field, for example, Taxonomy, then create a nested JSON object on the result page.'''
import requests
import concurrent.futures
import json
from npi_ids import all_npi_ids

url = "https://npiregistry.cms.hhs.gov/RegistryBack/npiDetails"

npi_ids = [i for i in all_npi_ids if i.isdigit() and len(i) == 10]
print(npi_ids)


def send_post_request(npi_id):
    '''This function sends a get request to api with single npi_id'''
    payload = {"number": npi_id}
    response = requests.post(url, json=payload)

    if response.status_code == 200:
        return response.json()
    else:
        return {
            "error": f"Failed for NPI {npi_id}",
            "status_code": response.status_code,
        }

#used threads to execute requests faster
with concurrent.futures.ThreadPoolExecutor(max_workers=25) as executor:
    results = list(executor.map(send_post_request, npi_ids))
    
#dumped the list into json file
with open("scraped.json", "w") as my_file:
    json.dump(results, my_file, indent=4)

print("All IDs Scraped. ")
