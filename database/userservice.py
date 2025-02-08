from database import get_db, Base
from database.models import User, Product, Category, Cart, Favorite, Brand
from telebot import TeleBot
bot = TeleBot(token='7722831734:AAHhjV00pbU5l0b_OL90il5G1UW_MV4h54Y')
def registration_db(username:str, password1:str, password2:str, phone_number:str, email:str = None, address:str = None):
    with next(get_db()) as db:
        user = db.query(User).filter(
            (User.phone_number == phone_number) |
            (User.email == email)
        ).first()
        if user:
            return {"status":0, 'message':"You are already registered"}
        else:
            if password1 == password2:
                new_user = User(
                    username = username,
                    password = password1,
                    phone_number = phone_number,
                    email = email,
                    address = address,
                )
                db.add(new_user)
                db.commit()
                return {"status":1, 'message':'Good'}
            return {"status":1, 'message':'Your password dont match'}

def login_db(identificator:str, password:str):
    with next(get_db()) as db:
        check = db.query(User).filter(
            (User.phone_number == identificator) |
            (User.email == identificator)
        ).first()
        if not check:
            return {'status':0, 'message':'User not exists'}
        if check.password == password:
            return {'status':'Good'}
        return {'status':0, 'message':'Invalid password'}

def change_account_db(id:int,password:str, username:str = None, phone_number:str = None, email:str = None,
                   address:str = None, new_password:str = None):
    with next(get_db()) as db:
        user = db.query(User).filter_by(id=id).first()
        changes = False
        if not user:
            return {'status':0, 'message':'user not found'}
        if user.password == password:
            if username is not None and  username !='string':
                user.username = username
                changes = True
            if phone_number is not None and phone_number !='string':
                user.phone_number = phone_number
                changes = True
            if email is not None and email !='string':
                user.email = email
                changes = True
            if address is not None and address !='string':
                user.address = address
                changes = True
            if new_password is not None and new_password !='string':
                user.password = new_password
                changes = True

            if changes:
                db.commit()
                return {'status':1, 'message':'user details updated!!!'}
            else:
                return {'status':0, 'message':'no changes detected'}

        else:
            return {'status':0, 'message':"invalid password"}

def delete_account_db(id:int, password:str):
    with next(get_db()) as db:
        user = db.query(User).filter_by(id=id).first()
        if user is not None and user.password == password:
            db.delete(user)
            db.commit()
            return {'status':1, 'message':'account deleted'}
        return {"status":0, 'message':'error'}

def add_to_favorite(id:int, product_id:int):
    with next(get_db()) as db:
        check = db.query(Product).filter_by(id=product_id).first()
        if check:
            result = Favorite(
                user_id = id,
                product_id = product_id
            )
            db.add(result)
            db.commit()
            return {'status': 1, 'message': 'good job'}
        return {'status':0, 'message':'not exists'}

def del_from_fav(id:int, product_id:int):
    with next(get_db()) as db:
        check = db.query(Favorite).filter_by(user_id = id, product_id = product_id).one_or_none()
        if check:
            db.delete(check)
            db.commit()
            return {'status': 1, 'message': 'good job'}
        return {'status': 0, 'message': 'not exists'}

def add_to_cart(id:int, product_id:int, count:int):
    with next(get_db()) as db:
        check = db.query(Product).filter_by(id=product_id).first()
        check_cart = db.query(Cart).filter_by(product_id=product_id, user_id=id).first()
        if check and check_cart:
            check_cart.count += count
            db.commit()
            return {'status': 1, 'message': 'good job'}
        elif check and not check_cart:
            new_cart_item = Cart(
                user_id = id,
                product_id =product_id,
                count = count
            )
            db.add(new_cart_item)
            db.commit()
            return {'status':1, 'message':'good job'}
        else:
            return {'status': 0, 'message': 'not exists'}

def del_from_cart(id:int, product_id:int, count:int):
    with next(get_db()) as db:
        check = db.query(Cart).filter_by(user_id = id, product_id = product_id).first()
        if check:
            if check.count > count:
                check.count -= count
                db.commit()
            else:
                db.delete(check)
                db.commit()
            return {'status': 1, 'message': 'good job'}
        return {'status': 0, 'message': 'not exists'}

def get_prod_main_menu():
    with next(get_db()) as db:
        all_products = db.query(Product).all()
        return all_products

def get_exact_prod_by_brand(id:int):
    with next(get_db()) as db:
        prod_by_brand = db.query(Product).filter_by(brand_id=id).all()
        return prod_by_brand

def get_exact_prod_by_cat(id:int):
    with next(get_db()) as db:
        prod_by_cat = db.query(Product).filter_by(category_id=id).all()
        return prod_by_cat

def get_all_cat():
    with next(get_db()) as db:
        result = db.query(Category).all()
        return result

def get_all_brands():
    with next(get_db()) as db:
        result = db.query(Brand).all()
        return result

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

def offer(id:int, count:int):
    with next(get_db()) as db:
        product = db.query(Product).filter_by(id=id).first()
        return product