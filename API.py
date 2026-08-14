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


# Тестовый список товаров
products_db = [
    {
        "id": 1,
        "name": "Черная футболка",
        "description": "Сочная пицца с томатами и сыром",
        "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQkg61qOl9IfvCc4Q8-jwWkCIHPzyj8IWCB4dP47c8pzA&s=10",
        "price": 250
    },
    {
        "id": 2,
        "name": "Белая футболка",
        "description": "Освежающий напиток 0.5л",
        "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTNdsm2KVJ6dUBq_E1_TY9fV_lovoZX1knJwV1N_X0mFA&s=10",
        "price": 250
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
    }
    products_db.insert(0, new_product)
    return new_product