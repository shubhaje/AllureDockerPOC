# AllureDockerPOC

This project demonstrates automated browser testing using [Playwright](https://playwright.dev/python/) with Python and integrates [Allure](https://docs.qameta.io/allure/) for test reporting. The project name is now **AllureDockerPOC**.

## Project Structure

```
AllureDockerPOC/
  Dockerfile
  pytest.ini
  requirements.txt
  run_tests.sh
  README.md
  tests/
    test_example.py
```

## Features
- End-to-end browser automation with Playwright
- Test execution using pytest
- Allure reporting for test results
- Docker support for consistent environment

## Getting Started

### Prerequisites
- Python 3.8+
- Docker (optional, for containerized runs)

### Installation
1. Clone the repository:
   ```powershell
   git clone <repo-url>
   cd playwright-python-allure
   ```
2. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

### Running Tests
- To run tests locally:
  ```powershell
  pytest --alluredir=allure-results
  ```
- To run tests in Docker:
  ```powershell
  docker build -t playwright-python-allure .
  docker run --rm playwright-python-allure
  ```
- To generate Allure report:
  ```powershell
  allure serve allure-results
  ```

## Running Tests with GitHub Actions (Docker)

This project includes a sample GitHub Actions workflow to run tests inside Docker and generate an Allure report.

1. Push your code to GitHub.
2. The workflow in `.github/workflows/ci.yml` will:
   - Build the Docker image.
   - Run tests inside the container.
   - Upload the `allure-results` as an artifact.
   - Optionally publish the Allure report.

To view the Allure report locally after a workflow run:
- Download the `allure-results` artifact from the workflow run.
- Run:
  ```powershell
  allure serve allure-results
  ```

See `.github/workflows/ci.yml` for workflow details.

### Project Files
- `tests/test_example.py`: Example Playwright test
- `requirements.txt`: Python dependencies
- `pytest.ini`: Pytest configuration
- `run_tests.sh`: Shell script to run tests (for Linux/macOS)
- `Dockerfile`: Container setup

## CI/CD
You can integrate this project with GitHub Actions or other CI tools. See `.github/workflows/ci.yml` for an example workflow.

## License
MIT
