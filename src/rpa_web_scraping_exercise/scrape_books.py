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
    #Primeira condição
    if max_books <= 0: return []

    #Criar lista de categorias
    page.goto(URL)
    Categories_List: dict = dict([[k[25:].replace("/index.html","").split("_")[0].replace("-"," "),k] for k in [k.get_attribute("href") for k in page.locator("div.side_categories").locator("a").all()][1:]])

    #Escolha de categoria e Segunda Condição
    try:
      if category: newURL = URL + Categories_List[category]
      else: newURL = URL + "catalogue/category/books_1/index.html"
    except KeyError: return []

    page.goto(newURL)

    #Montar lista de livros
    if page.locator("form.form-horizontal").locator("strong").count() == 1: 
       total: int = int(page.locator("form.form-horizontal").locator("strong").inner_text())
       total_page: int = total
    else: 
       total: int = [int(k.inner_text()) for k in page.locator("form.form-horizontal").locator("strong").all()][0]
       total_page: int = [int(k.inner_text()) for k in page.locator("form.form-horizontal").locator("strong").all()][2]

    newmax_books: int = max_books if total > max_books else total
    npages: int = newmax_books // total_page + (1 if newmax_books % total_page > 0 else 0)
    books: list[BookData] = []
    for k in range(npages):
      books += [{"url": "https://books.toscrape.com/catalogue/" + k.locator("a").get_attribute("href")[9:]} for k in page.locator("section").locator("h3").all()]
      if npages > 1 and k + 1 != npages: page.locator("ul.pager").locator("li.next").locator("a").click()
    
    #registrar o restante das informações
     
    ratings: dict = {"One": 1, "Two": 2, "Three": 3,"Four": 4, "Five": 5}

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