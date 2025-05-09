#!/bin/bash
#
# run_checks.sh - Run linting and tests for the civiclookup project
#
# This script runs linting and tests for Python, and is set up to run
# JavaScript linting and tests in the future.

set -e  # Exit immediately if a command exits with a non-zero status

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'  # No Color

# Print section header
section() {
  echo -e "\n${YELLOW}=================================${NC}"
  echo -e "${YELLOW}== $1${NC}"
  echo -e "${YELLOW}=================================${NC}\n"
}

# Run a command and report its success or failure
run_command() {
  local cmd="$1"
  local description="$2"
  
  echo -e "\n${YELLOW}== Running: ${cmd}${NC}"
  if eval "$cmd"; then
    echo -e "${GREEN}✓ ${description} passed${NC}"
    return 0
  else
    echo -e "${RED}✗ ${description} failed${NC}"
    return 1
  fi
}

# Activate virtual environment if it exists
if [ -d "venv-civiclookup" ]; then
  source venv-civiclookup/bin/activate
elif [ -d "venv" ]; then
  source venv/bin/activate
elif [ -d ".venv" ]; then
  source .venv/bin/activate
fi

# Check Python dependencies
section "Checking Python dependencies"
if ! command -v python >/dev/null 2>&1; then
  echo -e "${RED}Python is not installed or not in PATH${NC}"
  exit 1
fi

# Check for required Python packages
required_packages=("black" "flake8" "mypy" "isort")
missing_packages=()

for package in "${required_packages[@]}"; do
  if ! python -c "import $package" >/dev/null 2>&1; then
    missing_packages+=("$package")
  fi
done

if [ ${#missing_packages[@]} -gt 0 ]; then
  echo -e "${YELLOW}Some required packages are missing: ${missing_packages[*]}${NC}"
  echo -e "${YELLOW}Installing missing packages...${NC}"
  pip install -r requirements.txt
fi

# Run Python linting and tests
section "Running Python checks"

PYTHON_ERRORS=0

# Run black in check mode to see if files need formatting
if run_command "black --check python/ tests/"; then
  echo -e "${GREEN}✓ Python code is properly formatted${NC}"
else
  echo -e "${YELLOW}Python code needs formatting. Running black...${NC}"
  if run_command "black python/ tests/"; then
    echo -e "${GREEN}✓ Python code formatted successfully${NC}"
  else
    echo -e "${RED}✗ Failed to format Python code${NC}"
    PYTHON_ERRORS=$((PYTHON_ERRORS + 1))
  fi
fi

# Run isort to check imports
run_command "isort --check-only --profile black python/ tests/" "Import sorting" || {
  echo -e "${YELLOW}Python imports need sorting. Running isort...${NC}"
  run_command "isort --profile black python/ tests/" "Import sorting" || PYTHON_ERRORS=$((PYTHON_ERRORS + 1))
}

# Run flake8 to check for style issues
run_command "flake8 python/ tests/" "Flake8 linting" || PYTHON_ERRORS=$((PYTHON_ERRORS + 1))

# Run mypy for type checking
run_command "mypy python/ tests/" "Type checking" || PYTHON_ERRORS=$((PYTHON_ERRORS + 1))

# Run Python tests
run_command "python -m unittest discover tests" "Python tests" || PYTHON_ERRORS=$((PYTHON_ERRORS + 1))

# Check if JavaScript files exist and run linting and tests if they do
section "Checking for JavaScript files"

if [ -d "js" ] && [ -f "js/package.json" ]; then
  echo -e "${GREEN}JavaScript files found. Running JS checks...${NC}"
  
  # Check if Node.js is installed
  if ! command -v node >/dev/null 2>&1; then
    echo -e "${YELLOW}Node.js is not installed or not in PATH. Skipping JS checks.${NC}"
  else
    section "Running JavaScript checks"
    
    # Change to js directory
    cd js
    
    # Check if dependencies are installed
    if [ ! -d "node_modules" ]; then
      echo -e "${YELLOW}Node.js dependencies not installed. Running npm install...${NC}"
      run_command "npm install" "npm install" || {
        echo -e "${RED}Failed to install Node.js dependencies. Skipping JS checks.${NC}"
        cd ..
        JS_ERRORS=1
      }
    fi
    
    # If installation succeeded, run JS linting and tests
    if [ -d "node_modules" ]; then
      JS_ERRORS=0
      
      # Run ESLint
      if [ -f "node_modules/.bin/eslint" ]; then
        run_command "npm run lint" "JavaScript linting" || JS_ERRORS=$((JS_ERRORS + 1))
      else
        echo -e "${YELLOW}ESLint not found. Skipping JS linting.${NC}"
      fi
      
      # Run Prettier
      if [ -f "node_modules/.bin/prettier" ]; then
        run_command "npm run format -- --check" "JavaScript formatting" || {
          echo -e "${YELLOW}JavaScript files need formatting. Running Prettier...${NC}"
          run_command "npm run format" "JavaScript formatting" || JS_ERRORS=$((JS_ERRORS + 1))
        }
      else
        echo -e "${YELLOW}Prettier not found. Skipping JS formatting.${NC}"
      fi
      
      # Run Jest tests
      if [ -f "node_modules/.bin/jest" ]; then
        run_command "npm test" "JavaScript tests" || JS_ERRORS=$((JS_ERRORS + 1))
      else
        echo -e "${YELLOW}Jest not found. Skipping JS tests.${NC}"
      fi
      
      # Return to root directory
      cd ..
      
      if [ $JS_ERRORS -gt 0 ]; then
        echo -e "${RED}JavaScript checks completed with errors${NC}"
      else
        echo -e "${GREEN}All JavaScript checks passed${NC}"
      fi
    fi
  fi
else
  echo -e "${YELLOW}No JavaScript files found. Skipping JS checks.${NC}"
fi

# Print summary
section "Summary"

if [ $PYTHON_ERRORS -gt 0 ]; then
  echo -e "${RED}Python checks completed with $PYTHON_ERRORS errors${NC}"
  ERRORS=$((ERRORS + PYTHON_ERRORS))
else
  echo -e "${GREEN}All Python checks passed${NC}"
fi

if [ -n "$JS_ERRORS" ] && [ $JS_ERRORS -gt 0 ]; then
  echo -e "${RED}JavaScript checks completed with $JS_ERRORS errors${NC}"
  ERRORS=$((ERRORS + JS_ERRORS))
elif [ -d "js" ] && [ -f "js/package.json" ]; then
  echo -e "${GREEN}All JavaScript checks passed${NC}"
fi

# Exit with error if any checks failed
if [ ${ERRORS:-0} -gt 0 ]; then
  echo -e "\n${RED}$ERRORS check(s) failed${NC}"
  exit 1
else
  echo -e "\n${GREEN}All checks passed!${NC}"
  exit 0
fi