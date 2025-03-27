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
        response = await ac.post("addNew", data=x)
        result = response.json()
        print(result)
        has_inserted_id = result['inserted_id'] is str

        print(response.json())
        assert response.status_code == 200
        assert response.json()  # Add more assertions based on your expected output
        assert has_inserted_id

@pytest.mark.asyncio
async def test_delete_one_product():
    x1 = AsyncClient(base_url=baseurl)
    async with x1 as ac:
        response = await ac.get("deleteOne")
        #print(response)
        assert response.status_code == 200
        assert response.json()  # Add more assertions based on your expected output


@pytest.mark.asyncio
async def test_products_that_start_with():
    x1 = AsyncClient(base_url=baseurl)
    async with x1 as ac:
        response = await ac.get("startsWith")
        #print(response)
        assert response.status_code == 200
        assert response.json()  # Add more assertions based on your expected output


@pytest.mark.asyncio
async def test_paginate_from_a_selection_of_products():
    x1 = AsyncClient(base_url=baseurl)
    async with x1 as ac:
        response = await ac.get("paginate")
        #print(response)
        assert response.status_code == 200
        assert response.json()  # Add more assertions based on your expected output



@pytest.mark.asyncio
async def test_product_unit_price_currency_conversion():
    x1 = AsyncClient(base_url=baseurl)
    async with x1 as ac:
        response = await ac.get("convert")
        #print(response)
        assert response.status_code == 200
        assert response.json()  # Add more assertions based on your expected output


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