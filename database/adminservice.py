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

def del_exact_prod(id:int):
    with next(get_db()) as db:
        check = db.query(Product).filter_by(id=id).first()
        if check:
            db.delete(check)
            db.commit()
            return {'status':1, 'message':'post deleted'}
        else:
            return {'status':0, 'message':'post not exist'}

def change_prod_items(id:int, name:str = None, descr:str = None, photo:str = None,
                      price:str = None, count:int = None, category_id:int = None, brand_id:int = None):
    with next(get_db()) as db:
        product = db.query(Product).filter_by(id=id).first()
        changes = False
        if not product:
            return {'status':0, 'message':'product not exists'}
        if name is not None and name !='string':
            product.name = name
            changes = True
        if descr is not None and descr != 'string':
            product.descr = descr
            changes = True
        if photo is not None and photo != 'string':
            product.photo = photo
            changes = True
        if price is not None and price != 'string':
            product.price = price
            changes = True
        if count is not None and count != 'string':
            product.count = count
            changes = True
        if category_id is not None and category_id != 0:
            product.category_id = category_id
            changes = True
        if brand_id is not None and brand_id != 0:
            product.brand_id = brand_id
            changes = True
        if changes:
            db.commit()
            return {'status':1, 'message':'product details updated'}
        else:
            return {'status':0, 'message':'no changes detected'}

def change_br_items(id:int, name:str = None, descr:str = None):
    with next(get_db()) as db:
        brand = db.query(Brand).filter_by(id=id).first()
        changes = False
        if name is not None and name !='string':
            brand.name = name
            changes = True
        if descr is not None and descr != 'string':
            brand.descr = descr
            changes = True
        if changes:
            db.commit()
            return {'status':1, 'message': 'brand items updated'}
        else:
            return {'status':0, 'message':'no changes detected'}

def del_ex_br(id:int):
    with next(get_db()) as db:
        brand = db.query(Brand).filter_by(id=id).first()
        if brand:
            db.delete(brand)
            db.commit()
            return {'status':1, 'message':'brand deleted'}
        else:
            return {'status':0, 'message':'brand not exist'}

def change_cat_items(id:int, name:str = None, descr:str = None):
    with next(get_db()) as db:
        category = db.query(Category).filter_by(id=id).first()
        changes = False
        if category is not None and category != 'string':
            category.name = name
            changes = True
        if descr is not None and descr != 'string':
            category.descr = descr
            changes = True
        if changes:
            db.commit()
            return {'status':1, 'message':'category items updated'}
        else:
            return {'status':0, 'message':'no changes detected'}

def del_ex_cat(id:int):
    with next(get_db()) as db:
        category = db.query(Category).filter_by(id=id).first()
        if category:
            db.delete(category)
            db.commit()
            return {'status':1, 'message':'category deleted'}
        else:
            return {'status':0, 'message':'not exist'}