from fastapi import FastAPI, Depends, HTTPException, status
from app.database import engine, Base, get_db
import app.models
from sqlalchemy.orm import Session
from app import models, schemas, crud
from app.auth import create_access_token, get_current_user
from fastapi.security import HTTPBearer



# APP Setup
app = FastAPI(
    title="Bazar API",
    description="A ecommerce bankend API",
    version="1.0.0"
)
security = HTTPBearer()

Base.metadata.create_all(bind = engine)


# Root
@app.get("/")
def root():
    return {"Welcome to BAZAR"}


# AUTH Routes
@app.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if the email already exists
    existing = crud.get_user_by_email(db, user.email)
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    return crud.create_user(db, user)


@app.post("/login", response_model=schemas.Token)
def login(user: schemas.Login, db: Session = Depends(get_db)):
    # Find user by email
    db_user = crud.get_user_by_email(db, user.email)
    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )
    #verify password
    if not crud.verify_password(user.password, db_user.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )
    
    # Create and return token
    token = create_access_token(data={"sub": db_user.email})
    return {"access_token": token, "token_type": "bearer"}


# User routes
@app.get("/users", response_model=list[schemas.UserResponse])
def get_all_users(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return crud.get_all_users(db)

@app.get("/users/me", response_model=schemas.UserResponse)
def get_me(current_user = Depends(get_current_user)):
    return current_user


# Product routes
@app.post("/products", response_model=schemas.ProductResponse)
def create_product(
    product: schemas.ProductCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return crud.create_product(db, product)


@app.get("/products", response_model=list[schemas.ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return crud.get_all_products(db)

@app.get("/products/{product_id}", response_model=schemas.ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = crud.get_product_by_id(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.put("/products/{product_id}", response_model=schemas.ProductResponse)
def update_product(
    product_id: int,
    product: schemas.ProductCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    update = crud.update_product(db, product_id, product)
    if not update:
        raise HTTPException(status_code=404, detail="Product not found")
    return update


@app.delete("/products/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    deleted = crud.delete_product(db, product_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}

# Cart routes
@app.post("/cart", response_model=schemas.CartResponse)
def add_to_cart(
    cart: schemas.CartCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return crud.add_to_cart(db, current_user.id, cart)


@app.get("/cart", response_model=list[schemas.CartResponse])
def get_cart(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return crud.get_cart_by_user(db, current_user.id)



@app.delete("/cart/{cart_id}")
def delete_cart_item(
    cart_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    deleted = crud.delete_cart_item(db, cart_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return {"message": "Item removed from cart"}

    

# Order routes


@app.post("/orders", response_model=schemas.OrderResponse)
def create_order(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    order = crud.create_order(db, current_user.id)
    if not order:
        raise HTTPException(status_code=400, detail="Cart is empty")
    return order


@app.get("/orders", response_model=list[schemas.OrderResponse])
def get_orders(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return crud.get_orders_by_user(db, current_user.id)




