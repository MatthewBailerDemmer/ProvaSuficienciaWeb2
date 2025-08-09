from sqlalchemy import Column, String,Integer, Float
from db.database import Base, engine
from sqlalchemy.orm import relationship


class Produto(Base):
    __tablename__ = 'produtos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50), nullable=False)
    preco = Column(Float)

    peditito = relationship("ComandaPedido", back_populates="produto")
