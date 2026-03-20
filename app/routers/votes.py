from fastapi import  HTTPException, status, Depends, APIRouter
from .. import db_models, schemas
from .. database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. oauth2 import get_current_user


router = APIRouter(
    prefix= '/votes',      # keeping the all the routers name same, starting with /votes
    tags= ['Votes']
)

@router.post('/', status_code=status.HTTP_201_CREATED)
def votes(req:schemas.Vote, db:Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    
    post_exist = db.query(db_models.Post).filter(db_models.Post.id ==  req.post_id).first()

    if not post_exist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {req.post_id} does not exist!")    

    like_query =  db.query(db_models.Vote).filter(db_models.Vote.post_id == req.post_id, db_models.Vote.user_id == current_user.id)

    found_vote = like_query.first()

    if req.like == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} already liked this post {req.post_id}")
        
        new_like = db_models.Vote(post_id = req.post_id, user_id = current_user.id)
        db.add(new_like)
        db.commit()
       
    
    else:
        if not found_vote:
             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post is can not unlike without like")
        
        like_query.delete(synchronize_session=False)
        db.commit()
    

    updated_like = db.query(func.count(db_models.Vote.post_id)).filter(db_models.Vote.post_id == req.post_id)
    print(updated_like)
    return {"message":f"Total Likes {updated_like.scalar()}"}
        


    


