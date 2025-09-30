
def test_example(page):
    page.goto("https://playwright.dev/")
    assert "Playwright" in page.title()
    print("playwright test")
    print("page title:", page.title())
