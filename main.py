""" Main file """
import json

import redis
import requests
from fastapi import FastAPI

app = FastAPI()
redis_client = redis.Redis(
    host='localhost',
    port=6379,
    db=0
)

@app.get("/")
def read_root():
    """
    root callback
    """
    return "Hello World!!"

@app.get("/products")
def get_all_products():
    """
    Function to call API and get all products details. Data limited to 5 results.
    """
    req = requests.get("https://fakestoreapi.com/products?limit=5", timeout=500)
    return req.json()

@app.get("/products/{num_product}")
def get_specific_product(num_product: int):
    """
    Function to call API and get specific product details.
    """
    data = redis_client.get(num_product)
    if not data:
        data = requests.get(f"https://fakestoreapi.com/products/{num_product}", timeout=500)
        redis_client.set(num_product, data.text)
    return json.loads(data)
