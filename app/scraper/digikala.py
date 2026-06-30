from app.scraper.browser import get_browser

def search_products(query: str):

    playwright, browser = get_browser()

    page = browser.new_page()

    url = f"https://www.digikala.com/search/?q={query}"

    page.goto(url)

    page.wait_for_timeout(5000)

    title = page.title()

    browser.close()
    playwright.stop()

    return title
