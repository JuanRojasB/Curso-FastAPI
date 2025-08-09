from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="Mi API - Semana 2")

# Modelo Pydantic
class Product(BaseModel):
    name: str
    price: float
    description: Optional[str] = None

# Base de datos temporal
products_db: list[dict] = []

# Endpoint raíz
@app.get("/", response_model=dict)
def home() -> dict:
    return {"message": "API Semana 2 funcionando"}

# POST: Crear producto
@app.post("/products", response_model=dict)
def create_product(product: Product) -> dict:
    new_product = product.dict()
    new_product["id"] = len(products_db) + 1
    products_db.append(new_product)
    return {"message": "Producto creado con éxito", "product": new_product}

# GET: Listar todos los productos
@app.get("/products", response_model=list[dict])
def get_products() -> list[dict]:
    return products_db

# GET: Obtener producto por ID
@app.get("/products/{product_id}", response_model=dict)
def get_product(product_id: int) -> dict:
    for product in products_db:
        if product["id"] == product_id:
            return product
    return {"error": "Producto no encontrado"}

    