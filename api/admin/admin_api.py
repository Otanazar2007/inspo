from fastapi import APIRouter, Request, Form, File, UploadFile
from database.adminservice import (get_exact_user,
                                   new_brand, new_category, new_product, change_prod_items,
                                   del_exact_prod, change_br_items, change_cat_items, del_ex_cat, del_ex_br)
from pydantic import BaseModel, constr
from typing import Optional
import uuid
import shutil


admin_router = APIRouter()

class NewBrand(BaseModel):
    name:str
    descr: str

class NewCategory(BaseModel):
    name: str
    descr: str


@admin_router.post('/get_ex_user', tags=['Админ сервис'])
async def ex_user(id:int):
    result = get_exact_user(id=id)
    if result:
        return {'status': 1, 'message': result}
    return {'status':1, 'message':'not exists'}

@admin_router.post('/new_brand', tags=['Админ сервис'])
async def br_new(brand_model: NewBrand):
    result = new_brand(name=brand_model.name,
                       descr=brand_model.descr)
    return result

@admin_router.post('/new_cat', tags=['Админ сервис'])
async def add_new_cat(prod_model: NewCategory):
    result = new_category(name=prod_model.name,
                          descr=prod_model.descr)
    return result

@admin_router.post('/new_prod', tags=['Админ сервис'])
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

@admin_router.post('/ch_it_prod', tags=['Админ сервис'])
async def change_product_items(
        id: int = Form(...),
        name: Optional[str] = Form(None),
        descr: Optional[str] = Form(None),
        price: Optional[str] = Form(None),
        count: Optional[str] = Form(None),
        category_id : Optional[int] = Form(None),
        brand_id: Optional[int] = Form(None),
        file: Optional[UploadFile] = File(None)
):
        """
        На данный момент функция работает только с отправкой файла, из-за того что сваггер отправляет странные
        значения при отсуствии файла функция работает некорректно, лучше что бы сам фронтендер при разработке сам
        указывал какие данные отправляются на сервер
        """

        if file:
            try:
                file_id = uuid.uuid4()
                file_extension = file.filename.split('.')[-1]
                file_path = f'database/photos/photo_{file_id}.{file_extension}'
                with open(file_path, 'wb') as buffer:
                    shutil.copyfileobj(file.file, buffer)
                result = change_prod_items(
                    id = id,
                    name = name,
                    descr = descr,
                    photo = file_path,
                    price = price,
                    count = count,
                    category_id = category_id,
                    brand_id = brand_id
                )
                return {'status':1, 'message':result}
            except Exception as e:
                return {'status': 0, 'message': f'Error occurred: {str(e)}'}

@admin_router.post('/del_exact_product', tags=['Админ сервис'])
async def delete_exact_product(id:int):
    result = del_exact_prod(id = id)
    return result

@admin_router.post('/change_br_it', tags=['Админ сервис'])
async def br_it_change(id:int, name:str=None, descr:str=None):
    result = change_br_items(
        id = id,
        name = name,
        descr = descr
    )
    return result

@admin_router.post('/change_cat_it', tags=['Админ сервис'])
async def change_category_items(id:int, name:str=None, descr:str=None):
    result = change_cat_items(
        id = id,
        name = name,
        descr = descr
    )
    return result

@admin_router.post('/del_ex_cat', tags=['Админ сервис'])
async def delete_exact_category(id:int):
    result = del_ex_cat(
        id=id
    )
    return result

@admin_router.post('/del_br_ex', tags=['Админ сервис'])
async def delete_exact_brand(id:int):
    result = del_ex_br(
        id=id
    )
    return result
