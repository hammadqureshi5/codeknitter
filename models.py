from datetime import datetime

from sqlalchemy import Boolean
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from database import Base



class Model(Base):

    __tablename__ = "models"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False
    )

    provider: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    provider_model: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )




class Product(Base):

    __tablename__ = "products"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False
    )
# api_key_hash: Mapped[str] = mapped_column(
    api_key: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False
    )

    active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )