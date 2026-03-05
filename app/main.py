from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

class post(BaseModel):
    Title:str
    content:str
    published: bool = True
    rating : Optional[int] = None
    
while True:  # This loop helps to connect the fastapi server to postgre database until it is connected, then it moves to backend endpoints.
        
        try:
            conn =  psycopg2.connect(host = 'localhost', database ='Fastapi', user = 'postgres', 
                             password = '2003@', cursor_factory= RealDictCursor)  
            # cursor_factory= RealDictCursor ==> It maps the columns with the values

            cursor  = conn.cursor()
            print("Database Connected Sucessfully")
            break 

        except Exception as error:
         print("Connecting to Database Failed")
         print("Error: ", error)

         time.sleep(2) # For every 2 second server try to connect with database 



my_post = [post(Title='INDIA', content='INDIA IS A BEAUTIFUL COUNTRY', published=True, rating=None, id = 1),
            post(Title='Nepal', content='Nepal IS A Neighbor COUNTRY of india', published=True, rating=3, id =2)]

@app.get('/')
def root():
    return {"message":"Hello world"}


@app.get('/posts')
def get_post():
    cursor.execute(""" SELECT * FROM posts""")
    posts = cursor.fetchall()
    return{"message": posts}

@app.post('/createpost', status_code = status.HTTP_201_CREATED)
def create_post(pos: post): 
    cursor.execute(""" INSERT INTO posts (title,content, published, rating) VALUES (%s,%s,%s,%s) RETURNING *""",
                   (pos.Title, pos.content, pos.published, pos.rating))
    
    new_post = cursor.fetchone()
    conn.commit()
    
    return{"message": new_post}


@app.get('/posts/{post_id}')
def get_one_post(post_id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (post_id,))
    post_id_data = cursor.fetchone()

    if post_id_data is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    return{"message": post_id_data}



@app.delete("/delete_posts/{id}", status_code=status.HTTP_200_OK)
def delete_post(id: int):
    cursor.execute(
        "DELETE FROM posts WHERE id = %s RETURNING *",
        (id,)
    )

    deleted_id_post = cursor.fetchone()
    conn.commit()

    if deleted_id_post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    return {"message": deleted_id_post}



@app.put('/posts_update/{id}')
def update_post(id: int, posts:post):
    cursor.execute(
        "UPDATE posts SET title = %s, content = %s, published = %s, rating = %s WHERE id = %s RETURNING *",
        (posts.Title, posts.content, posts.published, posts.rating, id)
    )

    updated_post = cursor.fetchone()
    conn.commit()

    if  updated_post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    return {"message":  updated_post}


# run : fastapi dev main.py
# or 
# uvicorn main:app --reload