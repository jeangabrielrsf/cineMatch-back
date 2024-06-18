# Mapeando tabelas no banco de dados com SQLAlchemy
from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

table_registry = registry()


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )

    liked_movies: Mapped[list['Movie']] = relationship(
        init=False, back_populates='user', cascade='all, delete-orphan'
    )

    liked_series: Mapped[list['Serie']] = relationship(
        init=False, back_populates='user', cascade='all, delete-orphan'
    )


# filmes curtidos pelo usuário
@table_registry.mapped_as_dataclass
class Movie:
    __tablename__ = 'liked_movies'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    title: Mapped[str]
    overview: Mapped[str]
    tmdb_id: Mapped[int]
    popularity: Mapped[float]
    poster_path: Mapped[str]
    release_date: Mapped[str]
    vote_average: Mapped[float]
    vote_count: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    user: Mapped[User] = relationship(
        init=False, back_populates='liked_movies'
    )


@table_registry.mapped_as_dataclass
class Serie:
    __tablename__ = 'liked_series'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]
    overview: Mapped[str]
    tmdb_id: Mapped[int]
    popularity: Mapped[float]
    poster_path: Mapped[str]
    first_air_date: Mapped[str]
    vote_average: Mapped[float]
    vote_count: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    user: Mapped[User] = relationship(
        init=False, back_populates='liked_series'
    )
