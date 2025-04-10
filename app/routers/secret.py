import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from app.crud.secret import Secret
from app.model import get_db
from app.schemas import AddSecret

router = APIRouter(prefix="/secret", tags=["secret"])

secret = Secret()

@router.post("/")
async def add_secret(request: Request, message: AddSecret, db: AsyncSession = Depends(get_db)):
    ip_address = request.client.host
    return await secret.add(message.secret, message.passphrase, ip_address, db)

@router.get("/{secret_key}")
async def get_secret(request: Request, secret_key: uuid.UUID, db: AsyncSession = Depends(get_db)):
    ip_address = request.client.host
    return await secret.get(secret_key, ip_address, db)

@router.delete("/delete")
async def delite_secret(request: Request, secret_key: uuid.UUID, passphrase: str, db: AsyncSession = Depends(get_db)):
    ip_address = request.client.host
    return await secret.delete(secret_key, passphrase, ip_address, db)
