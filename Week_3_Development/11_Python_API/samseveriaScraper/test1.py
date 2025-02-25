import unittest
from unittest.mock import patch, MagicMock
from samseveriaForUnit import Scraper
import requests
from bs4 import BeautifulSoup


class TestScraper(unittest.TestCase):

    def setUp(self):
        """Create an instance of the Scraper class before each test."""
        self.scraper = Scraper(
            base_url="https://fermosaplants.com/collections/sansevieria"
        )

    @patch("requests.get")
    def test_extract_product_name(self, mock_get):
        """Test the extract_product_name function."""
        product_text = """
        Scientific Name- Sanseveria Trifasciata
        Some other details about the product
        1. Combo Name1
        2. Combo Name2
        """
        is_combo = True
        cleaned_scientific_name, list_of_names = self.scraper.extract_product_name(
            product_text, is_combo
        )
        self.assertEqual(cleaned_scientific_name, "Sanseveria Trifasciata")
        self.assertEqual(list_of_names, ["Combo Name1", "Combo Name2"])

    def test_determine_type(self):
        """Test the determine_type function."""
        list_of_names_combo = ["combo", "leaf", "plant"]
        list_of_names_no_combo = ["leaf", "plant"]
        self.assertEqual(self.scraper.extract_type(list_of_names_combo), "combo")
        self.assertEqual(self.scraper.extract_type(list_of_names_no_combo), "Plant")

    @patch("requests.get")
    def test_extract_price(self, mock_get):
        """Test the extract_price function."""
        product = MagicMock()
        product.find.return_value = MagicMock(text="$29.99")
        price = self.scraper.extract_price(product)
        self.assertEqual(price, "$29.99")

    @patch("requests.get")
    @patch("scraper.BeautifulSoup")
    def test_scrape_product(self, mock_soup, mock_get):
        """Test the scrape_product method."""
        # Set up mock for BeautifulSoup
        product_html = '<div class="desc product-desc">Scientific Name- Sanseveria Trifasciata</div>'
        mock_get.return_value.content = product_html.encode("utf-8")
        mock_soup.return_value = BeautifulSoup(product_html, "lxml")

        is_combo = False
        ctr = 1
        url = "https://fermosaplants.com/product/1"

        result = self.scraper.scrape_product(url, is_combo, ctr)

        self.assertEqual(result["scientific_name"], "Sanseveria Trifasciata")
        self.assertEqual(result["all_names"], [])
        self.assertEqual(result["total_units"], 1)

    @patch("requests.get")
    @patch("scraper.BeautifulSoup")
    def test_scrape_page(self, mock_soup, mock_get):
        """Test the scrape_page method."""
        # Mock data for scraping
        product_html = """
            <div class="product-item-v5">
                <a href="/product/1">Product 1</a>
                <h4 class="title-product">Combo product name (Leaf)</h4>
                <span class="price">$29.99</span>
            </div>
        """
        mock_get.return_value.content = product_html.encode("utf-8")
        mock_soup.return_value = BeautifulSoup(product_html, "html.parser")

        page_number = 1
        list_final = self.scraper.scrape_page(page_number)

        self.assertEqual(len(list_final), 1)
        self.assertEqual(list_final[0]["Product Title"], "Combo product name (Leaf)")
        self.assertEqual(list_final[0]["Price"], "$29.99")

    @patch("pandas.DataFrame.to_excel")
    def test_dump_to_excel(self, mock_to_excel):
        """Test the dump_to_excel method."""
        final_list = [
            {
                "Product Title": "Product 1",
                "Scientific name": "Sanseveria Trifasciata",
                "Type": "Combo",
                "All_Names": ["Name1", "Name2"],
                "Total Units": 2,
                "Price": "$29.99",
                "URL": "https://example.com/product1",
            }
        ]
        # Mock Pandas writer
        mock_writer = MagicMock()
        self.scraper.dump_to_excel(final_list, 1, mock_writer)
        mock_to_excel.assert_called_once()

    @patch("requests.get")
    @patch("scraper.BeautifulSoup")
    def test_run(self, mock_soup, mock_get):
        """Test the entire scraping and writing to Excel (run)."""
        product_html = """
            <div class="product-item-v5">
                <a href="/product/1">Product 1</a>
                <h4 class="title-product">Combo product name (Leaf)</h4>
                <span class="price">$29.99</span>
            </div>
        """
        mock_get.return_value.content = product_html.encode("utf-8")
        mock_soup.return_value = BeautifulSoup(product_html, "html.parser")

        # Mock Pandas writer
        mock_writer = MagicMock()

        self.scraper.run(total_pages=1)  # Test for only 1 page

        mock_writer.__enter__().save.assert_called_once()


if __name__ == "__main__":
    unittest.main()
