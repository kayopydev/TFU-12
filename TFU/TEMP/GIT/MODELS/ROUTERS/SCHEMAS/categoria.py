# -*- coding: utf-8 -*-
"""Schemas (Pydantic) de entrada e saída para Categoria."""

from typing import List, Optional

from pydantic import BaseModel, Field


class CategoriaBase(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100)
    descricao: Optional[str] = Field(None, max_length=255)


class CategoriaCreate(CategoriaBase):
    """Dados recebidos para cadastrar uma categoria."""
    pass


class CategoriaUpdate(CategoriaBase):
    """Dados recebidos para atualizar uma categoria."""
    pass


class CategoriaResponse(CategoriaBase):
    """Dados devolvidos pela API ao consultar uma categoria."""
    id_categoria: int

    class Config:
        from_attributes = True


class ProdutoResumo(BaseModel):
    """Versão resumida do produto, usada dentro da resposta da categoria."""
    id_produto: int
    nome: str
    preco: float
    estoque: int

    class Config:
        from_attributes = True


class CategoriaComProdutos(CategoriaResponse):
    """Categoria + lista de produtos (resposta aninhada)."""
    produtos: List[ProdutoResumo] = []

    class Config:
        from_attributes = True
