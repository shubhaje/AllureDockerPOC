#!/bin/bash
set -e

echo "🧼 Cleaning reports..."
rm -rf allure-results allure-report
mkdir -p allure-results

echo "🚀 Running tests..."
pytest --alluredir=/app/allure-results --html=/app/allure-report/report.html

echo "📊 Generating Allure report..."
allure generate allure-results --clean -o allure-report
echo "🌐 Opening Allure report..."
allure open allure-report
