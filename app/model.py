import datetime

from sqlalchemy import DateTime, ForeignKey, MetaData
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import as_declarative, Mapped, mapped_column

from app.config import postgres_user, postgres_password, postgres_host, postgres_db

metadata = MetaData()
engine = create_async_engine(f"postgresql+asyncpg://{postgres_user}:{postgres_password}@{postgres_host}/{postgres_db}",
                             echo=True)
SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)


async def get_db() -> AsyncSession:
    async with SessionLocal() as session:
        yield session


@as_declarative(metadata=metadata)
class AbstractModel:
    pass


class SecretModel(AbstractModel):
    __tablename__ = "secrets"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    secret: Mapped[str] = mapped_column()
    passphrase: Mapped[str] = mapped_column(unique=True)
    secret_key: Mapped[str] = mapped_column(unique=True)
    get_secret: Mapped[bool] = mapped_column()
    del_secret: Mapped[bool] = mapped_column()


class AddSecretModel(AbstractModel):
    __tablename__ = "add_secrets"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_secret: Mapped[int] = mapped_column(ForeignKey("secret.id"))
    time_added: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))
    ip_address: Mapped[str] = mapped_column()


class GetSecretModel(AbstractModel):
    __tablename__ = "get_secrets"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_secret: Mapped[int] = mapped_column(ForeignKey("secret.id"))
    time_get: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))
    ip_address: Mapped[str] = mapped_column()


class DeliteSecretModel(AbstractModel):
    __tablename__ = "delite_secrets"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_secret: Mapped[int] = mapped_column(ForeignKey("secret.id"))
    time_delite: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))
    ip_address: Mapped[str] = mapped_column()
