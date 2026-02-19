from sqlmodel import Session, select
from models import Product, Movement
from database import engine

def add_product(name, sku, min_threshold, price):
    with Session(engine) as session:
        product = Product(
            name=name,
            sku=sku,
            min_threshold=min_threshold,
            price=price
        )
        session.add(product)
        session.commit()

def get_products():
    with Session(engine) as session:
        return session.exec(select(Product)).all()
    

def update_ptoduct(product_id, name, sku, min_threshold, price):
    with Session(engine) as session:
        product = session.get(Product, product_id)
        if product:
            product.name = name,
            product.sku = sku,
            product.min_threshold = min_threshold,
            product.price = price
            session.add(product)
            session.commit()


def delete_product(product_id):
    with Session as session:
        product = session.get(Product, product_id)
        if product:
            session.delete(product)
            session.commit()

def move_stock(product_id, move_type, quantity):
    with Session(engine) as session:
        product = session.get(Product, product_id)

        if move_type == "IN":
            product.quantity += quantity
        elif move_type == "OUT" and product.quantity >= quantity:
            product.quantity -= quantity
        else:
            return False
        

        movement = Movement(
            product_id = product_id,
            type = move_type,
            quantity = quantity
        )

        session.add(movement)
        session.add(product)
        session.commit()

        return True
    

def get_alert_products():
    products = get_products()
    return [p for p in products if p.quantity < p.min_threshold]
    

def get_movements():
    with Session(engine) as session:
        return session.exec(select(Movement)).all()

