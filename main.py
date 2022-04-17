from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


dummy_posts = [{'id': 1, 'title': 'first Post', 'content': 'there is no content'}, {
    'id': 2, 'title': 'second post', 'content': 'still no post'}]


def find_post(id):
    for index, post in enumerate(dummy_posts):
        if post['id'] == id:
            return index, post

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"post with {id} not founded")


@app.get('/')
def main():
    return {'message': "server is running!"}


@app.get('/posts')
def posts():
    return {'data': dummy_posts}


@app.get('/posts/{id}')
def get_post(id: int):
    _, post = find_post(id)
    return {'data': post}


@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    dummy_posts.append(post.dict())
    return {'data': post}


@app.put('/posts/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_post(id: int, post: Post):
    index, _ = find_post(id)
    post_dict = post.dict()
    post_dict['id'] = id
    dummy_posts[index] = post_dict
    return {'data': post}


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    post_index, post = find_post(id)
    dummy_posts.pop(post_index)
    return {'data': post}
