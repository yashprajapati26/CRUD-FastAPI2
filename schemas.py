from pydantic import BaseModel

class User(BaseModel):
    email: str
    password: str
    is_active: bool
   
    class Config:
        orm_mode = True

class Item(BaseModel):
    title: str
    description: str
    owner_id: int

    class Config:
        orm_mode = True

