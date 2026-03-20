from fastapi import  HTTPException, status, Depends, APIRouter
from .. import db_models, schemas
from .. database import get_db
from sqlalchemy.orm import Session
from typing import List
from .. oauth2 import get_current_user
from typing import Optional
from sqlalchemy import func

router = APIRouter(
    prefix= '/posts',      # keeping the all the routers name same, starting with /posts
    tags= ['Posts']
)


# @router.get('/',response_model= List[schemas.PostResponse])
@router.get('/',response_model= List[schemas.PostOut])
def get_posts(db:Session = Depends(get_db), current_user_obj: int = Depends(get_current_user), limit: int=10, skip: int = 0, search : Optional[str] =""):
    # cursor.execute(""" SELECT * FROM posts""")
    # posts = cursor.fetchall()
    #posts = db.query(db_models.Post).filter(db_models.Post.title.contains(search)).limit(limit).offset(skip).all()  # limit and skip are the query parameter where any user can customise the output in the frontend.
    # Note: if you apply more than one query parameter then use by '&' b/w both the query. '?' is used to initiate the query option.
    # %20 is used for space during wirting of a query

    posts = db.query(db_models.Post, func.count(db_models.Vote.post_id).label("Like_count")).join(db_models.Vote, db_models.Vote.post_id == db_models.Post.id, isouter=True)\
        .group_by(db_models.Post.id).filter(db_models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # print(result) # apply left outer join
    return posts

@router.post('/', status_code = status.HTTP_201_CREATED, response_model= schemas.PostResponse)
def create_post(pos: schemas.CreatePost, db:Session = Depends(get_db), current_user_obj: int = Depends(get_current_user)): # user_id: int = Depends(get_current_user) this helps to run get_current_user this if its gives the id then end point will work otherwise not

    # cursor.execute(""" INSERT INTO posts (title,content, published, rating) VALUES (%s,%s,%s,%s) RETURNING *""",
    #                (pos.title, pos.content, pos.published, pos.rating))
    
    # new_post = cursor.fetchone()
    # conn.commit()

    new_post  = db_models.Post(owner_id = current_user_obj.id, **pos.dict())  # passing all the user input to the db schema (Title = pos.Title, content = pos.content)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)  # this helps to retrieve the currently pushed data from the db and stored in the new_post variable
    return new_post


@router.get('/{post_id}',response_model= schemas.PostOut)
def get_post(post_id: int , db:Session = Depends(get_db), current_user_obj: int = Depends(get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (post_id,))
    # post_id_data = cursor.fetchone()

    # post_id_data = db.query(db_models.Post).filter(db_models.Post.id == post_id).first()
    post_id_data = db.query(db_models.Post, func.count(db_models.Vote.post_id).label("Like_count")).join(db_models.Vote, db_models.Vote.post_id == db_models.Post.id, isouter=True)\
        .group_by(db_models.Post.id).filter(db_models.Post.id == post_id).first()

    if post_id_data is None:
        raise HTTPException(status_code=404, detail="Post not found")

    
    return post_id_data



@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db:Session = Depends(get_db), current_user_obj: int = Depends(get_current_user)):
    # cursor.execute(
    #     "DELETE FROM posts WHERE id = %s RETURNING *",
    #     (id,))
    # deleted_id_post = cursor.fetchone()
    # conn.commit()
    deleted_id_post = db.query(db_models.Post).filter(db_models.Post.id == id)  # find the required query for the given id
    
    if deleted_id_post.first() is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if deleted_id_post.first().owner_id != current_user_obj.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorised to perform this action")

    deleted_id_post.delete(synchronize_session = False)
    db.commit()
    #return Response(status_code= status.HTTP_204_NO_CONTENT)



@router.put('/{id}', response_model= schemas.PostResponse)
def update_post(id: int, updated_post:schemas.CreatePost, db:Session = Depends(get_db), current_user_obj: int = Depends(get_current_user)):
    # cursor.execute(
    #     "UPDATE posts SET title = %s, content = %s, published = %s, rating = %s WHERE id = %s RETURNING *",
    #     (posts.title, posts.content, posts.published, posts.rating, id))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query =  db.query(db_models.Post).filter(db_models.Post.id == id)
   
    if post_query.first() is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if post_query.first().owner_id != current_user_obj.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorised to perform this action")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
