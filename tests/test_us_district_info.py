import os
import sys
import unittest
from unittest.mock import MagicMock, patch

# Add the parent directory to the path so we can import the module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from python.get_us_district_info_from_address import get_us_district_info_from_address


class TestUSDistrictInfo(unittest.TestCase):
    """Test the US district info lookup functionality."""

    @patch("python.get_us_district_info_from_address.lookup_divisions")
    @patch("python.get_us_district_info_from_address.get_api_key")
    def test_address_lookup(self, mock_get_api_key, mock_lookup_divisions):
        """Test that address lookup works correctly."""
        # Mock the API key and response
        mock_get_api_key.return_value = "fake_api_key"

        # Create a mock response that mimics the structure from the Google Civic API
        mock_response = {
            "divisions": {
                "ocd-division/country:us/state:ca/cd:12": {
                    "name": "California's 12th congressional district"
                },
                "ocd-division/country:us/state:ca": {"name": "California"},
            }
        }
        mock_lookup_divisions.return_value = mock_response

        # Call the function with a test address
        result = get_us_district_info_from_address("123 Main St, San Francisco, CA")

        # Verify the result contains expected district information
        self.assertIn("districts", result)
        self.assertIn("CA-12", result["districts"])
        # Check for representatives and senators in the district info
        self.assertTrue(len(result["districts"]["CA-12"]["representatives"]) > 0)
        self.assertTrue(len(result["districts"]["CA-12"]["senators"]) > 0)

    def test_invalid_address(self):
        """Test that an invalid address returns an appropriate error."""
        # This would typically call the actual function, but would fail because
        # there's no API key. We'll use a mock to simulate a failed lookup
        with patch(
            "python.get_us_district_info_from_address.get_district_info_from_civic_api"
        ) as mock_lookup:
            mock_lookup.return_value = None

            result = get_us_district_info_from_address("Invalid Address XYZ")

            # Verify the result contains an error and empty districts
            self.assertIsNotNone(result.get("error"))
            self.assertEqual(result.get("districts"), {})


if __name__ == "__main__":
    unittest.main()
