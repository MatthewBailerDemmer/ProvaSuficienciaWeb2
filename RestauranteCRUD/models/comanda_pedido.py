from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base, engine

class ComandaPedido(Base):
    __tablename__ = 'comanda_pedido'

    id = Column(Integer, primary_key=True, autoincrement=True)
    IdComanda= Column(Integer, ForeignKey('comanditas.id'))
    IdProduto = Column(Integer, ForeignKey('produtos.id'))

    comanda = relationship("Comanda", back_populates="comanditita")
    produto = relationship("Produto", back_populates="peditito")

