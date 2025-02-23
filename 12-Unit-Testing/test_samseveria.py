import unittest
from unittest.mock import patch, MagicMock
from scraper import Scraper  # Importing the Scraper class
from bs4 import BeautifulSoup


class TestScraper(unittest.TestCase):
    """
    Unit tests for the Scraper class to verify functionalities
    like product name extraction, type extraction, price extraction,
    and webpage parsing.
    """

    def setUp(self):
        """Initialize the Scraper instance before each test."""
        self.scraper = Scraper(
            base_url="https://fermosaplants.com/collections/sansevieria"
        )

    def test_extract_product_name(self):
        """Test extraction of scientific name from product text for a non-combo product."""
        product_text = "Scientific Name- Sansevieria Trifasciata"
        is_combo = False

        result = self.scraper.extract_product_name(product_text, is_combo)

        # Assertions to check extracted product name and combo list
        self.assertEqual(result, ("Sansevieria Trifasciata", []))

    def test_extract_product_name_combo(self):
        """Test extraction of scientific name and combo names from a combo product text."""
        product_text = "1. Sansevieria Zeylanica 2. Sansevieria Moonshine"
        is_combo = True

        result = self.scraper.extract_product_name(product_text, is_combo)

        # Assertions to verify the extracted names
        self.assertEqual(
            result, ("Sanseveria", ["Sansevieria Zeylanica", "Sansevieria Moonshine"])
        )

    def test_extract_type(self):
        """Test the extraction of product type from different product descriptions."""
        self.assertEqual(self.scraper.extract_type("Combo Pack"), "Combo")
        self.assertEqual(self.scraper.extract_type("Single Plant"), "Plant")

    @patch("requests.get")
    def test_cook_soup_success(self, mock_get):
        """Test if cook_soup correctly fetches and parses HTML content on a successful request."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = "<html><body><div>Test</div></body></html>"
        mock_get.return_value = mock_response

        result = self.scraper.cook_soup("https://example.com")

        # Assertions to check if the result is a BeautifulSoup object
        self.assertIsInstance(result, BeautifulSoup)

    @patch("requests.get")
    def test_cook_soup_failure(self, mock_get):
        """Test cook_soup behavior when an HTTP request fails."""
        mock_get.side_effect = Exception("Request failed")

        # Ensure an exception is raised on request failure
        with self.assertRaises(Exception) as context:
            self.scraper.cook_soup("https://example.com")
        self.assertEqual(str(context.exception), "Request failed")

    def test_extract_price(self):
        """Test extraction of price from product HTML."""
        product_html = '<div><span class="price">$20</span></div>'
        product = BeautifulSoup(product_html, "lxml")

        price = self.scraper.extract_price(product)

        # Assertions to check extracted price
        self.assertEqual(price, "$20")

    @patch("scraper.Scraper.cook_soup")
    def test_scrape_product(self, mock_cook_soup):
        """Test scraping of individual product details from a webpage."""
        mock_html = '<div class="desc product-desc">Scientific Name- Sansevieria Laurentii</div>'
        mock_soup = BeautifulSoup(mock_html, "lxml")
        mock_cook_soup.return_value = mock_soup

        result = self.scraper.scrape_product("https://example.com", False)

        # Assertions to check scraped product details
        self.assertEqual(
            result,
            {
                "scientific_name": "Sansevieria Laurentii",
                "all_names": [],
                "total_units": 1,
            },
        )

    @patch("scraper.Scraper.cook_soup")
    def test_scrape_page(self, mock_cook_soup):
        """Test scraping of product listings from a page."""
        mock_html = """
        <div class="product-item-v5">
            <a href="/product1"></a>
            <h4 class="title-product">Sansevieria Golden Hahnii</h4>
            <span class="price">Rs. 250</span>
        </div>
        """
        mock_soup = BeautifulSoup(mock_html, "lxml")
        mock_cook_soup.return_value = mock_soup

        with patch(
            "scraper.Scraper.scrape_product",
            return_value={
                "scientific_name": "Sansevieria Golden Hahnii",
                "all_names": [],
                "total_units": 1,
            },
        ):
            result = self.scraper.scrape_page(1)

            # Assertions to check the scraped product list
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]["Product Title"], "Sansevieria Golden Hahnii")
            self.assertEqual(result[0]["Price"], "Rs. 250")


if __name__ == "__main__":
    unittest.main()
