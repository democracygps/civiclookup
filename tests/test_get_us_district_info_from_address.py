#!/usr/bin/env python3
"""
Tests for get_us_district_info_from_address.py
"""

import json
import os
import sys
import unittest
from unittest.mock import MagicMock, patch

# Add parent directory to path to import the module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from python.get_us_district_info_from_address import (
    filter_data,
    filter_legislator_data,
    format_text_output,
    get_us_district_info_from_address,
    parse_result,
)


class TestGetUSDistrictInfoFromAddress(unittest.TestCase):
    """Test the US district info lookup functionality."""

    @patch("python.get_us_district_info_from_address.lookup_divisions")
    @patch("python.get_us_district_info_from_address.get_api_key")
    def test_california_address(self, mock_get_api_key, mock_lookup_divisions):
        """Test a California address."""
        # Mock API key and response
        mock_get_api_key.return_value = "fake_api_key"

        # Create a mock response for a California address
        mock_response = {
            "divisions": {
                "ocd-division/country:us": {"name": "United States"},
                "ocd-division/country:us/state:ca": {"name": "California"},
                "ocd-division/country:us/state:ca/cd:12": {
                    "name": "California's 12th congressional district"
                },
            }
        }
        mock_lookup_divisions.return_value = mock_response

        # Call the function
        result = get_us_district_info_from_address("123 Main St, San Francisco, CA")

        # Verify the result structure
        self.assertIn("districts", result)
        self.assertIn("CA-12", result["districts"])

        # Verify the representatives
        ca_district = result["districts"]["CA-12"]
        self.assertIn("representatives", ca_district)
        self.assertTrue(
            any(rep["name"] == "Nancy Pelosi" for rep in ca_district["representatives"])
        )

        # Verify the senators
        self.assertIn("senators", ca_district)
        senator_names = [s["name"] for s in ca_district["senators"]]
        self.assertIn("Alex Padilla", senator_names)
        self.assertIn("Laphonza R. Butler", senator_names)

    @patch("python.get_us_district_info_from_address.lookup_divisions")
    @patch("python.get_us_district_info_from_address.get_api_key")
    def test_vermont_address(self, mock_get_api_key, mock_lookup_divisions):
        """Test a Vermont address with at-large district."""
        # Mock API key and response
        mock_get_api_key.return_value = "fake_api_key"

        # Create a mock response for a Vermont address
        mock_response = {
            "divisions": {
                "ocd-division/country:us": {"name": "United States"},
                "ocd-division/country:us/state:vt": {"name": "Vermont"},
            }
        }
        mock_lookup_divisions.return_value = mock_response

        # Call the function
        result = get_us_district_info_from_address("123 Main St, Bethel, VT")

        # Verify the result structure
        self.assertIn("districts", result)
        self.assertIn("VT-AL", result["districts"])

        # Verify the representatives
        vt_district = result["districts"]["VT-AL"]
        self.assertIn("representatives", vt_district)
        self.assertTrue(
            any(rep["name"] == "Becca Balint" for rep in vt_district["representatives"])
        )

        # Verify the senators
        self.assertIn("senators", vt_district)
        senator_names = [s["name"] for s in vt_district["senators"]]
        self.assertIn("Bernie Sanders", senator_names)
        self.assertIn("Peter Welch", senator_names)

    @patch("python.get_us_district_info_from_address.lookup_divisions")
    @patch("python.get_us_district_info_from_address.get_api_key")
    def test_dc_address(self, mock_get_api_key, mock_lookup_divisions):
        """Test a Washington DC address."""
        # Mock API key and response
        mock_get_api_key.return_value = "fake_api_key"

        # Create a mock response for a DC address
        mock_response = {
            "divisions": {
                "ocd-division/country:us": {"name": "United States"},
                "ocd-division/country:us/district:dc": {"name": "District of Columbia"},
            }
        }
        mock_lookup_divisions.return_value = mock_response

        # Call the function
        result = get_us_district_info_from_address(
            "1600 Pennsylvania Ave, Washington, DC"
        )

        # Verify the result structure
        self.assertIn("districts", result)
        self.assertIn("DC-AL", result["districts"])

        # Verify the delegate
        dc_district = result["districts"]["DC-AL"]
        self.assertIn("representatives", dc_district)
        reps = dc_district["representatives"]
        self.assertEqual(len(reps), 1)
        self.assertEqual(reps[0]["name"], "Eleanor Holmes Norton")
        self.assertEqual(reps[0]["role"], "Delegate (Non-Voting)")

        # DC has no senators
        self.assertIn("senators", dc_district)
        self.assertEqual(len(dc_district["senators"]), 0)

    def test_filter_legislator_data(self):
        """Test filtering legislator data."""
        # Test data
        data = {
            "districts": {
                "CA-12": {
                    "senators": [
                        {
                            "name": "Alex Padilla",
                            "party": "Democratic",
                            "role": "Senator",
                            "state": "CA",
                        },
                        {
                            "name": "Laphonza R. Butler",
                            "party": "Democratic",
                            "role": "Senator",
                            "state": "CA",
                        },
                    ],
                    "representatives": [
                        {
                            "name": "Nancy Pelosi",
                            "party": "Democratic",
                            "role": "Representative",
                            "district": "CA-12",
                        }
                    ],
                }
            }
        }

        # Test keeping fields
        filtered = filter_legislator_data(data, keep_fields={"name", "party"})

        # Verify senators filtered correctly
        senators = filtered["districts"]["CA-12"]["senators"]
        self.assertEqual(len(senators), 2)
        self.assertEqual(senators[0], {"name": "Alex Padilla", "party": "Democratic"})
        self.assertNotIn("role", senators[0])

        # Verify representatives filtered correctly
        reps = filtered["districts"]["CA-12"]["representatives"]
        self.assertEqual(len(reps), 1)
        self.assertEqual(reps[0], {"name": "Nancy Pelosi", "party": "Democratic"})
        self.assertNotIn("role", reps[0])

    def test_format_text_output(self):
        """Test formatting data as text."""
        # Test data
        data = {
            "districts": {
                "CA-12": {
                    "senators": [
                        {
                            "name": "Alex Padilla",
                            "party": "Democratic",
                            "role": "Senator",
                            "state": "CA",
                        },
                        {
                            "name": "Laphonza R. Butler",
                            "party": "Democratic",
                            "role": "Senator",
                            "state": "CA",
                        },
                    ],
                    "representatives": [
                        {
                            "name": "Nancy Pelosi",
                            "party": "Democratic",
                            "role": "Representative",
                            "district": "CA-12",
                        }
                    ],
                }
            }
        }

        # Format as text
        text = format_text_output(data)

        # Verify the text contains expected information
        self.assertIn("District: CA-12", text)
        self.assertIn("Senators:", text)
        self.assertIn("Alex Padilla (Democratic)", text)
        self.assertIn("Laphonza R. Butler (Democratic)", text)
        self.assertIn("Representatives:", text)
        self.assertIn("Nancy Pelosi (Democratic)", text)


if __name__ == "__main__":
    unittest.main()
