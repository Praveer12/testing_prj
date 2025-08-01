
from fastapi import FastAPI, Depends, HTTPException, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from models import *

from database import engine, db_run
import models, schemas, auth
from typing import List


models.Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




class Categories:

    @staticmethod

    async def create_category(category: schemas.CategoryCreate, db: Session = Depends(db_run), current_user: int = Depends(auth.get_current_user)):
        db_category = models.Category(**category.model_dump())
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category

    @staticmethod

    async def get_list(db: Session = Depends(db_run)):
        return db.query(models.Category).all()

    # Category CRUD

    @staticmethod

    async def get_category(category_id: int, db: Session = Depends(db_run)):
        category = db.query(models.Category).filter(models.Category.id == category_id).first()
        if not category:
            raise HTTPException(404, detail="Category not found")
        return category



    @staticmethod

    async def update_category(category_id: int, category: schemas.CategoryUpdate, db: Session = Depends(db_run), current_user: int = Depends(auth.get_current_user)):
        db_category = db.query(models.Category).filter(models.Category.id == category_id).first()
        if not db_category:
            raise HTTPException(404, detail="Category not found")

        for key, value in category.model_dump(exclude_unset=True).items():
            setattr(db_category, key, value)

        db.commit()
        db.refresh(db_category)
        return db_category

    @staticmethod

    async def delete_category(category_id: int, db: Session = Depends(db_run), current_user: int = Depends(auth.get_current_user)):
        db_category = db.query(models.Category).filter(models.Category.id == category_id).first()
        if not db_category:
            raise HTTPException(404, detail="Category not found")

        db.delete(db_category)
        db.commit()
        return {"message": "Category deleted successfully"}

# Products CRUD

class Products:
    @staticmethod

    async def create_products(products: schemas.EcommCreate, db: Session = Depends(db_run), current_user: dict = Depends(auth.get_current_user)):
        if not db.query(models.Category).filter(models.Category.id == products.category_id).first():
            raise HTTPException(404, "Category not found")



        db_product = Ecomm(

            product = products.product,
            price = products.price,
            description = products.description,
            category_id = products.category_id,
            owner_id = current_user.id
        )

        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product

    @staticmethod

    async def get_product(product_id: int, db: Session = Depends(db_run)):
        product = db.query(models.Ecomm).filter(models.Ecomm.id == product_id).first()

        if not product:
            raise HTTPException(404, detail="Product not found")
        return product

    @staticmethod

    async def get_all_products(db: Session = Depends(db_run),current_user: int = Depends(auth.get_current_user)):
        return db.query(Ecomm).filter(Ecomm.owner_id == current_user.id).order_by(Ecomm.id.asc()).all()


    @staticmethod

    async def update_product(product_id: int, product: schemas.EcommUpdate, db: Session = Depends(db_run), current_user: int = Depends(auth.get_current_user)):
        db_product = db.query(models.Ecomm).filter(models.Ecomm.id == product_id).first()
        if not db_product:
            raise HTTPException(404, detail="Product not found")

        if product.category_id:
            category_db = db.query(models.Category).filter(models.Category.id == product.category_id).first()
            if not category_db:
                raise HTTPException(404, detail="Category not found")

        for key, value in product.model_dump(exclude_unset=True).items():
            setattr(db_product, key, value)

        db.commit()
        db.refresh(db_product)
        return db_product

    @staticmethod

    async def delete_product(product_id: int, db: Session = Depends(db_run), current_user: int = Depends(auth.get_current_user)):
        db_product = db.query(models.Ecomm).filter(models.Ecomm.id == product_id).first()
        if not db_product:
            raise HTTPException(404, detail="Product not found")

        db.delete(db_product)
        db.commit()
        return {"message": "Product deleted successfully"}


#Category Router
category_router = APIRouter( tags=["Shopping Category"])
category_router.post("/category", response_model=schemas.CategoryResponse)(Categories.create_category)
category_router.get("/list", response_model=List[schemas.CategoryResponse])(Categories.get_list)
category_router.get("/category/{category_id}", response_model=schemas.CategoryResponse)(Categories.get_category)
category_router.patch("/category/{category_id}", response_model=schemas.CategoryResponse)(Categories.update_category)
category_router.delete("/category/{category_id}")(Categories.delete_category)

#Product Router
product_router = APIRouter( tags=["Shopping Products"])
product_router.post("/products", response_model=schemas.EcommResponse)(Products.create_products)
product_router.get("/products/{product_id}", response_model=schemas.EcommResponse)(Products.get_product)
product_router.get("/products", response_model=List[schemas.EcommResponse])(Products.get_all_products)
product_router.patch("/products/{product_id}", response_model=schemas.EcommResponse)(Products.update_product)
product_router.delete("/products/{product_id}")(Products.delete_product)



app.include_router(auth.router)
app.include_router(category_router)
app.include_router(product_router)