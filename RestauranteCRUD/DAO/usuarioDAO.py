from sqlalchemy.orm import Session
from models.usuario import Usuario
from models.usuarioAdmin import UsuarioAdmin
from schemas.usuario_schema import UsuarioSchema, UserAdminSchema

class UserDao:
    def __init__(self, db: Session):
        self.db = db


    def criar_usuario(self, user: UsuarioSchema) -> Usuario:
        db_usuario = Usuario(nomeUsuario=user.nomeUsuario, telefoneUsuario=user.telefoneUsuario)
        self.db.add(db_usuario)
        self.db.commit()
        self.db.refresh(db_usuario)
        return db_usuario

    def get_usuario(self, id: int):
        user = self.db.query(Usuario).filter(Usuario.idUsuario == id).first()
        return user

    def get_todos_usuarios(self):
        return self.db.query(Usuario).all()

    def criar_usuario_admin(self, user: UserAdminSchema):
        db_usuario = UsuarioAdmin(username=user.username, password=user.password)
        self.db.add(db_usuario)
        self.db.commit()
        self.db.refresh(db_usuario)
        return db_usuario

    def get_usuario_admin(self, username: str, password: str):
        user = self.db.query(UsuarioAdmin).filter(UsuarioAdmin.username == username, UsuarioAdmin.password == password).first()
        return user