from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas.produto_schema import ProdutoSchema
from db.database import get_db
from utils.respotas import resposta_api
from DAO.produtoDAO import ProdutoDAO
from contollers.authentification_controller import authenticate_user

router = APIRouter()

@router.post("/")
def criar_produto(produto: ProdutoSchema, db: Session = Depends(get_db), token=Depends(authenticate_user)):
    try:
        dao = ProdutoDAO(db)
        novo_produto = dao.criar_produto(produto)
        return resposta_api(data=novo_produto, message="Usuario criado com sucesso")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{id}")
def get_produto(id: str, db: Session = Depends(get_db),token=Depends(authenticate_user)):
    try:
        dao = ProdutoDAO(db)
        id_produto = int(id)
    except:
        raise HTTPException(status_code=400, detail="Id invalida")

    produto_achado = dao.get_produto(id_produto)
    if produto_achado is None:
        return resposta_api(data=produto_achado, message="Usuario nao encontrado")
    return resposta_api(data=produto_achado, message="Usuario achado com sucesso")

@router.get("/")
def get_all_products(db: Session = Depends(get_db), token=Depends(authenticate_user)):
    try:
        dao = ProdutoDAO(db)
        produtos = dao.get_todos_produtos()
        return resposta_api(data=produtos, message="Produtos achados com sucesso")
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))