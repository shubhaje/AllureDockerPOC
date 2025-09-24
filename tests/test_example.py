
def test_example(page):
    page.goto("https://playwright.dev/")
    assert "Playwright" in page.title()
