from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# 1. Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # разрешает запросы со всех сайтов
    allow_credentials=True,
    allow_methods=["*"],  # разрешает все методы (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # разрешает любые заголовки
)


# Модель данных для карточки товара
class Product(BaseModel):
    id: int
    name: str
    description: str
    image: str
    price: int
    details: str = ""


# Тестовый список товаров
products_db = [
    {
        "id": 1,
        "name": "Черная футболка",
        "description": "Стильная футболка в минималистичном дизайне.",
        "image": "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?auto=format&fit=crop&w=800&q=60",
        "price": 250,
        "details": "Сделана из 100% хлопка. Удобна для ношения в любой сезон. Проверенное качество."
    },
    {
        "id": 2,
        "name": "Белая футболка",
        "description": "Легкая и удобная футболка для повседневной носки.",
        "image": "https://images.unsplash.com/photo-1520975437132-68c902d30f3f?auto=format&fit=crop&w=800&q=60",
        "price": 250,
        "details": "Универсальный белый цвет подходит ко всему. Приятная на ощупь ткань. Носится долго."
    },
]


@app.get("/")
def read_root():
    return {"status": "ok", "message": "FastAPI сервер работает!"}


class ProductCreate(BaseModel):
    name: str
    description: str
    image: str
    price: int
    details: str = ""

@app.get("/products/")
def get_products():
    # Отправляем список напрямую (подходит для res.data на фронтенде)
    return products_db

@app.get("/products/{product_id}/")
def get_product(product_id: int):
    for product in products_db:
        if product["id"] == product_id:
            return product
    raise HTTPException(status_code=404, detail="Product not found")

@app.post("/products/")
def create_product(item: ProductCreate):
    next_id = max((product["id"] for product in products_db), default=0) + 1
    new_product = {
        "id": next_id,
        "name": item.name,
        "description": item.description,
        "image": item.image,
        "price": item.price,
        "details": item.details,
    }
    products_db.insert(0, new_product)
    return new_product

@app.delete("/products/{product_id}/")
def delete_product(product_id: int):
    global products_db
    for i, product in enumerate(products_db):
        if product["id"] == product_id:
            products_db.pop(i)
            return {"status": "deleted", "id": product_id}
    raise HTTPException(status_code=404, detail="Product not found")