from sqlalchemy import Column, String, Integer
from db.database import Base, engine
from sqlalchemy.orm import relationship
class Usuario(Base):
    __tablename__ = 'usuarios'

    idUsuario = Column(Integer, primary_key=True, autoincrement=True)
    nomeUsuario = Column(String(50), nullable=False)
    telefoneUsuario = Column(String(14))

    comanda = relationship("Comanda", back_populates="user")