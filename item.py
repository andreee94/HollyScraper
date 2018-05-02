
from dbmanager import DBManager
from datetime import datetime

class Item:

    mainURL = "https://www.hollisterco.com"

    def __init__(self, name=None, prices=None, imageURL=None, URL=None, color=None, sizes=None, productID=None, productIDSequence=None, collection=None):
        self.name = name
        self.prices = prices
        #self.originalPrice = originalPrice
        self.imageURL = imageURL
        self.URL = URL
        self.color = color
        self.sizes = sizes
        self.productID = productID
        self.productIDSequence = productIDSequence
        self.collection = collection

    # load item from the main page
    # not all info are available
    @classmethod
    def fromPreviewPage(self, card):
        it = Item()
        metaName = card.find("meta", itemprop="name", content=True)
        metaImage = card.find("meta", itemprop="image", content=True)
        metaPrices = card.find_all("meta", itemprop="price", content=True)
        metaPriceCurrecies = card.find_all("meta", itemprop="priceCurrency", content=True)
        aName = card.find("a", class_="product-card__name")

        it.name = it.__safeGet(metaName, "content")# metaName["content"]
        it.URL = it.__safeGet(aName, "href")#aName["href"]
        if not it.URL.startswith("https"):
            it.URL = Item.mainURL + it.URL
        it.imageURL = it.__safeGet(metaImage, u"content")
        priceSale = PriceSingle(it.__safeGet(metaPrices, u"content", index=0), it.__safeGet(metaPriceCurrecies, u"content", index=0))
        originalPrice = PriceSingle(it.__safeGet(metaPrices, u"content", index=1), it.__safeGet(metaPriceCurrecies, u"content", index=1))
        it.prices = [Price(priceSale, originalPrice)]
        it.color = None
        it.sizes = None
        it.productID = it.__safeGet(card, u"data-productid", isInt=True)
        it.productIDSequence = it.__safeGet(card, u"data-seq", isInt=True)
        it.collection = it.__safeGet(card, u"data-collection", isInt=True)
        return it

    # TODO must be implemented
    @classmethod
    def getPricesFromItemPage(self, content):
        # main div component
        container = content.find("div", class_="product-price-v2__inner")
        # should have 2 occurrence each
        metaPrices = card.find_all("meta", itemprop="price", content=True)
        metaPriceCurrecies = card.find_all("meta", itemprop="priceCurrency", content=True)
        # create price instances from html content
        price = Price(self.__safeGet(metaPrices, u"content", index=0), self.__safeGet(metaPriceCurrecies, u"content", index=0))
        originalPrice = Price(self.__safeGet(metaPrices, u"content", index=1), self.__safeGet(metaPriceCurrecies, u"content", index=1))
        return price, originalPrice

    # since data is generated at runtime I think,
    # this method cannot get just available sizes but all of them 
    def addSizes(self, content):
        sizesContaner = content.find("ul", "product-sizes")
        sizesContaner = sizesContaner.find_all("li")# , "product-attrs__attr")
        for s in sizesContaner:
            sizeValue = s.find("input")["value"]
            print(sizeValue)


    @classmethod
    def __safeGet(self, obj, field, index=None, isInt=False):
        if index == None:
            if obj != None and field != None and obj.has_attr(field):
                if isInt:
                    return int(obj[field])
                else: return obj[field]
        else:
            if obj != None and field != None:
                if len(obj) > index:
                    if isInt:
                        return int(obj[index][field])
                    else: return obj[index][field]
        #return None
        
    def getPricesTableName(self):
        return DBManager.DBtable_items + str(self.productID) + '_' + str(self.productIDSequence)

    def getTuple(self):
        return (self.getPricesTableName(), self.name, self.URL, self.imageURL, self.productID, self.productIDSequence, self.collection)
    
    def getPriceTuple(self, index):
        # tuples concatenation  
        return self.prices.getTuple()

    def __str__(self):
        return str(self.name) + ": " + self.URL #str(self.prices)# + " | " + str(self.originalPrice)

    def fromTuple(t):
        it = Item()
        # TODO it.name = 

class PriceSingle:
    def __init__(self, value, currency):
        self.value = value
        self.currency = currency
        
    def getTuple(self):
        return (self.value, self.currency)
        
    def __str__(self):
        return str(self.value) + " " + self.currency

class Price:

    # price and priceOriginal must be PriceSingle instances
    def __init__(self, priceSale, priceOriginal, date=None):
        # date = None means now
        self.priceSale = priceSale
        self.priceOriginal = priceOriginal
        if date != None:
            self.date = date
        else: self.date = int(datetime.now().strftime('%s'))

    def getTuple(self):
        return (self.date, ) + self.priceSale.getTuple() + self.priceOriginal.getTuple()

    def __str__(self):
        return str(self.priceSale) + " || " + str(self.priceOriginal)