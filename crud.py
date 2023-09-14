from sqlalchemy.orm import Session
import models, schemas

# for users
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.User):
    db_user = models.User(email=user.email, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db:Session, user:schemas.User, user_id:int):
    user_to_update = db.query(models.User).filter_by(id=user_id).first()
    if user_to_update:
        user_to_update.email = user.email
        user_to_update.password = user.password
        db.commit()
        return user_to_update
   
    
def delete_user(db:Session, user_id:int):
    user_to_delete = db.query(models.User).filter_by(id=user_id).first()
    if user_to_delete:
        db.delete(user_to_delete)
        db.commit()
        return True



# for items 
def get_item(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id).first()

def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()

def create_item(db: Session, item: schemas.Item):
    db_item = models.Item(title=item.title, description=item.description, owner_id=item.owner_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_item(db:Session, item:schemas.Item, item_id:int):
    item_to_update = db.query(models.Item).filter_by(id=item_id).first()
    if item_to_update:
        item_to_update.title = item.title
        item_to_update.description = item.description
        item_to_update.owner_id = item.owner_id
        db.commit()
        return item_to_update
    else:
        return False
