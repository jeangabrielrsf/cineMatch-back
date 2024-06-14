from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from cinematch_back.database import get_session
from cinematch_back.models import User
from cinematch_back.schemas import UserList, UserPublic, UserSchema
from cinematch_back.security import get_current_user, get_password_hash

router = APIRouter(prefix='/users', tags=['users'])

CurrentSession = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


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

    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email, username=user.username, password=hashed_password
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.get('/', status_code=HTTPStatus.OK, response_model=UserList)
def list_users(session: CurrentSession, skip: int = 0, limit: int = 50):
    users = session.scalars(select(User).offset(skip).limit(limit)).all()

    return {'users': users}


@router.put('/{user_id}', response_model=UserPublic)
def update_user(
    session: CurrentSession,
    user: UserSchema,
    user_id: int,
    current_user: CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail='Not enough permissions'
        )

    current_user.username = (user.username,)
    current_user.email = (user.email,)
    current_user.password = get_password_hash(user.password)

    session.commit()
    session.refresh(current_user)

    return current_user
