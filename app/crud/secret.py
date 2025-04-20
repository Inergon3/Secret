import datetime
import uuid

from fastapi import HTTPException, BackgroundTasks
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import cipher
from app.model import SecretModel, AddSecretModel, GetSecretModel, DeleteSecretModel
from app.redis.redis_client import redis


class Secret():

    async def add(self, secret_str: str, passphrase: str, ip_address: str, ttl_seconds,  db: AsyncSession):
        secret_key = uuid.uuid4()
        secret_str_cod = cipher.encrypt(secret_str.encode())
        if ttl_seconds == 0:
            raise HTTPException(status_code=400, detail="ttl cant zero")
        await redis.set(str(secret_key), secret_str_cod, ex=ttl_seconds)
        secret = SecretModel(secret=secret_str_cod, passphrase=passphrase, secret_key=secret_key, get_secret=False,
                             del_secret=False)
        db.add(secret)
        await db.commit()
        await add_in_add_secret_model(secret_key, ip_address, db)
        return {
            "secret_key": secret_key
        }

    async def get(self, secret_key: uuid.UUID, ip_address: str, db: AsyncSession):
        redis_secret = await redis.get(str(secret_key))
        if redis_secret is None:
            secret = await get_secret(secret_key, db)
            await check_secret(secret)
            await deletion_check(secret)
            await check_receipt(secret)
            response = cipher.decrypt(secret.secret).decode()
        if redis_secret is not None:
            response = cipher.decrypt(redis_secret).decode()
            await redis.delete(str(secret_key))
        #await add_in_get_secret_model(secret_key, ip_address, db)
        return {
            "secret": response
        }

    async def delete(self, secret_key: uuid.UUID, passphrase: str, ip_address: str, db: AsyncSession):
        secret = await get_secret(secret_key, db)
        await check_secret(secret)
        if secret.passphrase != passphrase:
            raise HTTPException(status_code=400, detail="Error passphrase")
        await deletion_check(secret)
        redis_secret = await redis.get(str(secret_key))
        if redis_secret is not None:
            await redis.delete(str(secret_key))
        secret.del_secret = True
        await db.commit()
        await add_in_delete_secret_model(secret_key, ip_address, db)
        return {
            "status": "secret deleted"
        }

    async def get_all(self, db):
        stmt = select(SecretModel)
        result = await db.execute(stmt)
        secrets = result.scalars().all()
        return secrets


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


async def check_secret(secret):
    if secret is None:
        raise HTTPException(status_code=404, detail="Secret not found")
    return secret


async def get_secret(secret_key, db: AsyncSession):
    stmt = select(SecretModel).where(SecretModel.secret_key == secret_key)
    result = await db.execute(stmt)
    secret = result.scalars().first()
    return secret


async def deletion_check(secret):
    if secret.del_secret == True:
        raise HTTPException(status_code=400, detail="Error, secret deleted")
    return secret


async def check_receipt(secret):
    if secret.get_secret == True:
        raise HTTPException(status_code=400, detail="Error, secret geted")


async def update_get_secret(secret_key, db: AsyncSession):
    stmt = select(SecretModel).where(SecretModel.secret_key == secret_key)
    result = await db.execute(stmt)
    secret = result.scalars().first()
    secret.get_secret = True
    await db.commit()
    return True


