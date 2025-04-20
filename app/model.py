import datetime
import uuid
from typing import AsyncGenerator

from sqlalchemy import DateTime, ForeignKey, MetaData, LargeBinary, UUID
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import as_declarative, Mapped, mapped_column

from app.config import SQLALCHEMY_DATABASE_URL

metadata = MetaData()
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


@as_declarative(metadata=metadata)
class AbstractModel:
    pass


class SecretModel(AbstractModel):
    __tablename__ = "secrets"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    secret: Mapped[bytes] = mapped_column(LargeBinary)
    passphrase: Mapped[str] = mapped_column()
    secret_key: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False
    )
    get_secret: Mapped[bool] = mapped_column()
    del_secret: Mapped[bool] = mapped_column()

    def __repr__(self):
        return (
            f"SecretModel("
            f"id={self.id!r}, "
            f"passphrase={self.passphrase!r}, "
            f"secret_key={self.secret_key!r}, "
            f"get_secret={self.get_secret!r}, "
            f"del_secret={self.del_secret!r}"
            f")"
        )


class AddSecretModel(AbstractModel):
    __tablename__ = "add_secrets"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_secret: Mapped[int] = mapped_column(ForeignKey("secrets.id"), nullable=False)
    time_added: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))
    ip_address: Mapped[str] = mapped_column()


class GetSecretModel(AbstractModel):
    __tablename__ = "get_secrets"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_secret: Mapped[int] = mapped_column(ForeignKey("secrets.id"), nullable=False)
    time_get: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))
    ip_address: Mapped[str] = mapped_column()


class DeleteSecretModel(AbstractModel):
    __tablename__ = "delete_secrets"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_secret: Mapped[int] = mapped_column(ForeignKey("secrets.id"), nullable=False)
    time_delited: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))
    ip_address: Mapped[str] = mapped_column()
