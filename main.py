from fastapi import FastAPI
from database.models import User, Product, Category, Cart, Brand, Favorite
from database import engine, Base
from api.users.user_api import user_router
app = FastAPI(docs_url='/')
app.include_router(user_router, prefix='/user')
Base.metadata.create_all(bind=engine)