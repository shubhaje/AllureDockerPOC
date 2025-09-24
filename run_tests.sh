#!/bin/bash

echo "🧼 Cleaning reports..."
rm -rf allure-results allure-report
mkdir -p allure-results allure-report

echo "🚀 Running tests..."
pytest --headed --project=chromium

echo "📊 Generating Allure report..."
allure generate allure-results --clean -o allure-report

echo "🌐 Opening Allure report..."
allure open allure-report
