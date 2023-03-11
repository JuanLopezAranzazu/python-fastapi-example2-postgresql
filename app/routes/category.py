from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter(
  prefix="/categories",
  tags=["categories"]
)

# http://127.0.0.1:8000/categories

# api de categorias

@router.get("/", response_model=List[schemas.Category])
async def get_categories(db: Session = Depends(get_db)):
  return db.query(models.Category).all()


@router.get("/{id}", response_model=schemas.Category)
async def get_category(id: int, db: Session = Depends(get_db)):
  category_found = db.query(models.Category).filter(models.Category.id == id).first()
  
  if not category_found:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                          detail=f"La categoria con el id: {id} no existe")
  
  return category_found


@router.post("/", response_model=schemas.Category, status_code=status.HTTP_201_CREATED)
async def create_category(category: schemas.Category, db: Session = Depends(get_db)):

  new_category = models.Category(**category.dict())
  db.add(new_category)
  db.commit()
  db.refresh(new_category)

  return new_category
