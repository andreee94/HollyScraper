



class Item:

    mainURL = "https://www.hollisterco.com"

    def __init__(self, name=None, price=None, imageURL=None, URL=None, originalPrice=None, color=None, sizes=None, productID=None, productIDSequence=None, collection=None):
        self.name = name
        self.price = price
        self.originalPrice = originalPrice
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
        it.price = Price(it.__safeGet(metaPrices, u"content", index=0), it.__safeGet(metaPriceCurrecies, u"content", index=0))
        it.originalPrice = Price(it.__safeGet(metaPrices, u"content", index=1), it.__safeGet(metaPriceCurrecies, u"content", index=1))
        it.color = None
        it.sizes = None
        it.productID = it.__safeGet(card, u"data-productid")
        it.productIDSequence = it.__safeGet(card, u"data-seq")
        it.collection = it.__safeGet(card, u"data-collection")
        return it

    def addSizes(self, content):
        sizesContaner = content.find("ul", "product-sizes")
        sizesContaner = sizesContaner.find_all("li")# , "product-attrs__attr")
        for s in sizesContaner:
            sizeValue = s.find("input")["value"]
            print(sizeValue)



    @classmethod
    def __safeGet(self, obj, field, index=None):
        if index == None:
            if obj != None and field != None and obj.has_attr(field):
                return obj[field]
        else:
            if obj != None and field != None:
                if len(obj) > index:
                    return obj[index][field]
        #return None
        
    def __str__(self):
        return str(self.price) + " | " + str(self.originalPrice)


class Price:

    def __init__(self, value, currency):
        self.value = value
        self.currency = currency

    def __str__(self):
        return str(self.value) + " " + self.currency