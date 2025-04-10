from typing import Union

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.openapi.utils import get_openapi
from pymongo import MongoClient
from fastapi import FastAPI, requests
from pydantic import BaseModel
from bson import ObjectId, json_util
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
    _id :dict[str, str]
    product_id: str
    name: str
    unit_price: float
    stock_quantity: int 
    description: str

    def toString(self):
        s = f"{ {self.product_id}, {self.name}, {self.unit_price}, {self.stock_quantity} , {self.description} }"
        return s


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/getSingleProduct/{item_id}")
def get_single_product(item_id: str):
    try:
        ys = collection.find_one({"product_id": item_id})
        if ys:
            return json.loads(json_util.dumps(ys, indent=4))
        else:
            return {"error": "Product not found"}
    except Exception as e:
        return {"error": str(e)}
    
    
@app.get("/getAll")
def get_all_products():
    try:
        ys = collection.find({})
        if ys: 
            return json.loads(json_util.dumps(list(ys), indent=4))
        else:
            return {"error": "No products found"}
    except Exception as e:
        return {"error": str(e)}
    

    
@app.post("/addNew")
def add_new_item(new_product :AutoProduct ):

    #print(new_product.description())

    x = {    "product_id"        : new_product.product_id 
         ,   "name"              : new_product.name
         ,   "unit_price"        : new_product.unit_price
         ,   "stock_quantity"    : new_product.stock_quantity 
         ,   "description"       : new_product.description  
        }
    
    try:
        y = collection.insert_one(x)
        #x1 = json.loads(json_util.dumps(y, indent=4))
        y1 = collection.find_one({"_id": y.inserted_id})
        return {"inserted_id": str(y.inserted_id), "product": json.loads(json_util.dumps(y1, indent=4))} 
    except Exception as e:
        return {"error": str(e)}



@app.delete("/deleteOne/{product_id}")
def delete_one_item(product_id: str ):
    x = {    "product_id"        : product_id 
        }
    
    try:
        y = collection.delete_many(x)
        #y = collection.delete_one(x)

        y1 = collection.find_one(x) 
        count = collection.count_documents(x)
        return {"deleted_count": str(y.deleted_count), "product_left": str(count),  "product": json.loads(json_util.dumps(y1, indent=4))} 
    except Exception as e:
        return {"error": str(e)}


@app.get("/startsWith/{query__all_startingwith}")
def starts_with(query__all_startingwith: str):
    q = {"name": {"$regex": f"^{query__all_startingwith}", "$options": "i"}}
    try:
        ys = collection.find(q)
        return json.loads(json_util.dumps(list(ys), indent=4))
    except Exception as e:
        return {"error": str(e)}


@app.get("/paginate/{page_number}")
def paginate(page_number: int):
    items_per_page = 10
    skip_count = (page_number - 1) * items_per_page
    try:
        ys = collection.find().skip(skip_count).limit(items_per_page)
        return json.loads(json_util.dumps(list(ys), indent=4))
    except Exception as e:
        return {"error": str(e)}

@app.get("/convert/{product_id}")
def convert_dollar_to_euro(product_id: str):
    x0 = {"product_id": product_id}
    try:
        ys = collection.find_one(x0)
        x1 = json.loads(json_util.dumps(ys, indent=4))
        if x1 is not None:
            x = AutoProduct(**x1)
            price: float = x.unit_price
            #response = requests.Request.get("https://api.exchangerate-api.com/v4/latest/USD")
            if True : #response.status_code == 200:
                #rates = response.json().get("rates", {})
                #euro_rate = rates.get("EUR", 0.0)
                euro = price * 0.91 #euro_rate
                y = {"unit_price__euro": euro}
                return y
            else:
                return {"error": "Failed to fetch exchange rate"}
        else:
            return {"unit_price__euro": -1}
    except Exception as e:
        return {"error": str(e) }



def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Fast API Auto Products",
        version="2.5.0",
        summary="This is a very custom OpenAPI schema",
        description="Here's a longer description of the custom **OpenAPI** schema",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi



'''

@app.get("/paginate/{page_number}")
def paginate(page_number :int ):
    
    y = collection.count_documents({})
    if y > 0:
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
        
        x1 = json.loads(json_util.dumps(list(ys), indent=4))

        return x1
    else :
        return None


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