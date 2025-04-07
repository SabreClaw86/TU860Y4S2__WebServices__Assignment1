from fastapi import Response
from fastapi.testclient import TestClient
#from cryptography.fernet import Fernet

from httpx import AsyncClient
import pytest
from main import AutoProduct, app  # Import your FastAPI app

client = TestClient(app)

baseurl = "http://localhost:8000"
#s = xmlrpc.client.ServerProxy('http://localhost:8000')

@pytest.mark.asyncio
async def test_get_all_products():
    x1 = AsyncClient(base_url=baseurl)
    async with x1 as ac:
        response = await ac.get("getAll")
        # "_id":{"$oid":"67dd8619508a15168ef3051b"},
        # "product_id":"AUTO001","name":"Starter Motor",
        # "unit_price":243.69,
        # "stock_quantity":50,
        # "description" : ""
        shouldHaveTheseKeys :set = { "_id", "product_id", "name", "unit_price", "stock_quantity", "description" }
        result :list[dict] = response.json()
        #print(result)
        keys1 = [( set(x.keys()) == set(shouldHaveTheseKeys)) for x in result]


        #print(response)
        assert response.status_code == 200
        assert response.json()  # Add more assertions based on your expected output
        assert all(keys1)


@pytest.mark.asyncio
async def test_get_a_single_product():
    x1 = AsyncClient(base_url=baseurl)
    async with x1 as ac:
        product_id1 = "AUTO001"
        response = await ac.get("getSingleProduct/" + product_id1)
        result :dict = response.json()
        print(result)

        shouldHaveTheseKeys :set = { "_id", "product_id", "name", "unit_price", "stock_quantity", "description" }
        #print(result)
        keys1 = ( set(result.keys()) == set(shouldHaveTheseKeys))


        #print(response)
        assert response.status_code == 200
        assert response.json()  # Add more assertions based on your expected output
        assert keys1

@pytest.mark.asyncio
async def test_add_new_product():
    x1 = AsyncClient(base_url=baseurl)
    async with x1 as ac:
        x = {   "product_id"        :   "AUTO1010"
            ,   "name"              :   "test1"
            ,   "unit_price"        :   0.00
            ,   "stock_quantity"    :   9999 
            ,   "description"       :   "Testing..."  
            }
        response = await ac.post("addNew", json=x)
        result = response.json()
        print(result)
        #has_inserted_id = result['inserted_id'] is str

        
        shouldHaveTheseKeys :set = { "_id", "product_id", "name", "unit_price", "stock_quantity", "description" }
        #print(result)
        keys1 = ( set(result['product'].keys()) == set(shouldHaveTheseKeys))



        print(response.json())
        assert response.status_code == 200
        assert response.json()  # Add more assertions based on your expected output
        assert keys1

@pytest.mark.asyncio
async def test_delete_one_product():
    x1 = AsyncClient(base_url=baseurl)
    async with x1 as ac:
        x1 = {   "product_id"        :   "AUTO1010"
            ,   "name"              :   "test1"
            ,   "unit_price"        :   0.00
            ,   "stock_quantity"    :   9999 
            ,   "description"       :   "Testing..."  
            }
        response1 = await ac.post("addNew", json=x1)
        result1 = response1.json()
        
        
        x2 = "AUTO1010"
        response2 = await ac.delete("deleteOne/" + (x2))
        result2 = response2.json()
        
        shouldHaveTheseKeys :set = { "_id", "product_id", "name", "unit_price", "stock_quantity", "description" }
        #print(result)
        deleted1 = int(result2["deleted_count"]) > 0 and result2["product"] is None and int(result2["product_left"]) == 0
        #print(result2)
        #keys1 = ( set(result['product'].keys()) == set(shouldHaveTheseKeys))

        
        #print(response)
        
        assert response1.status_code == 200
        assert response1.json()
        assert response2.status_code == 200
        assert response2.json()  # Add more assertions based on your expected output
        print(result2)
        print(deleted1)
        assert deleted1


@pytest.mark.asyncio
async def test_products_that_start_with():
    x1 = AsyncClient(base_url=baseurl)
    async with x1 as ac:
        x = "P"
        response = await ac.get("startsWith/" + str(x))
        result :list[dict] = response.json()

        shouldHaveTheseKeys :set = { "_id", "product_id", "name", "unit_price", "stock_quantity", "description" }
        keys1 = [( set( r.keys()) == set(shouldHaveTheseKeys)) for r in result ]
        
        product_names = sorted([r.get("name", "") for r in result])
        #product_names :list[str] = sorted([ r["name"] for r in result ])
        
        z = lambda x1 : (x1.find(x) == 0 and x1[ x1.find(x) : len(x)] == x )
        product_names__valid = [ z(r) for r in product_names ]

        #print(response)
        assert response.status_code == 200
        assert response.json()  # Add more assertions based on your expected output
        assert all(keys1) and all(product_names__valid)


@pytest.mark.asyncio
async def test_paginate_from_a_selection_of_products():
    x1 = AsyncClient(base_url=baseurl)
    async with x1 as ac:
        x = 1
        response = await ac.get("paginate/" + str(x))
        result :list[dict] = response.json()
        print(result)

        shouldHaveTheseKeys :set = { "_id", "product_id", "name", "unit_price", "stock_quantity", "description" }
        product_ids :list[str] = sorted([ r["product_id"] for r in result ])
        product_ids__valid = [ r[:4] == "AUTO" and int(r[4:]) >= 0  for r in product_ids ] 
        valid_ordering = True
        if all(product_ids__valid):
            product_ids__numbers = sorted([ int(r[4:])  for r in product_ids ])
            ordered = True
            contigious = True
            last = None
            for p in product_ids__numbers: 
                if last is None:
                    last = p
                else :
                    if p - last != 1 : 
                        contigious = False
                    if not (p > last) :
                        ordered = False 
                    last = p
            valid_ordering = ordered #and contigious

        
        keys1 = [( set( r.keys()) == set(shouldHaveTheseKeys)) for r in result ]
        #print(response)
        assert response.status_code == 200
        assert response.json()  # Add more assertions based on your expected output
        assert all(keys1) and all(product_ids__valid) and valid_ordering



@pytest.mark.asyncio
async def test_product_unit_price_currency_conversion():
    x1 = AsyncClient(base_url=baseurl)
    async with x1 as ac:
        #x = { "product_id" : "AUTO001"}
        product_id1 = "AUTO001"
        response1 = await ac.get("getSingleProduct/" + product_id1)
        #response : Response = await ac.post("get", data=x)
        result1 = response1.json()

        #price1 = result1["unit_price"]

        response2 = await ac.get("convert/" + product_id1)
        result2  :float = response2.json()
        
        print("result2: \n\t" + str(result2))
        print("result1: \n\t" + str(result1))
        sucessful_conversion = result1["unit_price"] *  0.91  == result2["unit_price__euro"]
        # 0.9234
        assert (sucessful_conversion)
        #print(response)
        assert response1.status_code == 200
        assert response1.json()  # Add more assertions based on your expected output
        assert response2.status_code == 200
        assert response2.json()  # Add more assertions based on your expected output


'''
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