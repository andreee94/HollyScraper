
import sqlite3

class DBManager:
    
    DB_filename = 'data/items.db'
    DBtable_items = "items"
    DBtable_prices = "prices"

    def __init__(self):
        pass

    def open(self):
        self.db = sqlite3.connect(DBManager.DB_filename)
        self.cursor = self.db.cursor()

    def createItemsTable(self):
        cur = self.getCursor()
        if cur == None:
            return
        cur.execute("CREATE TABLE if not exists " + DBManager.DBtable_items + "(id INTEGER PRIMARY KEY AUTOINCREMENT, PriceTable TEXT, Name TEXT, URL TEXT, ImageURL TEXT, ProductID INT, ProductIDSequence INT, Collection INT)") #, Price REAL, PriceCurrency TEXT, PriceOriginal REAL, PriceOriginalCurrency TEXT)")

    def createPriceItemTable(self, item):
        cur = self.getCursor()
        if cur == None:
            return
        table_name =  item.getPricesTableName()
        cur.execute("CREATE TABLE if not exists " + table_name + "(id INTEGER PRIMARY KEY AUTOINCREMENT, Data INT, Price REAL, PriceCurrency TEXT, PriceOriginal REAL, PriceOriginalCurrency TEXT)")

    def getItem(self, productID, sequence):
        cur = self.getCursor()
        if cur == None:
            return
        cur.execute("SELECT * FROM " + DBManager.DBtable_items + " WHERE ProductID=? AND ProductIDSequence=?", (productID, sequence))
        item = cur.fetchone()
        return item

    def addItem(self, item, commit=False):
        if self.db != None:
            cur = self.getCursor()
            cur.execute("insert into " + DBManager.DBtable_items + " (PriceTable, Name, URL, ImageURL, ProductID, ProductIDSequence, Collection) values (?, ?, ?, ?, ?, ?, ?)", item.getTuple())
            if commit:
                self.commit()

    def addPrice(self, item, commit=False):
        if self.db != None:
            cur = self.getCursor()
            self.createPriceItemTable(item)
            table_name =  item.getPricesTableName()
            cur.execute("insert into " + table_name + " (Data, Price, PriceCurrency, PriceOriginal, PriceOriginalCurrency) values (?, ?, ?, ?, ?)", item.getPriceTuple())
            if commit:
                self.commit()

    def close(self):
        if self.db != None: # and self.db.isopen
            self.db.close()
    
    def commit(self):
        if self.db != None:
            self.db.commit()

    def getCursor(self):
        if self.cursor == None:
            self.cursor = self.db.cursor()
        return self.cursor
