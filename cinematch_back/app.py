from http import HTTPStatus

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from cinematch_back.routers import auth, movies, series, users
from cinematch_back.schemas import Message

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(movies.router)
app.include_router(series.router)

origins = [
    "http://localhost",
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def health_check():
    return {'message': 'Server running OK!'}
