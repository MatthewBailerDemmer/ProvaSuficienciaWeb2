from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas.usuario_schema import UsuarioSchema
from db.database import get_db
from utils.respotas import resposta_api
from DAO.usuarioDAO import UserDao
from contollers.authentification_controller import authenticate_user

router = APIRouter()

@router.post("/")
def criar_usuario(usuario: UsuarioSchema, db: Session = Depends(get_db), token=Depends(authenticate_user)):
    try:
        dao = UserDao(db)
        novo_usuario = dao.criar_usuario(usuario)
        return resposta_api(data=novo_usuario, message="Usuario criado com sucesso")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{id}")
def criar_usuario(id: str, db: Session = Depends(get_db), token=Depends(authenticate_user)):
    try:
        dao = UserDao(db)
        id_usuario = int(id)
        usuario_achado = dao.get_usuario(id_usuario)
        if usuario_achado is None:
            return HTTPException(status_code=400, detail="Usuario não encontrado")
        return resposta_api(data=usuario_achado, message="Usuario achado com sucesso")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/")
def get_all_users(db: Session = Depends(get_db), token=Depends(authenticate_user)):
    try:
        dao = UserDao(db)
        usuarios = dao.get_todos_usuarios()
        return resposta_api(data=usuarios, message="Usuarios achados com sucesso")
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))