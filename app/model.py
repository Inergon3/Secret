import datetime
from importlib.metadata import metadata

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import as_declarative, Mapped, mapped_column


@as_declarative(metadata=metadata)
class AbstractModel:
    pass


class SecretModel(AbstractModel):
    __tablename__ = "secret"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    secret: Mapped[str] = mapped_column()
    passphrase: Mapped[str] = mapped_column(unique=True)
    secret_key: Mapped[str] = mapped_column(unique=True)


class AddSecretModel(AbstractModel):
    __tablename__ = "add_secret"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_secret: Mapped[int] = mapped_column(ForeignKey("secret.id"))
    time_added: Mapped[datetime.datetim] = mapped_column(DateTime(timezone=True))
    ip_address: Mapped[str] = mapped_column()


class GetSecretModel(AbstractModel):
    __tablename__ = "get_secret"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_secret: Mapped[int] = mapped_column(ForeignKey("secret.id"))
    time_get: Mapped[datetime.datetim] = mapped_column(DateTime(timezone=True))
    ip_address: Mapped[str] = mapped_column()


class DeliteSecretModel(AddSecretModel):
    __tablename__ = "delite_secret"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_secret: Mapped[int] = mapped_column(ForeignKey("secret.id"))
    time_delite: Mapped[datetime.datetim] = mapped_column(DateTime(timezone=True))
    ip_address: Mapped[str] = mapped_column()
