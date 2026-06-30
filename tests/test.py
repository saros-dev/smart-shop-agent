from playwright.sync_api import sync_playwright
from urllib.parse import urljoin
import re

BASE = "https://www.digikala.com"


# ----------------------------
# utils
# ----------------------------
def normalize_price(text: str):
    if not text:
        return None

    # remove separators
    text = text.replace(",", "").replace("٬", "").strip()

    # convert persian digits
    persian_map = str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789")
    text = text.translate(persian_map)

    digits = re.findall(r"\d+", text)
    if not digits:
        return None

    return int("".join(digits))


def is_valid_product(href: str):
    if not href:
        return False

    return (
        "/product/" in href
        and "dkp-" in href
        and href.startswith("/product/")
    )


# ----------------------------
# main scraper
# ----------------------------
def scrape(query="ipad", limit=20):
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )

        page = browser.new_page()

        url = f"{BASE}/search/?q={query}"
        page.goto(url, wait_until="networkidle")

        # ----------------------------
        # scroll to load lazy items
        # ----------------------------
        for _ in range(6):
            page.mouse.wheel(0, 5000)
            page.wait_for_timeout(800)

        # ----------------------------
        # collect product cards
        # ----------------------------
        cards = page.locator('a[href*="/product/"]')

        seen = set()
        results = []

        count = cards.count()

        for i in range(count):
            href = cards.nth(i).get_attribute("href")

            if not is_valid_product(href):
                continue

            full_url = urljoin(BASE, href)

            if full_url in seen:
                continue
            seen.add(full_url)

            card = cards.nth(i)

            # ----------------------------
            # TITLE (robust fallback)
            # ----------------------------
            title = None
            try:
                title_el = card.locator("xpath=ancestor::*[1]//h3 | ancestor::*[1]//h2")
                if title_el.count() > 0:
                    title = title_el.first.inner_text().strip()
            except:
                pass

            if not title:
                title = "NO_TITLE"

            # ----------------------------
            # PRICE (Digikala real DOM)
            # ----------------------------
            price = None
            try:
                price_el = card.locator('[data-testid="price-final"]')
                if price_el.count() > 0:
                    raw_price = price_el.first.inner_text()
                    price = normalize_price(raw_price)
            except:
                price = None

            # ----------------------------
            # filter noise products (optional but useful)
            # ----------------------------
            if title != "NO_TITLE" and len(title) < 10:
                continue

            results.append({
                "title": title,
                "price": price,
                "url": full_url
            })

            print("OK:", title, price)

            if len(results) >= limit:
                break


        print("\nUNIQUE PRODUCTS (REAL):", len(seen))


        browser.close()

        return results


# ----------------------------
# run
# ----------------------------
if __name__ == "__main__":
    data = scrape("ipad", limit=15)


    print("\nFINAL RESULT:")
    for item in data:
        print(item)