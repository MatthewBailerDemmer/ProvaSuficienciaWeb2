from sqlalchemy.orm import Session
from models.comanda import Comanda
from models.comanda_pedido import ComandaPedido
from schemas.comanda_schema import ComandaSchema, ComandaSchemaUpdate
from DAO.usuarioDAO import UserDao
from DAO.produtoDAO import ProdutoDAO
from schemas.produto_schema import ProdutoSchema
from typing import List

class ComandaDAO:
    def __init__(self, db: Session):
        self.db = db


    def criar_comanda(self, comanda: ComandaSchema) -> ComandaSchema:
        userDao = UserDao(self.db)
        user_achado = userDao.get_usuario(comanda.idUsuario)
        if user_achado is None:
            raise ValueError("Usuário não encontrado")
        else:
            if user_achado.nomeUsuario != comanda.nomeUsuario:
                raise ValueError("Nome de usuário diferente do cadastrado")
            elif user_achado.telefoneUsuario != comanda.telefoneUsuario:
                raise ValueError("Telefone de usuário diferente do cadastrado")

        for produto in comanda.produtos:
            produtoDAO = ProdutoDAO(self.db)
            produto_achado = produtoDAO.get_produto(produto.id)
            if produto_achado is None:
                raise ValueError("Produto não encontrado")
            else:
                if produto_achado.nome != produto.nome:
                    raise ValueError("Nome de produto diferente do cadastrado")
                elif produto_achado.preco != produto.preco:
                    raise ValueError("Preco de produto diferente do cadastrado")


        db_Comanda = Comanda(IdUsuario=comanda.idUsuario)
        self.db.add(db_Comanda)
        self.db.commit()
        self.db.refresh(db_Comanda)

        for produto in comanda.produtos:
            db_comandaPedido = ComandaPedido(IdProduto=produto.id, IdComanda=db_Comanda.id)
            self.db.add(db_comandaPedido)
            self.db.commit()
            self.db.refresh(db_comandaPedido)

        return comanda

    def get_all_comandas(self):
        comandas = self.db.query(Comanda).all()
        resultComandas = []
        userDao = UserDao(self.db)
        produtoDao = ProdutoDAO(self.db)
        for comanda in comandas:
            usuarioComanda = userDao.get_usuario(comanda.IdUsuario)

            pedidosComandaList = []
            pedidosComanda = self.db.query(ComandaPedido).filter(ComandaPedido.IdComanda == comanda.id)
            for pedidoComanda in pedidosComanda:
                pedido = produtoDao.get_produto(pedidoComanda.IdProduto)
                if pedido is not None:
                    pedidosComandaList.append(ProdutoSchema(id=pedido.id, nome=pedido.nome, preco=pedido.preco))

            resultComandas.append(ComandaSchema(id=comanda.id, idUsuario=usuarioComanda.idUsuario, nomeUsuario=usuarioComanda.nomeUsuario, telefoneUsuario=usuarioComanda.telefoneUsuario, produtos=pedidosComandaList))

        return resultComandas

    def get_comanda(self, id: int):
        comanda = self.db.query(Comanda).filter(Comanda.id == id).first()
        if comanda is None:
            raise ValueError("Comanda não econtrada")
        userDao = UserDao(self.db)
        usuario = userDao.get_usuario(comanda.IdUsuario)

        produtoDao = ProdutoDAO(self.db)

        pedidosList = []
        pedidosComanda = self.db.query(ComandaPedido).filter(ComandaPedido.IdComanda == comanda.id)
        for pedidoComanda in pedidosComanda:
            pedido = produtoDao.get_produto(pedidoComanda.IdProduto)
            pedidosList.append(ProdutoSchema(id=pedido.id, nome=pedido.nome, preco=pedido.preco))

        return ComandaSchema(idUsuario=usuario.idUsuario, nomeUsuario=usuario.nomeUsuario, telefoneUsuario=usuario.telefoneUsuario, produtos=pedidosList)


    def delete_comanda(self, id: int):
        comanda = self.db.query(Comanda).filter(Comanda.id == id).first()
        if comanda is None:
            raise ValueError("Comanda não econtrada")

        pedidosComanda = self.db.query(ComandaPedido).filter(ComandaPedido.IdComanda == comanda.id)
        for pedidoComanda in pedidosComanda:
            self.db.delete(pedidoComanda)
            self.db.commit()

        self.db.delete(comanda)
        self.db.commit()
        return comanda

    def update_comanda(self, id: int, comandaSch: ComandaSchemaUpdate):
        comanda = self.db.query(Comanda).filter(Comanda.id == id).first()
        alteracao = False
        if comanda is None:
            raise ValueError("Comanda não econtrada")
        for pedido in comandaSch.produtos:
            db_comandaItem = ComandaPedido(IdProduto=pedido.id, IdComanda=id)
            self.db.add(db_comandaItem)
            self.db.commit()
            self.db.refresh(db_comandaItem)
            alteracao = True

        return alteracao

