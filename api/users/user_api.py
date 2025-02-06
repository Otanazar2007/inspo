import shutil
import uuid
from typing import Optional
from fastapi import APIRouter, Request, Form, File, UploadFile
from pydantic import BaseModel, constr
import re
from database.userservice import (registration_db, login_db, change_account_db, delete_account_db,
                                  add_to_favorite, add_to_cart, del_from_cart, del_from_fav,
                                  get_exact_prod_by_brand, get_exact_prod_by_cat, get_prod_main_menu)
from database.adminservice import (get_exact_user, get_exact_category, get_exact_brand,
                                   get_exact_product, new_brand, new_category, new_product)

# (right - get_exact_user,new_brand, new_category, new_product, registration_db,
 # login_db, delete_account_db, get_exact_product, get_exact_category, get_exact_brand, get_exact_category, get_exact_brand, get_exact_product,
# add_to_favorite, add_to_cart, del_from_cart, del_from_fav, get_prod_main_menu

# in (process - ,get_exact_prod_by_brand, get_exact_prod_by_cat

user_router = APIRouter()
email_check = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
phone_number_check = re.compile(r'^\+998(33|90|97|94)\d{7}$')
def mail_checker(email, phone_number):
    if re.fullmatch(email_check, email) and re.fullmatch(phone_number_check, phone_number):
        return True
    return False

class RegistrationModel(BaseModel):
    username:str
    phone_number:str
    email:str
    password1: constr(max_length=10)
    password2: constr(max_length=10)
    address :Optional[str]

class LoginModel(BaseModel):
    identificator:str
    password: str

class ChangeAccountModel(BaseModel):
    id: int
    password: str
    username: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    new_password: Optional[str] = None

class UserDeleteAccountModel(BaseModel):
    id:int
    password:str
    reason: Optional[str] = None

class NewCategory(BaseModel):
    name: str
    descr: str

class NewBrand(BaseModel):
    name:str
    descr: str

@user_router.post('/registration', tags=['Работающие'])
async def register_user(user_model: RegistrationModel):
    data = dict(user_model)
    checker = mail_checker(user_model.email, user_model.phone_number)
    if checker:
        result = registration_db(**data)
        return {'status':1, 'message':'new user! hell yeah'}
    return {'status':0, 'message':'invalid email or phone number '}

@user_router.post('/login', tags=['Работающие'])
async def login_view(user_model: LoginModel):
    data = dict(user_model)
    result = login_db(identificator=user_model.identificator,
                      password=user_model.password)
    return {'status':1, 'message':result}

@user_router.post('/change', tags=['Работающие'])
async def change_account(user_model: ChangeAccountModel):
    data = dict(user_model)
    result = change_account_db(id=user_model.id, password=user_model.password, username=user_model.username,
                               phone_number=user_model.phone_number, email=user_model.email,
                               address=user_model.address, new_password=user_model.new_password)
    return {'status':1, 'message':result}

@user_router.post('/del', tags=['Работающие'])
async def drop_account(user_model: UserDeleteAccountModel):
    result = delete_account_db(id = user_model.id, password=user_model.password)
    return {'status':1, 'message':result}

@user_router.post('/get_ex_user', tags=['Работающие'])
async def ex_user(id:int):
    result = get_exact_user(id=id)
    if result:
        return {'status': 1, 'message': result}
    return {'status':1, 'message':'not exists'}

@user_router.post('/new_cat', tags=['Работающие'])
async def add_new_cat(prod_model: NewCategory):
    result = new_category(name=prod_model.name,
                          descr=prod_model.descr)
    return result

@user_router.post('/new_brand', tags=['Работающие'])
async def br_new(brand_model: NewBrand):
    result = new_brand(name=brand_model.name,
                       descr=brand_model.descr)
    return result

@user_router.post('/new_prod', tags=['Работающие'])
async def new_prod(
    name: str = Form(...),
    descr:str = Form(...),
    price: str = Form(...),
    count:int = Form(...),
    category_id: int = Form(...),
    brand_id: int = Form(...),
    file: UploadFile = File(...)):
    if file:
        file_id = uuid.uuid4()
        file_extension = file.filename.split('.')[-1]
        file_path = f'database/photos/photo_{file_id}.{file_extension}'
        with open(file_path, 'wb') as buffer:
            shutil.copyfileobj(file.file, buffer)
        result = new_product(name=name, descr=descr, photo=file_path, price=price,
                             category_id=category_id, brand_id=brand_id, count=count)
        return {'status': 1, 'message': result}
    return {'status': 1, 'message': 'not exists'}

@user_router.post('/get_ex_cat', tags=['Работающие'])
async def ex_cat_get(id:int):
    result = get_exact_category(id=id)
    return result

@user_router.post('/get_ex_brand', tags=['Работающие'])
async def ex_br_get(id:int):
    result = get_exact_brand(id=id)
    return result

@user_router.post('/get_ex_prod', tags=['Работающие'])
async def ex_prod_get(id:int):
    result = get_exact_product(id=id)
    return result

@user_router.post('/add_to_fav', tags=['Работающие'])
async def fav_add(id, product_id):
    result = add_to_favorite(id=id, product_id=product_id)
    return result

@user_router.post('/add_to_cart', tags=['Работающие'])
async def cart_add(id:int, product_id:int, count:int):
    result = add_to_cart(id=id, product_id=product_id, count=count)
    return result

@user_router.post('/cart_del', tags=['Работающие'])
async def del_cart(id:int, product_id:int, count:int):
    result = del_from_cart(id=id, product_id=product_id, count=count)
    return result

@user_router.post('/fav_del', tags=['Работающие'])
async def del_fav(id:int, product_id:int):
    result = del_from_fav(id=id, product_id=product_id)
    return result

@user_router.get('/home', tags=['Работающие'])
async def main_menu():
    result = get_prod_main_menu()
    return result

@user_router.post('/ex_prod_by_cat', tags=['Тест'])
async def prod_ex_by_cat(id:int):
    result = get_exact_prod_by_cat(id=id)
    return result

@user_router.post('/ex_prod_by_brand', tags=['Тест'])
async def prod_ex_by_cat(id:int):
    result = get_exact_prod_by_brand(id=id)
    return result