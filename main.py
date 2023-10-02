from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi import Depends, FastAPI, HTTPException
import crud, models, schemas
from models import User, Item
from db import SessionLocal, engine
from sqlalchemy.orm import Session
from sqladmin import Admin, ModelView
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
admin = Admin(app, engine)

# Here register our model in sqlAdmin 
class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email, User.is_active]

class ItemAdmin(ModelView, model=Item):
    column_list = [Item.id, Item.title, Item.description, Item.owner_id]

 # add on dashboard
admin.add_view(UserAdmin)
admin.add_view(ItemAdmin)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def index():
    return "Welcome To FastAPI Demo"


# users routes 

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.User, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.put("/users/{user_id}",response_model=schemas.User)
def update_user(user_id: int, user: schemas.User,db: Session = Depends(get_db)):
    updated_user = crud.update_user(db, user_id=user_id, user=user)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user


@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    delete_user = crud.delete_user(db, user_id=user_id)
    if delete_user:
        return {"msg": "User Deleted Sucessfully"}
    else:
        raise HTTPException(status_code=404, detail="User not found")



# item routes

@app.post("/items/", response_model=schemas.Item)
def create_item(item: schemas.Item, db: Session = Depends(get_db)):
    return crud.create_item(db=db, item=item)


@app.get("/items/", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items

@app.get("/items/{item_id}", response_model=schemas.Item)
def read_item(item_id :int , db:Session = Depends(get_db)):
    item = crud.get_item(db, item_id=item_id)
    return item

@app.put("/items/{item_id}",response_model=schemas.Item)
def update_item(item_id: int, item: schemas.Item,db: Session = Depends(get_db)):
    updated_item = crud.update_item(db, item_id=item_id, item=item)
    if updated_item:
        return updated_item
    else:
        raise HTTPException(status_code=404, detail="Item not found")

