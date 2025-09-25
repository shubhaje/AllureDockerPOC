FROM python:3.12.10-slim

# Set working directory
WORKDIR /app

# Copy everything
COPY . .

# Install Python packages
RUN pip install --upgrade pip && pip install -r requirements.txt

# Install Playwright browsers
RUN python -m playwright install

# Make the script executable
RUN chmod +x /app/run_tests.sh

# Make entrypoint.sh executable if it exists
RUN if [ -f /app/entrypoint.sh ]; then chmod +x /app/entrypoint.sh; fi

# Set CMD to run_tests.sh using absolute path
CMD ["/app/run_tests.sh"]
