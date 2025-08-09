from sqlalchemy.orm import Session
from models.produto import Produto
from schemas.produto_schema import ProdutoSchema

class ProdutoDAO:
    def __init__(self, db: Session):
        self.db = db


    def criar_produto(self, product: ProdutoSchema) -> Produto:
        db_produto = Produto(nome=product.nome, preco=product.preco)
        self.db.add(db_produto)
        self.db.commit()
        self.db.refresh(db_produto)
        return db_produto

    def get_produto(self, id: int):
        produto = self.db.query(Produto).filter(Produto.id == id).first()
        return produto

    def get_todos_produtos (self):
        return self.db.query(Produto).all()