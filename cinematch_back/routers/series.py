from typing import Annotated
from http import HTTPStatus
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import select

from cinematch_back.database import get_session
from cinematch_back.models import User, Serie
from cinematch_back.schemas import SerieSchema, SeriePublic, SerieList
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
        user_id=user.id
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
    limit: int = Query(None)
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
    final_list: SerieList= []
    for serie in series:
        recommended_list = get_recommendation_series_by_id(serie.id)
        for item in recommended_list['results']:
            if item['name'] in final_list or item['name'] in series:
                continue
            new_serie = Serie(
                name=item['name'],
                overview=item['overview'],
                tmdb_id=item['id'],
                popularity=item['popularity'],
                vote_average=item['vote_average'],
                vote_count=item['vote_count'],
                user_id=user.id,
            )
            final_list.append(new_serie)

    return final_list