import re
from playwright.sync_api import Page, TimeoutError, expect
from datetime import datetime


def _try_selectors(page: Page, candidates, timeout=2000):
    """Try several selector strategies and return the first visible locator, or None."""
    for desc, fn in candidates:
        try:
            loc = fn(page)
            if loc and loc.count() > 0:
                try:
                    loc.wait_for(state="visible", timeout=timeout)
                    print(f"✅ Found visible element with: {desc}")
                    return loc
                except TimeoutError:
                    print(f"⚠️ Element found but not visible for: {desc}")
                    return loc  # fallback
        except Exception as e:
            print(f"❌ Selector attempt '{desc}' raised: {e}")
    return None


def _search_in_frames(page: Page, selector_text):
    """Look for a text in frames."""
    for frame in page.frames:
        try:
            loc = frame.locator(selector_text)
            if loc.count() > 0:
                print("🔎 Found inside iframe:", frame.url)
                return loc, frame
        except Exception:
            continue
    return None, None


def _save_debug_artifacts(page: Page, prefix="failure"):
    """Save screenshot and HTML for debugging."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = f"{prefix}_{timestamp}.png"
    html_path = f"{prefix}_{timestamp}.html"

    try:
        page.screenshot(path=screenshot_path, full_page=True)
        print(f"📸 Screenshot saved: {screenshot_path}")
    except Exception as e:
        print(f"Failed to save screenshot: {e}")

    try:
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(page.content())
        print(f"📄 HTML saved: {html_path}")
    except Exception as e:
        print(f"Failed to save HTML: {e}")


def _verify_page_loaded(page: Page, timeout=10000):
    """Verify page has fully loaded."""
    try:
        page.wait_for_load_state("networkidle", timeout=timeout)
        ready_state = page.evaluate("() => document.readyState")
        assert ready_state == "complete", f"Page not fully loaded. ReadyState: {ready_state}"
        print("✅ Page fully loaded and ready")
        return True
    except Exception as e:
        print(f"⚠️ Page load verification failed: {e}")
        return False


def _verify_no_errors(page: Page):
    """Check for JS errors on the page."""
    errors = page.evaluate("""() => window.__playwright_errors__ || []""")
    if errors:
        print(f"⚠️ JavaScript errors detected: {errors}")
        return False
    print("✅ No JavaScript errors detected")
    return True


def test_example(page: Page):
    """Main test function with robust error handling."""
    test_start_time = datetime.now()
    print(f"\n🚀 Test started at: {test_start_time}")

    try:
        # Collect console errors and warnings
        page.on("pageerror", lambda exc: print(f"❌ Page error: {exc}"))
        page.on(
            "console",
            lambda msg: print(f"🖥️ Console {msg.type}: {msg.text}")
            if msg.type in ["error", "warning"]
            else None,
        )

        # Step 1: Navigate to homepage
        print("\n📍 Step 1: Navigating to Playwright homepage...")
        response = page.goto("https://playwright.dev/", wait_until="networkidle", timeout=30000)
        assert response and response.ok, f"Failed to load page. Status: {response.status if response else 'No response'}"
        print(f"✅ Page loaded with status: {response.status}")

        _verify_page_loaded(page)

        # Step 2: Verify title
        print("\n📍 Step 2: Verifying page title...")
        expect(page).to_have_title(re.compile("Playwright", re.I))
        print(f"✅ Page title verified: {page.title()}")

        # Step 3: Wait for main content
        print("\n📍 Step 3: Waiting for main content...")
        page.wait_for_selector("main", timeout=5000, state="visible")
        print("✅ Main content visible")

        # Step 4: Find "Get started" link
        print("\n📍 Step 4: Finding 'Get started' link...")
        candidates = [
            ("get_by_role", lambda p: p.get_by_role("link", name=re.compile("Get started", re.I))),
            ("get_by_text", lambda p: p.get_by_text("Get started", exact=False)),
            ("css_href", lambda p: p.locator("a[href*='/docs/intro']")),
            ("css_has_text", lambda p: p.locator("a:has-text('Get started')")),
            ("text_selector", lambda p: p.locator("text=Get started")),
        ]
        get_started = _try_selectors(page, candidates, timeout=3000)

        if not get_started:
            print("🔎 Searching in iframes...")
            loc_in_frame, frame = _search_in_frames(page, "text=Get started")
            if loc_in_frame:
                get_started = loc_in_frame

        assert get_started, "Could not find the 'Get started' link."
        expect(get_started).to_be_visible()
        expect(get_started).to_be_enabled()

        # Step 5: Click the link
        print("\n📍 Step 5: Clicking 'Get started' link...")
        get_started.click()
        page.wait_for_url("**/docs/intro", timeout=10000)
        print(f"✅ Navigated to: {page.url}")

        _verify_page_loaded(page)

        # Step 6: Verify heading
        print("\n📍 Step 6: Verifying page heading...")
        heading = page.locator("h1").first
        expect(heading).to_be_visible(timeout=5000)
        heading_text = heading.inner_text().strip()
        print(f"✅ Heading found: '{heading_text}'")
        assert len(heading_text) > 0, "Heading text is empty"

        expected_keywords = ["Installation", "Getting started", "Introduction", "Playwright"]
        assert any(keyword.lower() in heading_text.lower() for keyword in expected_keywords), \
            f"Heading '{heading_text}' doesn't contain expected keywords"

        # Step 7: Additional verifications
        nav = page.locator("nav").first
        expect(nav).to_be_visible()
        content = page.locator("main, article, .content").first
        expect(content).to_be_visible()
        word_count = page.evaluate("() => document.body.innerText.split(/\\s+/).length")
        assert word_count > 50, f"Page seems empty. Word count: {word_count}"
        print(f"✅ Page has substantial content ({word_count} words)")

        broken_images = page.evaluate("""
            () => Array.from(document.images).filter(img => !img.complete || img.naturalHeight === 0).length
        """)
        if broken_images > 0:
            print(f"⚠️ Warning: {broken_images} broken images detected")
        else:
            print("✅ All images loaded successfully")

        page.screenshot(path="test_success.png", full_page=True)
        test_duration = (datetime.now() - test_start_time).total_seconds()
        print(f"\n✅ TEST PASSED in {test_duration:.2f} seconds")

    except AssertionError as e:
        print(f"\n❌ ASSERTION FAILED: {e}")
        _save_debug_artifacts(page, "assertion_failure")
        raise
    except TimeoutError as e:
        print(f"\n⏱️ TIMEOUT ERROR: {e}")
        _save_debug_artifacts(page, "timeout_failure")
        raise
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        _save_debug_artifacts(page, "failure")
        raise
    finally:
        test_duration = (datetime.now() - test_start_time).total_seconds()
        print(f"\n⏱️ Test duration: {test_duration:.2f} seconds")


def test_playwright_example(page: Page):
    """Wrapper for Playwright test runner."""
    test_example(page)
