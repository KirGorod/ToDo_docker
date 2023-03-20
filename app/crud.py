from sqlalchemy.orm import Session

from app import models, schemas

def get_item(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id).one()


def get_items(db: Session):
    return db.query(models.Item).all()


def create_item(db: Session, item: schemas.ItemCreate):
    db_item = models.Item(title=item.title, description=item.description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_item(db: Session, item_id: int, item: schemas.ItemCreate):
    db.query(models.Item).filter(models.Item.id == item_id).update(item.dict(exclude_unset=True))
    db.commit()


def delete_item(db: Session, item_id: int):
    db.query(models.Item).filter(models.Item.id == item_id).delete()
    db.commit()
    return
