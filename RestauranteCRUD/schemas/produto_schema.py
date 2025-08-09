from pydantic import BaseModel
from typing import Optional

class ProdutoSchema(BaseModel):
    id: int
    nome: str
    preco: float

    class Config:
        from_attributes = False
