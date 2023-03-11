from fastapi import FastAPI
from .routes import product, category
from .database import engine
from . import models

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# uvicorn main:app --reload
# http://127.0.0.1:8000


@app.get("/")
async def root():
  return { "message": "API POSTGRESQL CON ENTORNO VIRTUAL" }

# routes
app.include_router(product.router)
app.include_router(category.router)

# http://127.0.0.1:8000/docs
# http://127.0.0.1:8000/redoc

