# Mapeando tabelas no banco de dados com SQLAlchemy
from datetime import datetime
from sqlalchemy.orm import Mapped, registry, mapped_column, relationship
from sqlalchemy import ForeignKey, func

table_registry = registry()

@table_registry.mapped_as_dataclass
class User:
    __tablename__= 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )
    