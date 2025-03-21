from typing import Union

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pymongo import MongoClient
from fastapi import FastAPI
from pydantic import BaseModel
from bson import json_util
import json

app = FastAPI()

mongourl = "mongodb://root:example@localhost:27018/"
client = MongoClient(mongourl)
db = client.AutoProducts
collection = db.AutoProducts

'''
{
    "Product ID": "AUTO029",
    "Name": "Transmission Fluid",
    "Unit Price": 821.43,
    "Stock Quantity": 54,
    "Description": "High-quality Transmission Fluid designed for durability and performance."
  },
'''


class AutoProduct(BaseModel):
    product_id: int
    name: str
    unit_price: float
    stock_quantity: int 
    description: str

    def toString(self):
        s = "{ " + self.product_id + ", " + self.name + ", " + self.unit_price + ", " + self.stock_quantity + ", " + self.description + " }"
        return s


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/getSingleProduct/{item_id}")
def get_single_product(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/getAll")
def get_all_products():
    
    ys = collection.find({})
    x = json.loads(json_util.dumps(list(ys), indent=4))

    return x
 
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
def delete_one_item(product_id: str ):
    x = {    "product_id"        : product_id 
        }
    
    y = collection.delete_one(x)
    
    return {"Message": y}



@app.get("/startsWith/{query__all_startingwith}")
def starts_with(query__all_startingwith: str ):
    
    q = { "name": { "$regex": query__all_startingwith + "\\w+" }} 
    ys = collection.find(q)
    x = json.loads(json_util.dumps(list(ys), indent=4))

    return x

@app.get("/paginate/{page_number}")
def paginate(page_number :int ):
    
    y = collection.count_documents({})

    item_index_min = (page_number - 1) * 10
    x = y - item_index_min 
    item_index_max = (page_number) * 10 if x >= 10  else item_index_min + x

    start = item_index_min
    end = item_index_max
    
    q = {
        "$expr": {
            "$let": {
                "vars": {
                    "product_id_number_int": {
                        "$convert": {
                            "input": { "$substr": ["$product_id", 4, -1] },
                            "to": "int",
                            "onError": 0,
                            "onNull": 0
                        }
                    }
                },
                "in": {
                    "$and": [
                        { "$lte": ["$$product_id_number_int", end] },
                        { "$gte": ["$$product_id_number_int", start] }
                    ]
                }
            }
        }
    }
               
     
    ys = collection.find(q)
    
    x = json.loads(json_util.dumps(list(ys), indent=4))

    return x

@app.get("/convert/{product_id}")
def convert_dollar_to_euro(product_id :str ):

    x = collection.find_one({"product_id" : product_id })
    price = x["unit_price"]
    euro = price *  0.9234
    return euro
 

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
    

'''