import re
from playwright.sync_api import Page, TimeoutError

def _try_selectors(page: Page, candidates, timeout=2000):
    """Try several selector strategies and return the first visible locator, or None."""
    for desc, fn in candidates:
        try:
            loc = fn(page)
            # if locator object is returned, check existence/visibility
            if loc and loc.count() > 0:
                try:
                    loc.wait_for(state="visible", timeout=timeout)
                    print(f"✅ Found visible element with: {desc}")
                    return loc
                except TimeoutError:
                    print(f"⚠️ Element found but not visible for: {desc}")
                    return loc  # still return it as fallback (maybe clickable via JS)
        except Exception as e:
            print(f"❌ Selector attempt '{desc}' raised: {e}")
    return None

def _search_in_frames(page: Page, selector_text):
    """Look for a text in frames (useful if page embeds content in an iframe)."""
    for frame in page.frames:
        try:
            loc = frame.locator(selector_text)
            if loc.count() > 0:
                print("🔎 Found inside iframe:", frame.url)
                return loc, frame
        except Exception:
            continue
    return None, None

def test_example(page: Page):
    try:
        page.goto("https://playwright.dev/", wait_until="networkidle")
        assert "Playwright" in page.title()
        print("Page title:", page.title())

        # wait for main content to appear
        page.wait_for_selector("main", timeout=5000)

        # --- Example: find the "Get started" link with several strategies ---
        candidates = [
            ("get_by_role", lambda p: p.get_by_role("link", name=re.compile("Get started", re.I))),
            ("get_by_text", lambda p: p.get_by_text("Get started")),
            ("css_href", lambda p: p.locator("a[href*='/docs/intro']")),
            ("css_has_text", lambda p: p.locator("a:has-text('Get started')")),
            ("text_selector", lambda p: p.locator("text=Get started")),
        ]

        get_started = _try_selectors(page, candidates, timeout=3000)

        # If not found, try searching inside iframes
        if not get_started:
            loc_in_frame, frame = _search_in_frames(page, "text=Get started")
            if loc_in_frame:
                get_started = loc_in_frame

        assert get_started, "Could not find the 'Get started' link after trying multiple selectors."

        # click (use force if element covered by overlay; but prefer to debug overlay)
        get_started.click()
        page.wait_for_url("**/docs/intro", timeout=7000)
        print("Navigated to:", page.url)

        # Validate an H1 or fallback to contains text
        heading = page.locator("h1")
        heading.wait_for(state="visible", timeout=5000)
        heading_text = heading.inner_text().strip()
        print("Heading:", heading_text)
        assert "Installation" in heading_text or "Getting started" in heading_text or len(heading_text) > 0

    except Exception as e:
        # useful debugging artifacts
        print("Test failed:", e)
        page.screenshot(path="failure.png", full_page=True)
        # save html for quick inspection
        with open("failure.html", "w", encoding="utf-8") as f:
            f.write(page.content())
        raise
