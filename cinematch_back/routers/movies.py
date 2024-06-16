import json
from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from cinematch_back.database import get_session
from cinematch_back.models import Movie, User
from cinematch_back.schemas import MovieList, MoviePublic, MovieSchema
from cinematch_back.security import get_current_user
from cinematch_back.service import get_recommendation_by_id

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


@router.get('/recommendations', status_code=HTTPStatus.OK)
def list_recommended_movies(session: CurrentSession, user: CurrentUser):
    query = select(Movie).where(Movie.user_id == user.id)

    movies = session.scalars(query).all()
    final_list: MovieList = []
    for movie in movies:
        print('entrei no movie')
        print(json.dumps(movie))
        recommended_list = get_recommendation_by_id(movie.id)
        print(f'RECOMENDAÇÕES DO {movie.title}')
        for item in recommended_list['results']:
            print(item['media_type'])
            if item['title'] in final_list or item['title'] in movies:
                continue
            new_movie = Movie(
                title=item['title'],
                overview=item['overview'],
                tmdb_id=item['id'],
                popularity=item['popularity'],
                vote_average=item['vote_average'],
                vote_count=item['vote_count'],
                user_id=user.id,
            )
            final_list.append(new_movie)

    return final_list
