from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from cinematch_back.database import get_session
from cinematch_back.models import User
from cinematch_back.schemas import UserPublic, UserSchema

router = APIRouter(prefix='/users', tags=['users'])

CurrentSession = Annotated[Session, Depends(get_session)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: CurrentSession):
    db_user = session.scalar(
        select(User).where(
            or_(User.email == user.email, User.username == user.username)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Username already exists',
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Email already exists',
            )

    db_user = User(
        email=user.email, username=user.username, password=user.password
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user