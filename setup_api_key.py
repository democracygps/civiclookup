#!/usr/bin/env python3
"""
setup_api_key.py

Set up the Google Civic API key for use with civiclookup.

This script helps create or update the .env file with your Google Civic API key.
"""

import os
import sys
from pathlib import Path

def setup_api_key():
    """
    Set up the Google Civic API key in the .env file.
    
    Prompts the user for their API key and writes it to the .env file.
    """
    # Get the API key from the user
    print("Please enter your Google Civic API key.")
    print("You can obtain a key from the Google Cloud Console: https://console.cloud.google.com/")
    api_key = input("API Key: ").strip()
    
    if not api_key:
        print("Error: API key cannot be empty.")
        sys.exit(1)
    
    # Determine the .env file location
    root_dir = Path(__file__).parent
    env_path = root_dir / ".env"
    
    # Check if .env already exists
    if env_path.exists():
        # Read existing content
        with open(env_path, "r") as f:
            env_content = f.read()
        
        # Check if GOOGLE_CIVIC_API_KEY is already defined
        if "GOOGLE_CIVIC_API_KEY=" in env_content:
            # Replace the existing key
            lines = []
            for line in env_content.splitlines():
                if line.startswith("GOOGLE_CIVIC_API_KEY="):
                    lines.append(f"GOOGLE_CIVIC_API_KEY={api_key}")
                else:
                    lines.append(line)
            
            # Write the updated file
            with open(env_path, "w") as f:
                f.write("\n".join(lines))
            
            print(f"Updated existing API key in {env_path}")
        else:
            # Append the new key
            with open(env_path, "a") as f:
                f.write(f"\nGOOGLE_CIVIC_API_KEY={api_key}\n")
            
            print(f"Added API key to existing .env file at {env_path}")
    else:
        # Create a new .env file
        with open(env_path, "w") as f:
            f.write(f"GOOGLE_CIVIC_API_KEY={api_key}\n")
        
        print(f"Created new .env file with API key at {env_path}")
    
    print("\nAPI key setup complete. You can now use the civiclookup tools.")


if __name__ == "__main__":
    setup_api_key()