# -*- coding: utf-8 -*-
"""Rotas de Categoria: CRUD completo."""

from typing import List

from fastapi import APIRouter, HTTPException, status

from database import SessionDep
from models.categoria import Categoria
from models.produto import Produto
from schemas.categoria import (
    CategoriaComProdutos,
    CategoriaCreate,
    CategoriaResponse,
    CategoriaUpdate,
)
from utils import obter_ou_404

router = APIRouter(prefix="/categorias", tags=["Categorias"])


@router.post("/", response_model=CategoriaResponse, status_code=status.HTTP_201_CREATED)
def criar_categoria(categoria: CategoriaCreate, db: SessionDep):
    """Cadastra uma nova categoria."""
    existente = db.query(Categoria).filter(Categoria.nome == categoria.nome).first()
    if existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Já existe uma categoria com esse nome.",
        )
    nova_categoria = Categoria(**categoria.model_dump())
    db.add(nova_categoria)
    db.commit()
    db.refresh(nova_categoria)
    return nova_categoria


@router.get("/", response_model=List[CategoriaResponse])
def listar_categorias(db: SessionDep):
    """Lista todas as categorias cadastradas."""
    return db.query(Categoria).all()


@router.get("/{id_categoria}", response_model=CategoriaComProdutos)
def buscar_categoria(id_categoria: int, db: SessionDep):
    """Busca uma categoria pelo id, já trazendo os produtos dela (resposta aninhada)."""
    return obter_ou_404(
        db, Categoria, id_categoria, Categoria.id_categoria, "Categoria não encontrada."
    )


@router.put("/{id_categoria}", response_model=CategoriaResponse)
def atualizar_categoria(id_categoria: int, dados: CategoriaUpdate, db: SessionDep):
    """Atualiza nome e descrição de uma categoria existente."""
    categoria = obter_ou_404(
        db, Categoria, id_categoria, Categoria.id_categoria, "Categoria não encontrada."
    )
    for campo, valor in dados.model_dump().items():
        setattr(categoria, campo, valor)
    db.commit()
    db.refresh(categoria)
    return categoria


@router.delete("/{id_categoria}", status_code=status.HTTP_204_NO_CONTENT)
def remover_categoria(id_categoria: int, db: SessionDep):
    """Remove uma categoria, desde que não existam produtos vinculados a ela."""
    categoria = obter_ou_404(
        db, Categoria, id_categoria, Categoria.id_categoria, "Categoria não encontrada."
    )
    produtos_vinculados = (
        db.query(Produto).filter(Produto.id_categoria == id_categoria).count()
    )
    if produtos_vinculados > 0:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Não é possível remover: existem produtos cadastrados nesta categoria.",
        )
    db.delete(categoria)
    db.commit()
