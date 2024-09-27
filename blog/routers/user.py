from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session 
from .. import schemas, models, hashing, database

router = APIRouter(
    tags=["user"]
)
get_db = database.get_db

@router.post("/user", status_code=201, response_model=schemas.ShowUser)
def create_user(body: schemas.User, db: Session = Depends(get_db)):
    hashed_password = hashing.hash_text(body.password)
    new_user = models.User(name=body.name, email=body.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/users", response_model=List[schemas.ShowUser])
def get_all(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

@router.get("/user/{id}", response_model=schemas.ShowUser)
def get_user(id, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} D.N.E")
    return user

@router.delete("/user/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} D.N.E")
    user.delete(synchronize_session=False)
    db.commit()
    return {"msg" : "Deleted"}

