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
    vote_average: float
    vote_count: int


class MoviePublic(BaseModel):
    id: int
    title: str
    overview: str
    tmdb_id: int
    popularity: float
    vote_average: float
    vote_count: int
