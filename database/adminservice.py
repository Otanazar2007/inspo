from database import get_db, Base
from database.models import User, Product, Category, Cart, Favorite, Brand

def new_category(name:str, descr:str):
    with next(get_db()) as db:
        check = db.query(Category).filter_by(name=name).first()
        if check:
            return {'status':0, 'message':'already exists'}
        else:
            result = Category(
                name = name,
                descr = descr
            )
            db.add(result)
            db.commit()
            return {'status':1, 'message':'good job'}

def new_brand(name:str, descr:str):
    with next(get_db()) as db:
        check = db.query(Brand).filter_by(name=name).first()
        if check:
            return {'status': 0, 'message': 'already exists'}
        else:
            result = Brand(
                name = name,
                descr = descr
            )
            db.add(result)
            db.commit()
            return {'status':1, 'message':'good job'}

def new_product(name:str, descr:str, photo:str, price:str, count:str, category_id:int, brand_id:int):
    with next(get_db()) as db:
        check = db.query(Product).filter_by(name=name).first()
        if check:
            return {'status': 0, 'message': 'already exists'}
        else:
            result = Product(
                name = name,
                descr = descr,
                photo = photo,
                price = price,
                count = count,
                category_id = category_id,
                brand_id = brand_id
            )
            db.add(result)
            db.commit()
            return  {'status':1, 'message':'good job'}


def get_exact_user(id:int):
    with next(get_db()) as db:
        check = db.query(User).filter_by(id = id).first()
        if check:
                return check
        return {'status': 0, 'message': 'already exists'}

def get_exact_product(id:int):
    with next(get_db()) as db:
        check = db.query(Product).filter_by(id=id).first()
        if check:
            return check
        return {'status': 0, 'message': 'already exists'}

def get_exact_brand(id:int):
    with next(get_db()) as db:
        check = db.query(Brand).filter_by(id=id).first()
        if check:
            return check
        return {'status': 0, 'message': 'already exists'}

def get_exact_category(id:int):
    with next(get_db()) as db:
        check = db.query(Category).filter_by(id=id).first()
        if check:
            return check
        return {'status': 0, 'message': 'already exists'}

def get_exact_cart(id:int):
    with next(get_db()) as db:
        check = db.query(Cart).filter_by(id=id).first()
        if check:
            return check
        return {'status': 0, 'message': 'already exists'}