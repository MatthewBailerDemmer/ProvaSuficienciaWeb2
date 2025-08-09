from sqlalchemy import Column, String, Integer
from db.database import Base, engine

class UsuarioAdmin(Base):
    __tablename__ = 'administradores'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(50), nullable=False)
