

# FermosaScraper

**FermosaScraper** is a Python-based web scraper designed to collect product details from the Fermosa Plants website. The script extracts plant-related data such as scientific names, plant types, prices, and combo details, and exports the data to an Excel file. The script also uses multithreading to speed up the scraping process across multiple pages.

## Features

- **Multithreaded Scraping**: Scrapes data concurrently from multiple pages using Python's `ThreadPoolExecutor`.
- **Extracts Scientific Names**: Scrapes scientific names of plants listed on the website.
- **Supports Combo Products**: Identifies combo products and extracts individual plant names.
- **Extracts Product Type**: Automatically detects the product type (e.g., Combo, Clump, Leaf, Plant).
- **Price Extraction**: Extracts the price of each product.
- **Exports to Excel**: Saves all scraped data into an Excel file, with separate sheets for each page.
- **Regex-based Extraction**: Utilizes regular expressions for clean and reliable extraction of scientific names, combo names, and plant types.

## Requirements

- Python 3.x
- `requests` (for sending HTTP requests)
- `beautifulsoup4` (for parsing HTML)
- `pandas` (for working with data and exporting to Excel)
- `openpyxl` (for Excel writing support)

Install the required dependencies by running:

```bash
pip install requests beautifulsoup4 pandas openpyxl
```

## Usage

To run the script, simply execute the following command:

```bash
python fermosa_scraper.py
```

### Optional Configuration

- **base_url**: Set the `base_url` to the starting URL for the website you want to scrape.
- **total_pages**: Adjust the `total_pages` variable to specify how many pages you want to scrape (default is 7).

## How it works

1. The script starts by sending requests to each page using the `requests` library.
2. Each page is parsed using `BeautifulSoup` to extract product details, including:
   - Product Title
   - Scientific Name
   - Type (e.g., Combo, Leaf, Plant)
   - Price
   - All names in case of combo products
3. The results are stored in a dictionary and written into an Excel file with a separate sheet for each page.

## Output

After running the script, an Excel file named **Fermosa_extract.xlsx** will be generated. Each page of results is saved to a separate sheet, named `page-1`, `page-2`, etc. The sheet contains the following columns:

| Product Title | Scientific Name | Type | Total Units | Name1 | Name2 | Price | URL |
|---------------|-----------------|------|-------------|-------|-------|-------|-----|
| Plant 1       | Sanseveria       | Combo | 2           | Name1 | Name2 | $20   | link |
| Plant 2       | Aloe Vera        | Plant | 1           | -     | -     | $15   | link |

## Example

1. **Run the script to scrape product details and save them to an Excel file:**

```bash
python fermosa_scraper.py
```

2. **The data will be saved in an Excel file named `Fermosa_extract.xlsx`.**

## Explanation of Functions

### `cook_soup(url)`
Fetches and parses the HTML content of the given URL using `BeautifulSoup`.

### `extract_product_name(product_text, is_combo)`
Extracts the scientific name and list of combo names from the product text.

### `extract_type(all_types)`
Determines if the product is a combo or plant.

### `extract_price(product)`
Extracts the price of the product from the HTML.

### `scrape_product(url, is_combo)`
Scrapes product details from an individual product page.

### `scrape_page(page_number)`
Scrapes all products from a given page, collects their details, and stores them in a dictionary.

### `dump_to_excel(all_data)`
Writes all scraped data into an Excel file with separate sheets for each page.

## Implementation Notes

- The script uses `requests` for HTTP requests and `BeautifulSoup` for HTML parsing.
- **Multithreading**: The `ThreadPoolExecutor` is used to scrape multiple pages concurrently, improving performance.
- The data is stored in a dictionary and later written to an Excel file using `pandas`.

## Limitations

- **Network Issues**: If the website is down or unreachable, the script will fail to scrape data.
- **Performance**: While multithreading improves performance, scraping a large number of pages may still take time.
- **Page Structure**: The script assumes that the HTML structure of the website remains consistent across pages.
