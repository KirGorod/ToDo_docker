from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqladmin import Admin

from app import crud, models, schemas
from app.database import engine, SessionLocal
from app.admin import AdminAuth, ItemAdmin

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Admin
authentication_backend = AdminAuth(secret_key="...")
admin = Admin(
    app=app,
    authentication_backend=authentication_backend,
    engine=engine
)
admin.add_view(ItemAdmin)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/item/{item_id}", response_model=schemas.Item)
def get_item(item_id: int, db: Session = Depends(get_db)):
    return crud.get_item(db, item_id)


@app.get("/items/", response_model=list[schemas.Item])
def get_items(db: Session = Depends(get_db)):
    return crud.get_items(db=db)


@app.post("/items/", response_model=schemas.Item)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_item(db=db, item=item)


@app.put("/items/{item_id}")
def update_item(item_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    item_db = db.query(models.Item).filter(models.Item.id == item_id).first()
    if item_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Item with id {item_id} not found.')
    crud.update_item(db, item_id, item)
    return {'message': 'Item successfully updated.'}


@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Item with id {item_id} not found.'
        )
    crud.delete_item(db, item_id)
    return {'message:': 'Item deleted successfully.'}
