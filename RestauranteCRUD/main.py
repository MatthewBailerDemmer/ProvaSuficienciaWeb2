import uvicorn
from fastapi import FastAPI
from contollers.usuario_controller import router as usuario_router
from contollers.produto_controller import router as produto_router
from contollers.comanda_controller import router as comanda_router
from contollers.authentification_controller import router as auth_router
from db.database import Base, engine
from models.usuario import Usuario
from models.produto import Produto
from models.comanda import Comanda
from models.comanda_pedido import ComandaPedido
from models.usuarioAdmin import UsuarioAdmin

app = FastAPI()

app.include_router(usuario_router, prefix="/api/usuario", tags=["Users"])
app.include_router(produto_router, prefix="/api/produto", tags=["Products"])
app.include_router(comanda_router, prefix="/api/comanda", tags=["Comands"])
app.include_router(auth_router, prefix="/api/auth", tags=["Authentics"])

@app.get("/")
def root():
    return {"message": "Hellow, world. Bevindo a API do restaurante do Matheus"}

Base.metadata.create_all(engine)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)