from contextlib import asynccontextmanager
from typing import List

from fastapi import Depends, FastAPI
from sqlmodel import Session, select

from database_setup import Item, create_db_and_tables, get_session


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/items/", response_model=Item)
def create_item(item: Item, session: Session = Depends(get_session)):
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@app.get("/items/", response_model=List[Item])
def read_items(session: Session = Depends(get_session)):
    return session.exec(select(Item)).all()
