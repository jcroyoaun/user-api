from http.client import HTTPException
from typing import List
from uuid import uuid4
from fastapi import FastAPI, Depends
from models import *
from database import engine, SessionLocal
import models 
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@app.get("/")
def create_database():
    return {"Hello": "Grid U!"}

@app.get("/api/v1/users")
async def fetch_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

@app.post("/api/v1/users")
async def register_user(user: UserModel, db: Session = Depends(get_db)):
    user_model = models.User()
    user_model.id = user.id
    user_model.first_name = user.first_name
    user_model.last_name = user.last_name
    user_model.middle_name = user.middle_name
    db.add(user_model)
    db.commit()
    return {"id": user.id }

# todo: complete delete method
# @app.delete("/api/v1/users/{user_id}")

# todo: complete put method
# @app.put("/api/v1/users/{user_id}")
