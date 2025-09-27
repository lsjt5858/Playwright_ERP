#!/bin/bash
set -euo pipefail

# Run from script directory to make paths stable
cd "$(dirname "$0")"

pytest
allure generate allure-results -o allure-report --clean
allure serve ./allure-report
