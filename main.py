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

# db: List[User] = [
#     User(
#         id=uuid4(), 
#         first_name="Chimpy", 
#         last_name="Oruguez",
#         # gender=Gender.female,
#         # roles=[Role.student]
#     ),
#     User(
#         id=uuid4(),
#         first_name="Jose",
#         last_name="Navarro",
#         # gender=Gender.male,
#         # roles=[Role.student]
#     )
# ]
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

# @app.delete("/api/v1/users/{user_id}")
# async def delete_user(user_id: UUID):
#     for user in db:
#         if user.id == user_id:
#             db.remove(user)
#     raise HTTPException (
#         status_code=404,
#         detail="user with id: {user_id} does not exist"
#     )
# @app.put("/api/v1/users/{user_id}")
# async def update_user(user_update: UserUpdateRequest, user_id: UUID):
#     for user in db:
#         if user.id == user_id:
#             if user_update.first_name is not None:
#                 user.first_name = user_update.first_name
#             if user_update.last_name is not None:
#                 user.last_name = user_update.last_name
#             if user_update.middle_name is not None:
#                 user.middle_name = user_update.middle_name
#             if user_update.roles is not None:
#                 user.roles = user_update.roles
#             return
#     raise HTTPException(
#         status_code=404,
#         detail=f"user with id: {user_id} does not exist"
#     )