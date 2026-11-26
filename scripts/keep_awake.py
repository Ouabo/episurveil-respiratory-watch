"""Open the public apps in a headless browser so that Streamlit Community Cloud does not put them to sleep;
if an app is already asleep, press its wake-up button. Used by .github/workflows/keep-awake.yml.
Run locally: pip install playwright && playwright install chromium && python scripts/keep_awake.py"""
import sys
import time

from playwright.sync_api import sync_playwright

APPS = ["https://episurveil-respiratory.streamlit.app/", "https://episurveil.streamlit.app/"]
WAKE_TEXT = "get this app back up"


def visit(page, url: str) -> str:
    page.goto(url, wait_until="domcontentloaded", timeout=120_000)
    time.sleep(10)
    button = page.get_by_role("button", name=WAKE_TEXT, exact=False)
    if button.count():
        button.first.click()
        time.sleep(60)          # give the app time to start
        return "was asleep, woken up"
    return "awake"


if __name__ == "__main__":
    failed = False
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        for url in APPS:
            try:
                print(url, "->", visit(page, url))
            except Exception as e:  # report and go on with the next app
                failed = True
                print(url, "-> ERROR", e)
        browser.close()
    sys.exit(1 if failed else 0)
