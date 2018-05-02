import cfscrape
from bs4 import BeautifulSoup
from item import Item
from dbmanager import DBManager

mainURL = "https://www.hollisterco.com/"
salesURL = "https://www.hollisterco.com/shop/eu-it/lui-saldi"

scraper = cfscrape.create_scraper()  # returns a CloudflareScraper instance
# Or: scraper = cfscrape.CloudflareScraper()  # CloudflareScraper inherits from requests.Session
# print(scraper.get(salesURL).content)  # => "<!DOCTYPE html><html><head>..."

content = scraper.get(salesURL).content

soup = BeautifulSoup(content,  'html.parser')

container = soup.find("ul", class_='product-grid__products')

cards = container.find_all("li", class_="product-card")

dbManager = DBManager()
dbManager.open()
dbManager.createItemsTable()

for i, card in enumerate(cards):
    if i > 20:
        break

    it = Item.fromPreviewPage(card)
    print(it.name)
    print(it.URL)
    dbManager.addItem(it)
    dbManager.addPrice(it)
    #content_inner = scraper.get(it.URL).content
    #soup_inner = BeautifulSoup(content_inner,  'html.parser')
    #it.addSizes(soup_inner)

    #name = card.find("a", class_="product-card__name").get_text()
    #print(name.strip())

dbManager.commit()
dbManager.close()
#for c in container:
#    if c != None:
#        for cc in c:
#
#            print("-------------------------------------------")
#            print(c)
#print(list(soup.children))

#primary-content > div.product-grid__col--major > div > ul.product-grid__products.category-product-wrap.whiteoutarea