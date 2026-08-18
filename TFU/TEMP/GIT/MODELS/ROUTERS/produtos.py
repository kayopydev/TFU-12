# -*- coding: utf-8 -*-
"""Rotas de Produto: CRUD completo, sempre vinculado a uma Categoria."""

from typing import List, Optional

from fastapi import APIRouter, HTTPException, status

from database import SessionDep
from models.categoria import Categoria
from models.produto import Produto
from schemas.produto import ProdutoCreate, ProdutoResponse, ProdutoUpdate
from utils import obter_ou_404

router = APIRouter(prefix="/produtos", tags=["Produtos"])


@router.post("/", response_model=ProdutoResponse, status_code=status.HTTP_201_CREATED)
def criar_produto(produto: ProdutoCreate, db: SessionDep):
    """Cadastra um novo produto, vinculado a uma categoria já existente."""
    obter_ou_404(
        db, Categoria, produto.id_categoria, Categoria.id_categoria,
        "Categoria informada não existe.",
    )
    novo_produto = Produto(**produto.model_dump())
    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)
    return novo_produto


@router.get("/", response_model=List[ProdutoResponse])
def listar_produtos(db: SessionDep, id_categoria: Optional[int] = None):
    """Lista os produtos cadastrados. Pode filtrar por categoria (?id_categoria=1)."""
    consulta = db.query(Produto)
    if id_categoria is not None:
        consulta = consulta.filter(Produto.id_categoria == id_categoria)
    return consulta.all()


@router.get("/{id_produto}", response_model=ProdutoResponse)
def buscar_produto(id_produto: int, db: SessionDep):
    """Busca um produto pelo id, com os dados da categoria aninhados."""
    return obter_ou_404(
        db, Produto, id_produto, Produto.id_produto, "Produto não encontrado."
    )


@router.put("/{id_produto}", response_model=ProdutoResponse)
def atualizar_produto(id_produto: int, dados: ProdutoUpdate, db: SessionDep):
    """Atualiza um ou mais campos de um produto existente."""
    produto = obter_ou_404(
        db, Produto, id_produto, Produto.id_produto, "Produto não encontrado."
    )

    dados_informados = dados.model_dump(exclude_unset=True)

    if "id_categoria" in dados_informados:
        obter_ou_404(
            db, Categoria, dados_informados["id_categoria"], Categoria.id_categoria,
            "Categoria informada não existe.",
        )

    for campo, valor in dados_informados.items():
        setattr(produto, campo, valor)

    db.commit()
    db.refresh(produto)
    return produto


@router.delete("/{id_produto}", status_code=status.HTTP_204_NO_CONTENT)
def remover_produto(id_produto: int, db: SessionDep):
    """Remove um produto do catálogo."""
    produto = obter_ou_404(
        db, Produto, id_produto, Produto.id_produto, "Produto não encontrado."
    )
    db.delete(produto)
    db.commit()
