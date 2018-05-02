
from item import Item
from dbmanager import DBManager


dbManager = DBManager()
dbManager.open()
dbManager.createItemsTable()

it = dbManager.getItem(11272912, 1)
for i in it:
    print(i)

dbManager.close()