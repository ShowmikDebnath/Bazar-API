from sqlalchemy.orm import Session
from app import models, schemas
from passlib.context import CryptContext

# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


'''
# User Crud
'''

def create_user(db: Session, user: schemas.UserCreate):
    hashed = hash_password(user.password)

    db_user = models.User(
        name = user.name,
        email = user.email,
        password = hashed,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_all_users(db: Session):
    return db.query(models.User).all()



'''
# Product Crud
'''

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(
        name = product.name,
        description = product.description,
        price = product.price,
        quantity = product.quantity,
        category = product.category
    )

    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_all_products(db: Session):
    return db.query(models.Product).all()

def get_product_by_id(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def update_product(db: Session, product_id: int, product: schemas.ProductCreate):
    db_product = get_product_by_id(db, product_id)

    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.quantity = product.quantity
        db_product.category = product.category
        db.commit()
        db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int):
    db_product = get_product_by_id(db, product_id)

    if db_product:
        db.delete(db_product)
        db.commit()
    return db_product


'''
# Cart Crud
'''
def add_to_cart(db: Session, user_id: int, cart: schemas.CartCreate):
    db_cart = models.Cart(
        user_id = user_id,
        product_id = cart.product_id,
        quantity = cart.quantity
    )
    db.add(db_cart)
    db.commit()
    db.refresh(db_cart)
    return db_cart

def get_cart_by_user(db: Session, user_id: int):
    return db.query(models.Cart).filter(models.Cart.user_id == user_id).all()

def delete_cart_item(db: Session, cart_id: int):
    db_cart = db.query(models.Cart).filter(models.Cart.id == cart_id).first()
    if db_cart:
        db.delete(db_cart)
        db.commit()
    return db_cart



'''
# Order Crud
'''

def create_order(db: Session, user_id: int):
    # Get all cart items form this current user
    cart_items = get_cart_by_user(db, user_id)

    if not cart_items:
        return None
    

    # Calculate total price
    total = 0
    for item in cart_items:
        product = get_product_by_id(db, item.product_id)
        total += product.price * item.quantity

    # Create Order
    db_order = models.Order(
        user_id = user_id,
        total_price = total,
        status = "pending"
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)


    # Create order item from Cart
    for item in cart_items:
        product = get_product_by_id(db, item.product_id)
        db_order_item = models.OrderItem(
            order_id = db_order.id,
            product_id = item.product_id,
            quantity = item.quantity,
            price = product.price
        )

        db.add(db_order_item)
        db.delete(item) # Clear the cart after order

    db.commit()
    return db_order

def get_orders_by_user(db: Session, user_id: int):
    return db.query(models.Order).filter(models.Order.user_id == user_id).all()









