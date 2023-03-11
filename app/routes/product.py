from fastapi import APIRouter, HTTPException, Depends, status, Response
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter(
  prefix="/products",
  tags=["products"]
)

# http://127.0.0.1:8000/products

# api de productos

@router.get("/", response_model=List[schemas.Product])
async def get_products(db: Session = Depends(get_db)):
  return db.query(models.Product).all()


@router.get("/{id}", response_model=schemas.Product)
async def get_product(id: int, db: Session = Depends(get_db)):
  product_found = db.query(models.Product).filter(models.Product.id == id).first()
  
  if not product_found:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                          detail=f"El producto con el id: {id} no existe")
  
  return product_found


@router.post("/", response_model=schemas.Product, status_code=status.HTTP_201_CREATED)
async def create_product(product: schemas.Product, db: Session = Depends(get_db)):

  category_found = db.query(models.Category).filter(models.Category.id == product.category_id).first()
  
  if not category_found:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                          detail=f"La categoria con el id: {product.category_id} no existe")
  
  if not category_found.is_active:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                          detail=f"La categoria con el id: {product.category_id} esta inactiva")

  new_product = models.Product(**product.dict())
  db.add(new_product)
  db.commit()
  db.refresh(new_product)

  return new_product

@router.put("/", response_model=schemas.Product)
async def update_product(product: schemas.Product, db: Session = Depends(get_db)):
  product_query = db.query(models.Product).filter(models.Product.id == id)

  product_found = product_query.first()

  if product_found == None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"El product con el id: {id} no existe")


  product_query.update(product.dict(), synchronize_session=False)
  db.commit()

  return product_query.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(id: int, db: Session = Depends(get_db)):
  product_query = db.query(models.Product).filter(models.Product.id == id)

  product_found = product_query.first()

  if product_found == None:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                          detail=f"El product con el id: {id} no existe")

  product_query.delete(synchronize_session=False)
  db.commit()

  return Response(status_code=status.HTTP_204_NO_CONTENT)


