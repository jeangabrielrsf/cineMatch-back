from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from cinematch_back.database import get_session
from cinematch_back.models import Movie, User
from cinematch_back.schemas import MovieList, MoviePublic, MovieSchema
from cinematch_back.security import get_current_user

router = APIRouter(prefix='/movies', tags=['movies'])

CurrentSession = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=MoviePublic)
def include_liked_movie(
    movie: MovieSchema, user: CurrentUser, session: CurrentSession
):
    db_movie = Movie(
        title=movie.title,
        overview=movie.overview,
        tmdb_id=movie.tmdb_id,
        popularity=movie.popularity,
        vote_average=movie.vote_average,
        vote_count=movie.vote_count,
        user_id=user.id,
    )

    session.add(db_movie)
    session.commit()
    session.refresh(db_movie)

    return db_movie


@router.get('/', status_code=HTTPStatus.OK, response_model=MovieList)
def list_liked_movies(
    session: CurrentSession,
    user: CurrentUser,
    title: str = Query(None),
    offset: int = Query(None),
    limit: int = Query(None),
):
    query = select(Movie).where(Movie.user_id == user.id)

    if title:
        query = query.filter(Movie.title.contains(title))

    movies = session.scalars(query.offset(offset).limit(limit)).all()

    return {'liked_movies': movies}
