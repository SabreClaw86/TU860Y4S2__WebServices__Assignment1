from typing import Union

from pymongo import MongoClient
from fastapi import FastAPI

app = FastAPI()

mongourl = "mongodb://root:example@localhost:27018/"
client = MongoClient(mongourl)
db = client.AutoProducts
collection = db.AutoProducts

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/getSingleProduct/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/getAll")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/addNew")
def add_new_item(product_id: str, name: str, unit_price :float, stock_quantity :int, description :str  ):
    x = {    "product_id"        : product_id 
         ,   "name"              : name
         ,   "unit_price"        : unit_price
         ,   "stock_quantity"    : stock_quantity 
         ,   "description"       : description  
        }
    
    y = collection.insert_one(x)
    
    return {"Message": y}

@app.get("/deleteOne")
def add_new_item(product_id: str ):
    x = {    "product_id"        : product_id 
        }
    
    y = collection.delete_one(x)
    
    return {"Message": y}



@app.get("/startsWith")
def starts_with(query__all_startingwith: str ):
    
    q = { "name": { "$regex": query__all_startingwith + "\w+" }} 
    y = collection.find(q)
    
    return {"Message": y}

@app.get("/paginate/{page_number}")
def starts_with(product_id_start: str, product_id_end :str ):
    
    start = int(product_id_start.removeprefix("AUTO"))
    end = int(product_id_end.removeprefix("AUTO"))
    
    q = {
            "$exp" : {
                "$let" : {
                    "vars" : { 
                        "product_id_number_int" : 
                            "{ $convert: "
                                "{ input: "
                                    "\"$ltrim(this.product_id, \"AUTO\")\", "
                                    "to: \"int\" "
                                "}"
                            " }"
                    } 
                },
                "in" : {
                    "$and" : {
                        "$lte" : ["product_id_number_int", end],
                        "$gte" : ["product_id_number_int", start]
                    }
                }
            }
        }
               
     
    y = collection.find(q)
    
    return {"Message": y}

'''
 {
    "Product ID": "AUTO029",
    "Name": "Transmission Fluid",
    "Unit Price": 821.43,
    "Stock Quantity": 54,
    "Description": "High-quality Transmission Fluid designed for durability and performance."
  },

 The API should have the following endpoints:
• /getSingleProduct - This allows you to pass a single ID number into 
the endpoint and return the details of the single product in JSON 
format.
• /getAll - This endpoint should return all inventory in JSON format.
• /addNew - This endpoint should take in all 5 attributes of a new item 
and insert them into the database.
• /deleteOne - This endpoint should delete a product by the provided ID.
• /startsWith - This should allow the user to pass a letter to the URL, 
such as s, and return all products that start with s.
• /paginate - This URL should pass in a product ID to start from and a 
product ID to end from. The products should be returned in a batch of 
10.
• /convert - All of the prices are currently in dollars in the sample data. 
Implement a URL titled /convert which takes in the ID number of a 
product and returns the price in euro. An online API should be used to 
get the current exchange rate.

'''