from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas.comanda_schema import ComandaSchema, ComandaSchemaUpdate
from db.database import get_db
from utils.respotas import resposta_api
from DAO.comandaDAO import ComandaDAO
from contollers.authentification_controller import authenticate_user

router = APIRouter()



@router.post("/")
def criar_comanda(comanda: ComandaSchema, db: Session = Depends(get_db), token=Depends(authenticate_user)):
    try:
        comandaDAO = ComandaDAO(db)
        nova_comanda = comandaDAO.criar_comanda(comanda)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return resposta_api(data=nova_comanda, message="Comanda criado com sucesso")

@router.get("/")
def get_comandas(db: Session = Depends(get_db), token=Depends(authenticate_user)):
    try:
        comandaDAO = ComandaDAO(db)
        comandas = comandaDAO.get_all_comandas()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return resposta_api(data=comandas, message="Comandas encontradas com sucesso")

@router.get("/{id}")
def get_comanda(id: str, db: Session = Depends(get_db), token=Depends(authenticate_user)):
    dao = ComandaDAO(db)
    try:
        id_comanda = int(id)
    except:
        raise HTTPException(status_code=400, detail="Id invalida")
    comanda_achada = None
    try:
        comanda_achada = dao.get_comanda(id_comanda)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    if comanda_achada is None:
        raise HTTPException(status_code=404, detail='Comanda não encontrada')
    return resposta_api(data=comanda_achada, message="Comanda achada com sucesso")

@router.delete("/{id}")
def delete_comanda(id: str, db: Session = Depends(get_db), token=Depends(authenticate_user)):
    dao = ComandaDAO(db)
    try:
        id_comanda = int(id)
    except:
        raise HTTPException(status_code=400, detail="Id invalida")

    try:
        dao.delete_comanda(id_comanda)
    except:
        raise HTTPException(status_code=404, detail="Comanda não econtrada")
    objcetReturn = {
        "sucess": {
            "text": "comanda removida"
        }
    }
    return resposta_api(data=objcetReturn)

@router.put("/{id}")
def update_comanda(id: str, comandaSch: ComandaSchemaUpdate, db: Session = Depends(get_db), token=Depends(authenticate_user)):
    dao = ComandaDAO(db)
    try:
        id_comanda = int(id)
    except:
        raise HTTPException(status_code=400, detail="Id invalida")

    try:
        resultado = dao.update_comanda(id_comanda, comandaSch)
        if resultado:
            objcetReturn = {
                "sucess": {
                    "text": "Comanda Atualizada com sucesso"
                }
            }
            return resposta_api(data=objcetReturn)
        else:
            objcetReturn = {
                "sucess": {
                    "text": "Nenhuma comanda atualizada"
                }
            }
            return resposta_api(data=objcetReturn)

    except:
        raise HTTPException(status_code=400, detail="Falha ao editar comanda")
