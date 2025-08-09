from pydantic import BaseModel
from typing import List
from schemas.produto_schema import ProdutoSchema
from typing import Optional

class ComandaSchema(BaseModel):
    id: Optional[int] = None
    idUsuario: int
    nomeUsuario: str
    telefoneUsuario: str
    produtos: List[ProdutoSchema]

    class Config:
        from_attributes = False

class ComandaSchemaUpdate(BaseModel):
    produtos: Optional[List[ProdutoSchema]] = None

    class Config:
        from_attributes = False