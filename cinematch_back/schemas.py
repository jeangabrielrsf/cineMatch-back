# Arquivo de validação de dados de entrada/saída
from pydantic import BaseModel, ConfigDict, EmailStr


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: list[UserPublic]


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class MovieSchema(BaseModel):
    title: str
    overview: str
    tmdb_id: int
    popularity: float
    poster_path: str
    release_date: str
    vote_average: float
    vote_count: int


class MoviePublic(BaseModel):
    id: int
    title: str
    overview: str
    tmdb_id: int
    popularity: float
    poster_path: str
    release_date: str
    vote_average: float
    vote_count: int


class MovieList(BaseModel):
    liked_movies: list[MoviePublic]


class SerieSchema(BaseModel):
    name: str
    overview: str
    tmdb_id: int
    popularity: float
    poster_path: str
    first_air_date: str
    vote_average: float
    vote_count: int


class SeriePublic(BaseModel):
    id: int
    name: str
    overview: str
    tmdb_id: int
    popularity: float
    poster_path: str
    first_air_date: str
    vote_average: float
    vote_count: int


class SerieList(BaseModel):
    liked_series: list[SeriePublic]
