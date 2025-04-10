from uuid import UUID

from pydantic import BaseModel


class AddSecret(BaseModel):
    secret: str
    passphrase: str
    ttl_seconds: int
