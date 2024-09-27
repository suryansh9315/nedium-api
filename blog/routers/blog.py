from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Annotated
from sqlalchemy.orm import Session 
from .. import schemas, models, database, oauth2

router = APIRouter(
    tags=["blog"]
)
get_db = database.get_db

@router.post("/blog", status_code=201, response_model=schemas.ShowBlog)
def create(body: schemas.Blog, current_user: Annotated[schemas.User, Depends(oauth2.get_current_user)], db: Session = Depends(get_db)):
    new_blog = models.Blog(title=body.title, description=body.description, body=body.body, user_id=1 )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@router.get("/blogs", response_model=List[schemas.ShowBlog])
def get_all(current_user: Annotated[schemas.User, Depends(oauth2.get_current_user)], db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@router.get("/blog/{id}", response_model=schemas.ShowBlog)
def get_blog(id, current_user: Annotated[schemas.User, Depends(oauth2.get_current_user)], db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} D.N.E")
    return blog

@router.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id, current_user: Annotated[schemas.User, Depends(oauth2.get_current_user)], db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} D.N.E")
    blog.delete(synchronize_session=False)
    db.commit()
    return {"msg" : "Deleted"}

@router.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_blog(id, current_user: Annotated[schemas.User, Depends(oauth2.get_current_user)], body: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} D.N.E")
    blog.update(body)
    db.commit()
    return {"msg" : "Updated"}