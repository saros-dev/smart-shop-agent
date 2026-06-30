from fastapi import APIRouter
from app.scraper.digikala import search_products

router = APIRouter()

@router.get("/search")
def search(q: str):

    title = search_products(q)

    return {
        "page_title": title
    }
