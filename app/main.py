from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Optional
app = FastAPI()


class post(BaseModel):
    Title:str
    content:str
    published: bool = True
    rating : Optional[int] = None
    id : int 

my_post = [post(Title='INDIA', content='INDIA IS A BEAUTIFUL COUNTRY', published=True, rating=None, id = 1),
            post(Title='Nepal', content='Nepal IS A Neighbor COUNTRY of india', published=True, rating=3, id =2)]

@app.get('/')
def root():
    return {"message":"Hello world"}


@app.get('/posts')
def get_post():
    return{"message": my_post}

@app.post('/createpost', status_code = status.HTTP_201_CREATED)
def create_post(new_post: post): 
    new_post.dict() 
    my_post.append(new_post)
    print(my_post)
    return{"message": my_post}


@app.get('/posts/{id}')
def get_one_post(id: int):
    for p in my_post:
        if p.id == id:
            return p

    raise HTTPException(status_code=404, detail="Post not found")

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    for ind, p in enumerate(my_post):
        if p.id == id:
            my_post.pop(ind)
            return

    raise HTTPException(status_code=404, detail="Post not Exist")


@app.put('/posts_update/{id}')
def update_post(id: int, posts:post):
    for ind, p in enumerate(my_post):
        if p.id == id:
            post_dict = posts.dict()
            # post_dict['id'] = id 
            my_post[ind] = post(**post_dict)
            return {"message": "Post Updated Successfully"}

    raise HTTPException(status_code=404, detail="Post not Exist")


# run : fastapi dev main.py
# or 
# uvicorn main:app --reload