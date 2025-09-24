FROM python:3.12.10-slim

# Install tools
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

# Copy everything
COPY . .

# Install Python packages
RUN pip install --upgrade pip && pip install -r requirements.txt

# Install Playwright browsers
RUN python -m playwright install

# Make the script executable
RUN chmod +x run_tests.sh

# Make the workflow script executable (add this if you have a workflow.sh)
RUN chmod +x workflow.sh

# Change the CMD to run workflow.sh instead of run_tests.sh
CMD ["./workflow.sh"]
