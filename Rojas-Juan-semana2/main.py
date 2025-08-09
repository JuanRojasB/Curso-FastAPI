from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI(title="My API with Pydantic")

# Modelo Pydantic básico
class Product(BaseModel):
    name: str
    price: int  # en centavos para evitar decimales
    available: bool = True  # valor por defecto

# Response Models
class ProductResponse(BaseModel):
    id: int
    name: str
    price: int
    available: bool
    message: str = "Successful operation"

class ProductListResponse(BaseModel):
    products: List[dict]
    total: int
    message: str = "List retrieved"

# Lista temporal de productos
products: list[dict] = []

# Endpoint raíz
@app.get("/", response_model=dict)
def hello_world() -> dict:
    return {"message": "API with Pydantic!"}

# POST: Crear producto con validación automática
@app.post("/products", response_model=ProductResponse)
def create_product(product: Product) -> ProductResponse:
    product_dict = product.dict()
    product_dict["id"] = len(products) + 1
    products.append(product_dict)
    return ProductResponse(**product_dict, message="Product created successfully")

# GET: Listar todos los productos
@app.get("/products", response_model=ProductListResponse)
def get_products() -> ProductListResponse:
    return ProductListResponse(products=products, total=len(products))

# GET: Obtener producto por ID (parámetro de ruta)
@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int) -> ProductResponse:
    for product in products:
        if product["id"] == product_id:
            return ProductResponse(**product, message="Product retrieved successfully")
    raise HTTPException(status_code=404, detail="Product not found")

# GET: Obtener producto por categoría e ID (múltiples parámetros de ruta)
@app.get("/categories/{category}/products/{product_id}")
def product_by_category(category: str, product_id: int) -> dict:
    return {
        "category": category,
        "product_id": product_id,
        "message": f"Searching product {product_id} in category {category}"
    }

# GET: Búsqueda de productos con parámetros de query
@app.get("/search")
def search_products(
    name: Optional[str] = None,
    max_price: Optional[int] = None,
    available: Optional[bool] = None
) -> dict:
    results = products.copy()

    if name:
        results = [p for p in results if name.lower() in p["name"].lower()]
    if max_price:
        results = [p for p in results if p["price"] <= max_price]
    if available is not None:
        results = [p for p in results if p["available"] == available]

    return {"results": results, "total": len(results)}

# Modelo Pydantic más completo (opcional)
class CompleteUser(BaseModel):
    name: str
    age: int
    email: str
    phone: Optional[str] = None
    active: bool = True

# POST: Crear usuario con validación automática
@app.post("/users", response_model=dict)
def create_user(user: CompleteUser) -> dict:
    return {"user": user.dict(), "valid": True}
