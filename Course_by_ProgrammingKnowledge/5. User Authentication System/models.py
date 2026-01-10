from sqlalchemy import create_engine, Table, Column, Integer, String
from db import metadata

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("username", String(50), unique=True, nullable=False, index=True),
    Column("age", Integer, nullable=False),
    Column("password", String(), nullable=False)
)
