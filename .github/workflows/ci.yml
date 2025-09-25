name: Run Tests in Docker

on:
  push:
    branches:
      - main
  workflow_dispatch:

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Build Docker image
        run: |
          docker build \
            --no-cache \
            -t test-image \
            .

      - name: Debug: List files in image
        run: |
          docker run --rm test-image ls -l /app

      - name: Debug: Check script permissions
        run: |
          docker run --rm test-image ls -l /app/run_tests.sh

      - name: Run tests in container