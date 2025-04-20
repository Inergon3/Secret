from pydantic import BaseModel, Field


class AddSecret(BaseModel):
    secret: str
    passphrase: str
    ttl_seconds: int = 1
