#!/usr/bin/env python3
"""
Tests for update_us_congressional_data.py
"""

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add parent directory to path to import the module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from python.update_us_congressional_data import (
    build_legislators_dict,
    filter_fields,
    get_current_congress_legislators,
)


class TestUpdateUSCongressionalData(unittest.TestCase):
    """Test the US congressional data update functionality."""

    @patch("python.update_us_congressional_data.requests.get")
    def test_get_current_congress_legislators(self, mock_get):
        """Test that the legislators data is fetched and cached correctly."""
        # Mock response
        mock_response = MagicMock()
        mock_response.content = b"first_name,last_name,state,district\nNancy,Pelosi,CA,12\nAlex,Padilla,CA,\nChuck,Schumer,NY,"
        mock_get.return_value = mock_response

        # Create a temporary directory for the test
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Call function with the temp directory
            df = get_current_congress_legislators(csv_dir=temp_path)

            # Verify the CSV file was created
            csv_path = temp_path / "legislators-current.csv"
            self.assertTrue(csv_path.exists())

            # Verify the DataFrame has the expected content
            self.assertEqual(len(df), 3)
            self.assertTrue("Pelosi" in df["last_name"].values)
            self.assertTrue("Padilla" in df["last_name"].values)
            self.assertTrue("Schumer" in df["last_name"].values)

            # Call the function again - it should use cached data
            mock_get.reset_mock()
            df2 = get_current_congress_legislators(csv_dir=temp_path)

            # Verify the request was not made again
            mock_get.assert_not_called()

    def test_build_legislators_dict(self):
        """Test that the legislators dictionary is built correctly."""
        # Create a test DataFrame
        import pandas as pd

        df = pd.DataFrame(
            {
                "first_name": ["Nancy", "Alex", "Chuck", "Harriet"],
                "last_name": ["Pelosi", "Padilla", "Schumer", "Hageman"],
                "state": ["CA", "CA", "NY", "WY"],
                "district": [12, None, None, 0],  # None for senators
            }
        )

        # Call the function
        result = build_legislators_dict(df)

        # Verify the structure and content
        self.assertIn("states", result)
        self.assertIn("districts", result)

        # Check states (senators)
        self.assertIn("CA", result["states"])
        self.assertIn("NY", result["states"])
        self.assertIn("senators", result["states"]["CA"])
        self.assertEqual(len(result["states"]["CA"]["senators"]), 1)
        self.assertEqual(result["states"]["CA"]["senators"][0]["last_name"], "Padilla")

        # Check districts (representatives)
        self.assertIn("CA-12", result["districts"])
        self.assertIn("WY-0", result["districts"])
        self.assertEqual(result["districts"]["CA-12"]["representative"]["last_name"], "Pelosi")
        self.assertEqual(result["districts"]["WY-0"]["representative"]["last_name"], "Hageman")

    def test_filter_fields(self):
        """Test the field filtering functionality."""
        # Test data
        row = {
            "name": "John Doe",
            "party": "Independent",
            "phone": "555-1234",
            "email": "john@example.com",
        }

        # Test keeping fields
        filtered = filter_fields(row, keep_fields={"name", "party"})
        self.assertEqual(filtered, {"name": "John Doe", "party": "Independent"})
        self.assertNotIn("phone", filtered)
        self.assertNotIn("email", filtered)

        # Test deleting fields
        filtered = filter_fields(row, delete_fields={"phone", "email"})
        self.assertEqual(filtered, {"name": "John Doe", "party": "Independent"})
        self.assertNotIn("phone", filtered)
        self.assertNotIn("email", filtered)

        # Test with no filtering
        filtered = filter_fields(row)
        self.assertEqual(filtered, row)


if __name__ == "__main__":
    unittest.main()
