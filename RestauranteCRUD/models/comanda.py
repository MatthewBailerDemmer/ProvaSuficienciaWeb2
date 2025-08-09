from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base, engine

class Comanda(Base):
    __tablename__ = 'comanditas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    IdUsuario = Column(Integer, ForeignKey('usuarios.idUsuario'))

    user = relationship("Usuario", back_populates="comanda")
    comanditita = relationship("ComandaPedido", back_populates="comanda")


