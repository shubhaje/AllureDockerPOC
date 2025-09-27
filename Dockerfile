# Use official Python slim image
FROM python:3.12.10-slim

# Install system dependencies including browsers dependencies
RUN apt-get update && \
    apt-get install -y \
    curl \
    unzip \
    default-jdk \
    nodejs \
    npm \
    wget \
    gnupg \
    libnss3-dev \
    libatk-bridge2.0-dev \
    libdrm-dev \
    libxkbcommon-dev \
    libgtk-3-dev \
    libgbm-dev \
    libasound2-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Allure CLI
RUN curl -o allure.zip -L https://github.com/allure-framework/allure2/releases/download/2.35.1/allure-2.35.1.zip && \
    unzip allure.zip -d /opt/ && \
    ln -s /opt/allure-2.35.1/bin/allure /usr/bin/allure && \
    rm allure.zip

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Install Playwright browsers with dependencies
RUN python -m playwright install --with-deps chromium

# Copy all project files
COPY . .

# Ensure run_tests.sh is executable
RUN chmod +x /app/run_tests.sh

# Create a modified run script for Docker environment
RUN echo '#!/bin/bash\n\
set -e\n\
\n\
echo "🧼 Cleaning reports..."\n\
if [ "$SKIP_CLEANUP" = "true" ]; then\n\
  echo "Skipping cleanup as per SKIP_CLEANUP variable."\n\
elif mountpoint -q /app/allure-results || mountpoint -q /app/allure-report; then\n\
    ECHO "Detected mounted volumes, skipping directory removal"\n\
    rm -rf /app/allure-results/* 2>/dev/null || echo "Could not clean allure-results contents"\n\
    rm -rf /app/allure-report/* 2>/dev/null || echo "Could not clean allure-report contents"\n\
else\n\
        rm -rf allure-results allure-report 2>/dev/null || echo "Could not remove directories"\n\
fi\n\
    rm -rf allure-results allure-report\n\
mkdir -p allure-results\n\
\n\
echo "🚀 Running tests..."\n\
python -m pytest --browser chromium --alluredir=allure-results\n\
\n\
echo "📊 Generating Allure report..."\n\
allure generate allure-results --clean -o allure-report\n\
\n\
echo "✅ Tests completed successfully!"\n\
echo "📁 Reports generated in allure-report directory"' > /app/run_tests_docker.sh && \
    chmod +x /app/run_tests_docker.sh

# Use the Docker-optimized script
CMD ["/app/run_tests_docker.sh"]
