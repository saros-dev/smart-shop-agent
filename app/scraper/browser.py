from playwright.sync_api import sync_playwright

def get_browser():
    playwright = sync_playwright().start()

    browser = playwright.chromium.launch(
        headless=True
    )

    return playwright, browser
