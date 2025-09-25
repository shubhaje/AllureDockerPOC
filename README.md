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

## Running Tests in Docker

1. Build the Docker image:
   ```sh
   docker build -t playwright-allure .
   ```
2. Run the tests inside the container:
   ```sh
   docker run --rm -v $(pwd):/app playwright-allure
   ```
   - On Windows (PowerShell), use:
     ```powershell
     docker run --rm -v ${PWD}:/app playwright-allure
     ```
3. After the run, the `allure-results` directory will be available in your project folder. Generate the Allure report:
   ```sh
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

## Integrating with GitHub Actions

1. Ensure your repository contains the workflow file at `.github/workflows/ci.yml`.
2. Push your code to GitHub.
3. On every push or pull request to the `main` branch, GitHub Actions will:
   - Build the Docker image.
   - Run tests inside Docker.
   - Upload the Allure results as an artifact.
4. You can view workflow runs and download the Allure report from the Actions tab in your GitHub repository.

See `.github/workflows/ci.yml` for the workflow configuration.

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
