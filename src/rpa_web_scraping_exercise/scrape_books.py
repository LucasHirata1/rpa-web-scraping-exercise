from decimal import Decimal
from typing import TypedDict

from playwright.sync_api import Page

URL: str = "https://books.toscrape.com/"

def change_url(complete:str):
   URL: str = "https://books.toscrape.com/" + complete

class BookData(TypedDict):
    url: str
    name: str
    rating: int
    price: Decimal
    in_stock: bool


def scrape_books(page: Page, *, category: str | None, max_books: int) -> list[BookData]:
    """Scrape book data from https://books.toscrape.com/.

    After navigating to the site homepage, scrapes book data following this
    contract:

    - `category` is `None`: scrape all books, following the pagination from
      the homepage without navigating into any category.
    - `category` matches a sidebar category (case-insensitive): scrape only
      that category's books, following its pagination.
    - `category` does not match any sidebar category (or is empty /
      whitespace-only): return an empty list.

    Stops as soon as `max_books` books have been collected and never request
    pages beyond the limit. If `max_books` is less than or equal to zero, an
    empty list is returned.

    Args:
        page: A Playwright page, already created and navigable.
        category: The category to scrape, or `None` to scrape all books.
        max_books: Maximum number of books to scrape.

    Returns:
        A list of the scraped books.
    """
    #Primeira condição
    if max_books <= 0: return []

    #Criar lista de categorias
    page.goto(URL)
    Categories_List = dict([[k[25:].replace("/index.html","").split("_")[0].replace("-"," "),k] for k in [k.get_attribute("href") for k in page.locator("div.side_categories").locator("a").all()][1:]])

    #Escolha de categoria e Segunda Condição
    try:
      if category: newURL = URL + Categories_List[category]
      else: newURL = URL + "catalogue/category/books_1/index.html"
    except KeyError: return []

    page.goto(newURL)

    #Montar lista de livros
    total,total_page = [int(k.inner_text()) for k in page.locator("form.form-horizontal").locator("strong").all()][::2]
    newmax_books = max_books if total > max_books else total
    npages = newmax_books // total_page + 1
    books = []
    for k in range(npages):
      books += [{"url": "https://books.toscrape.com/catalogue/" + k.locator("a").get_attribute("href")[9:]} for k in page.locator("section").locator("h3").all()]
      if npages > 1 and k + 1 != npages: page.locator("ul.pager").locator("li.next").locator("a").click()
    
    #registrar o restante das informações
     
    ratings = {"One": 1, "Two": 2, "Three": 3,"Four": 4, "Five": 5}

    for i,k in enumerate(books[:newmax_books]):
       page.goto(k["url"])
       book: BookData = {
           "url":       k["url"],
           "name":      page.locator("div.col-sm-6.product_main").locator("h1").inner_text(),
           "rating":    ratings[page.locator("div.col-sm-6.product_main").locator("p").last.get_attribute("class")[12:]],
           "price":     Decimal(page.locator("div.col-sm-6.product_main").locator("p.price_color").inner_text()[1:]),
           "in_stock":  page.locator("div.col-sm-6.product_main").locator("p.instock.availability").inner_text()[:11] == " In stock ("}
       books[i] = book

    return books[:newmax_books]

#awd = ["catalogue/category/books_1/index.html","catalogue/category/books/mystery_3/index.html","catalogue/category/books/religion_12/index.html"]
#aa = dict([[k[25:].replace("/index.html","").split("_")[0],k] for k in awd[1:]])
#for k in 

#for k in range(2):print(k)
#https://books.toscrape.com/catalogue/sharp-objects_997/index.html

