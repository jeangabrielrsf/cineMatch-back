from http import HTTPStatus

from fastapi import FastAPI

from cinematch_back.routers import auth, movies, users
from cinematch_back.schemas import Message

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(movies.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def health_check():
    return {'message': 'Server running OK!'}
