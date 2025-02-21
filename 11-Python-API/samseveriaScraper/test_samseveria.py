import unittest
from samseveriav3 import Scraper
import requests
from unittest.mock import patch, MagicMock
from urllib.parse import urljoin


class TestScraper(unittest.TestCase):

    def setUp(self):

        self.scraper = Scraper(
            base_url="https://fermosaplants.com/collections/sansevieria"
        )

    def test_extract_product_name(self):
        product_text = """Scientific Name- Sanseveria Trifasciata
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

    def test_extract_type(self):
        test_text1 = "Sanseveria Combo Plant"
        test_text2 = "Sanseveria Fritonia clump"
        test_text3 = "Sanseveria"
        self.assertEqual(self.scraper.extract_type(test_text1), "Combo")
        self.assertEqual(self.scraper.extract_type(test_text2), "Clump")
        self.assertEqual(self.scraper.extract_type(test_text3), "Plant")

    def test_extract_price(self):
        product = MagicMock()
        product.find.return_value = MagicMock(text="Rs. 350.00")
        self.assertEqual(self.scraper.extract_price(product), "Rs. 350.00")

    @patch("requests.get")
    @patch("scraper.BeautifulSoup")
    def test_cook_soup(self):
        pass
        # soup_html = '<div class="desc product-desc">Scientific Name- Sanseveria Trifasciata</div>'
        # mock_get.return_value.content = product_html.encode("utf-8")
