from pymongo import MongoClient
import json

mongourl = "mongodb://root:example@localhost:27018/"
client = MongoClient(mongourl)
db = client.AutoProducts
collection = db.AutoProducts

def add_new_item(product_id: str, name: str, unit_price :float, stock_quantity :int, description :str  ):
    x = {    "product_id"        : product_id 
         ,   "name"              : name
         ,   "unit_price"        : unit_price
         ,   "stock_quantity"    : stock_quantity 
         ,   "description"       : description  
        }
    
    y = collection.insert_one(x)
    
    print({"Message": y})


with open('auto_products.json', 'r', encoding="utf-8") as file:
    data = json.load(file)

#ys :list[AutoProduct] = [AutoProduct(**y) for y in data]
collection.delete_many({})

for y in data:
    x = {    "product_id"        : y["Product ID"] 
         ,   "name"              : y["Name"]
         ,   "unit_price"        : y["Unit Price"]
         ,   "stock_quantity"    : y["Stock Quantity"] 
         ,   "description"       : y["Description"]  
        }
    add_new_item(**x)
