FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy

WORKDIR /app

# Install Python packages
RUN pip install --no-cache-dir \
    playwright==1.40.0 \
    pytest==7.4.3 \
    pytest-playwright==0.4.4 \
    allure-pytest==2.13.2

# Install Playwright browsers
RUN playwright install chromium

# Copy test files
COPY tests/ /app/tests/
COPY pytest.ini /app/pytest.ini

# Create output directory
RUN mkdir -p /app/allure-results

# Default command
CMD ["python", "-m", "pytest", "/app/tests/", "-v", "--alluredir=/app/allure-results"]