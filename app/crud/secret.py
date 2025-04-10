import datetime
import uuid

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import cipher
from app.model import SecretModel, AddSecretModel, GetSecretModel, DeleteSecretModel


class Secret():
    async def add(self, secret_str: str, passphrase: str, ip_address: str, db: AsyncSession):
        secret_key = uuid.uuid4()
        secret_str_cod = cipher.encrypt(secret_str.encode())
        secret = SecretModel(secret=secret_str_cod, passphrase=passphrase, secret_key=secret_key, get_secret=False,
                             del_secret=False)
        db.add(secret)
        await db.commit()
        await add_in_add_secret_model(secret_key, ip_address, db)
        return {
            "secret_key": secret_key
        }

    async def get(self, secret_key: uuid.UUID, ip_address: str, db: AsyncSession):
        secret = await get_secret(secret_key, db)
        if secret.get_secret == True:
            raise HTTPException(status_code=400, detail="Error, secret geted")
        await availability_secret(secret)
        await add_in_get_secret_model(secret_key, ip_address, db)
        response = cipher.decrypt(secret.secret).decode()
        secret.get_secret = True
        await db.commit()
        return {
            "secret": response
        }

    async def delete(self, secret_key: uuid.UUID, passphrase: str, ip_address: str, db: AsyncSession):
        secret = await get_secret(secret_key, db)
        await availability_secret(secret)
        if secret.passphrase != passphrase:
            raise HTTPException(status_code=400, detail="Error passphrase")
        if secret.del_secret == True:
            raise HTTPException(status_code=400, detail="Error, secret deleted")
        await add_in_delete_secret_model(secret_key, ip_address, db)
        secret.del_secret = True
        await db.commit()
        return {
            "status": "secret deleted"
        }


async def add_in_add_secret_model(secret_key: uuid.UUID, ip_address: str, db: AsyncSession):
    stmt = select(SecretModel).where(SecretModel.secret_key == secret_key)
    result = await db.execute(stmt)
    secret = result.scalars().first()
    log = AddSecretModel(id_secret=secret.id, time_added=datetime.datetime.now(), ip_address=ip_address)
    db.add(log)
    await db.commit()
    return True


async def add_in_get_secret_model(secret_key: uuid.UUID, ip_address: str, db: AsyncSession):
    stmt = select(SecretModel).where(SecretModel.secret_key == secret_key)
    result = await db.execute(stmt)
    secret = result.scalars().first()
    log = GetSecretModel(id_secret=secret.id, time_get=datetime.datetime.now(), ip_address=ip_address)
    db.add(log)
    await db.commit()
    return True


async def add_in_delete_secret_model(secret_key: uuid.UUID, ip_address: str, db: AsyncSession):
    stmt = select(SecretModel).where(SecretModel.secret_key == secret_key)
    result = await db.execute(stmt)
    secret = result.scalars().first()
    log = DeleteSecretModel(id_secret=secret.id, time_delited=datetime.datetime.now(), ip_address=ip_address)
    db.add(log)
    await db.commit()
    return True


async def availability_secret(secret):
    if secret is None:
        raise HTTPException(status_code=404, detail="Secret not found")
    return secret

async def get_secret(secret_key, db: AsyncSession):
    stmt = select(SecretModel).where(SecretModel.secret_key == secret_key)
    result = await db.execute(stmt)
    secret = result.scalars().first()
    return secret
