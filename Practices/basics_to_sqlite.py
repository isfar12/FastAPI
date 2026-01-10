from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlmodel import SQLModel, Field, Session, select
from pydantic import BaseModel
from typing import Optional
from contextlib import asynccontextmanager

# DEFINE DATABASE SCHEMA


class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    price: float
    ratings: Optional[float] = None

# DEFINE LIFESPAN EVENT HANDLER THAT WILL TRIGGER WHEN THE APP STARTS


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

# DEFINE Pydantic MODEL FOR DATA VALIDATION and How data will be returned to the user


class ProductCreate(BaseModel):
    name: str
    price: float


DATABASE_URL = "sqlite:///./products.db"

# CREATE DATABASE ENGINE
engine = create_engine(DATABASE_URL, echo=True)

# BIND APP WITH LIFESPAN EVENT HANDLER
app = FastAPI(lifespan=lifespan)

# DEFINE ENDPOINTS


@app.post("/products/")
async def create_product(product: Product):
    with Session(engine) as session:
        session.add(product)
        session.commit()
        session.refresh(product)

        return product


@app.get("/all-products/", response_model=list[ProductCreate])
async def get_all_products():
    with Session(engine) as session:
        products = session.exec(select(Product)).all()
        return products
