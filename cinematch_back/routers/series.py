import random
from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from cinematch_back.database import get_session
from cinematch_back.models import Serie, User
from cinematch_back.schemas import SerieList, SeriePublic, SerieSchema
from cinematch_back.security import get_current_user
from cinematch_back.service import get_recommendation_series_by_id

router = APIRouter(prefix='/series', tags=['series'])

CurrentSession = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', status_code=HTTPStatus.OK, response_model=SeriePublic)
def include_liked_serie(
    serie: SerieSchema, user: CurrentUser, session: CurrentSession
):
    db_serie = Serie(
        name=serie.name,
        overview=serie.overview,
        tmdb_id=serie.tmdb_id,
        popularity=serie.popularity,
        vote_average=serie.vote_average,
        vote_count=serie.vote_count,
        user_id=user.id,
        first_air_date=serie.first_air_date,
        poster_path=serie.poster_path
    )

    session.add(db_serie)
    session.commit()
    session.refresh(db_serie)

    return db_serie


@router.get('/', status_code=HTTPStatus.OK, response_model=SerieList)
def list_liked_series(
    session: CurrentSession,
    user: CurrentUser,
    name: str = Query(None),
    offset: int = Query(None),
    limit: int = Query(None),
):
    query = select(Serie).where(Serie.user_id == user.id)

    if name:
        query = query.filter(Serie.name.contains(name))

    series = session.scalars(query.offset(offset).limit(limit)).all()

    return {'liked_series': series}


@router.get('/recommendations', status_code=HTTPStatus.OK)
def list_recommended_series(session: CurrentSession, user: CurrentUser):
    query = select(Serie).where(Serie.user_id == user.id)

    series = session.scalars(query).all()
    if len(series) == 0:
        return series
    final_list: SerieList = []
    for serie in series:
        recommended_list = get_recommendation_series_by_id(serie.tmdb_id)
        for item in recommended_list['results']:
            if item['name'] in final_list or item['name'] in series:
                continue
            final_list.append(item)
    
    random.shuffle(final_list)

    return final_list[0:5]
