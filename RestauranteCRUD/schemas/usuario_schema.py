from pydantic import BaseModel
from typing import Optional

class UsuarioSchema(BaseModel):
    idUsuario: Optional[int] = None
    nomeUsuario: str
    telefoneUsuario: str

    class Config:
        from_attributes = False

class UserAdminSchema(BaseModel):
    username: str
    password: str
