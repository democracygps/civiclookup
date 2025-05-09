# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

civiclookup is an open-source project that helps identify elected representatives for a given address. It was created to replace the retired Google Civic Info Representatives API (shut down in April 2025) and provides tools for developers, nonprofits, journalists, and civic technologists.

The project starts with U.S. federal legislators (House & Senate) but is designed to scale globally. It:
- Uses Google's `/divisionsByAddress` endpoint to identify political districts based on a user-provided address
- Matches those districts to open-source legislator data to determine who represents that area
- Returns structured data about representatives for a given address

## Development Environment Setup

### Python Setup

```bash
# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables with your Google Civic API key
# Option 1: Use the setup script (recommended)
python setup_api_key.py
# Or make it executable and run directly:
chmod +x setup_api_key.py
./setup_api_key.py

# Option 2: Manually create a .env file in the project root directory:
echo "GOOGLE_CIVIC_API_KEY=your_api_key_here" > .env

# The .env file will be automatically found and loaded by python-dotenv
# You can also place the .env file in the python/ directory if preferred
```

### JavaScript Setup

```bash
# Change to js directory
cd js

# Install dependencies
npm install

# Run tests
npm test
```

## Commands

### Python Commands

```bash
# Get district info from an address (text output)
python python/get_us_district_info_from_address.py "1600 Pennsylvania Ave, Washington DC"

# Get district info as JSON
python python/get_us_district_info_from_address.py --output-format json "1600 Pennsylvania Ave, Washington DC"

# Get district info as YAML
python python/get_us_district_info_from_address.py --output-format yaml "1600 Pennsylvania Ave, Washington DC"

# Filter fields
python python/get_us_district_info_from_address.py --keep-fields name party "1600 Pennsylvania Ave, Washington DC"
python python/get_us_district_info_from_address.py --delete-fields role --output-format json "94110"

# Update US congressional data (downloads from congress-legislators repo)
python python/update_us_congressional_data.py

# This generates cached data used by the district lookup script
# Always run this first before using get_us_district_info_from_address.py

# Update with field filtering options
python python/update_us_congressional_data.py --keep-fields last_name first_name party state
python python/update_us_congressional_data.py --delete-fields twitter facebook youtube

# Run all tests (use our test script to set up Python path correctly)
./run_tests.sh

# Run specific test files (with correct Python path)
PYTHONPATH=. python -m unittest tests/test_update_us_congressional_data.py
PYTHONPATH=. python -m unittest tests/test_get_us_district_info_from_address.py

# Lint and format code individually
black python/
flake8 python/
mypy python/
isort python/

# Or run all checks with the convenience script
./run_checks.sh
```

### JavaScript Commands

```bash
# From the js directory
cd js

# Lint code
npm run lint

# Format code
npm run format

# Run tests
npm test
```

## Project Structure

- `python/` – Python implementation
  - `get_us_district_info_from_address.py`: Handles address lookup to find congressional districts
  - `update_us_congressional_data.py`: Downloads and processes legislator data
  - `README.md`: Python-specific documentation

- `js/` – JavaScript implementation (NPM module)
  - `index.js`: Main module entry point
  - `test/`: JavaScript tests
  - `package.json`: NPM package configuration
  - `.prettierrc`: Prettier formatting configuration
  - `.eslintrc.json`: ESLint linting configuration
  - `tsconfig.json`: TypeScript configuration
  - `README.md`: JavaScript-specific documentation

- `tests/` – Python tests

- Root directory – Project-wide configuration files
  - `requirements.txt`: Python dependencies
  - `pyproject.toml`: Black and isort configuration
  - `mypy.ini`: Type checking configuration
  - `.flake8`: Python linting configuration

## Code Style & Linting

### Python
- Code formatting: `black`
- Linting: `flake8`
- Static type checking: `mypy`
- Import sorting: `isort`

### JavaScript
- Code formatting: `prettier`
- Linting: `eslint`

## Important Considerations

1. **API Key Requirement**: This tool requires each user to provide their own Google Civic API key

2. **International Support**: The project is designed for multilingual support and international expansion
   - Always use UTF-8 encoding and Unicode-aware text processing
   - Preserve original names, accents, and characters when working with non-English datasets

3. **Data Sources**:
   - Current implementation uses Google's `/divisionsByAddress` endpoint
   - Legislator data comes from [congress-legislators](https://github.com/unitedstates/congress-legislators)

4. **Data Storage**:
   - Legislator data is cached locally in a `cached_data/us/` directory
   - Cache is refreshed if older than 24 hours
   - Country-specific data is stored in ISO country code subdirectories (e.g., "us" for United States)

## Future Development

Planned features include:
- U.S. state and local expansion
- Country modules for Canada, the EU, Australia, and Latin America
- Browser-first widget
- Optional integration with various data stores