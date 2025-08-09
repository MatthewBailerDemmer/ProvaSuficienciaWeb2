from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from schemas.comanda_schema import ComandaSchema, ComandaSchemaUpdate
from db.database import get_db
from utils.respotas import resposta_api
from DAO.comandaDAO import ComandaDAO
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from schemas.usuario_schema import UserAdminSchema
from DAO.usuarioDAO import UserDao

oauth_scheme = OAuth2PasswordBearer(tokenUrl="token")

meu_token = 'oi'

SECRET_KEY = "matheuz"
ALGORITHM = "HS256"

router = APIRouter()

@router.post("/signUp")
def signup(credenciais: UserAdminSchema, db: Session = Depends(get_db)):
    try:
        dao = UserDao(db)
        usuarioAdimin = dao.criar_usuario_admin(credenciais)
        return resposta_api(status=200, message="Usuario criado com sucesso")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
def login(credenciais: UserAdminSchema, db: Session = Depends(get_db)):
    dao = UserDao(db)
    usuarioAdimin = dao.get_usuario_admin(credenciais.username, credenciais.password)
    if usuarioAdimin is None:
        raise HTTPException(status_code=401, detail="Usuário ou senha inválidos")

    # Gera o token
    access_token = criate_token(data={"sub": credenciais.username})
    return {"access_token": access_token, "token_type": "bearer"}
def authenticate_user(token: str = Depends(oauth_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
        return username
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido ou expirado")

def criate_token(data: dict):
    encode_data = data.copy()
    expire = datetime.utcnow() + (timedelta(minutes=30))
    encode_data.update({"expira": expire.timestamp()})
    encoded_jwt = jwt.encode(encode_data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

