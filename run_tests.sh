#!/bin/bash
#
# run_tests.sh - Run all tests for the civiclookup project
#
# This script runs the tests with the correct Python path setup

# Set up PYTHONPATH to include the root directory
export PYTHONPATH="${PYTHONPATH:+${PYTHONPATH}:}$(pwd)"

# Now run the tests
python -m unittest discover tests