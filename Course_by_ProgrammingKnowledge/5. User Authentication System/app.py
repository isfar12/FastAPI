from fastapi import FastAPI, HTTPException
from passlib.context import CryptContext
from contextlib import asynccontextmanager
from db import database, engine, metadata
from models import users
from schema import Register, Login

metadata.create_all(engine)

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: code before yield runs on startup
    await database.connect()
    yield
    # Shutdown: code after yield runs on shutdown
    await database.disconnect()


app = FastAPI(lifespan=lifespan)


@app.post("/register")
async def register(user: Register):
    query = users.select().where(users.c.username == user.username)
    existing_user = await database.fetch_one(query)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username Already Exists")
    
    query = users.insert().values(username=user.username,
                                  age=user.age, password=user.password)
    await database.execute(query)
    return {"message": "User registered successfully!"}

@app.post("/login")
async def login(user: Login):
    query = users.select().where(users.c.username == user.username)
    existing_user = await database.fetch_one(query)
    if not existing_user:
        raise HTTPException(status_code=400, detail="Invalid Username or Password")
    
    if existing_user.password != user.password:
        raise HTTPException(status_code=400, detail="Invalid Username or Password")
    
    return {"message": "Login successful!"}