# Use official Python slim image
FROM python:3.12.10-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y curl unzip default-jdk nodejs npm && \
    apt-get clean

# Install Allure CLI
RUN curl -o allure.zip -L https://github.com/allure-framework/allure2/releases/download/2.35.1/allure-2.35.1.zip && \
    unzip allure.zip -d /opt/ && \
    ln -s /opt/allure-2.35.1/bin/allure /usr/bin/allure && \
    rm allure.zip

# Set working directory
WORKDIR /app

# Copy all project files
COPY . .

# Ensure run_tests.sh is executable
RUN chmod +x /app/run_tests.sh

# Ensure entrypoint.sh is executable if it exists
RUN [ -f /app/entrypoint.sh ] && chmod +x /app/entrypoint.sh || true

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Install Playwright browsers
RUN python -m playwright install

# Use absolute path for CMD to avoid permission issues
CMD ["/app/run_tests.sh"]
