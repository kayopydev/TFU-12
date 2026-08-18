# -*- coding: utf-8 -*-
"""Schemas (Pydantic) de entrada e saída para Produto."""

from typing import Optional

from pydantic import BaseModel, Field


class ProdutoBase(BaseModel):
    nome: str = Field(..., min_length=2, max_length=150)
    marca: Optional[str] = Field(None, max_length=100)
    preco: float = Field(..., gt=0, description="Preço deve ser maior que zero")
    estoque: int = Field(..., ge=0, description="Estoque não pode ser negativo")
    id_categoria: int


class ProdutoCreate(ProdutoBase):
    """Dados recebidos para cadastrar um produto."""
    pass


class ProdutoUpdate(BaseModel):
    """Dados recebidos para atualizar um produto (todos os campos opcionais)."""
    nome: Optional[str] = Field(None, min_length=2, max_length=150)
    marca: Optional[str] = Field(None, max_length=100)
    preco: Optional[float] = Field(None, gt=0)
    estoque: Optional[int] = Field(None, ge=0)
    ativo: Optional[bool] = None
    id_categoria: Optional[int] = None


class CategoriaResumo(BaseModel):
    """Versão resumida da categoria, usada dentro da resposta do produto."""
    id_categoria: int
    nome: str

    class Config:
        from_attributes = True


class ProdutoResponse(BaseModel):
    """Dados devolvidos pela API ao consultar um produto (com a categoria aninhada)."""
    id_produto: int
    nome: str
    marca: Optional[str]
    preco: float
    estoque: int
    ativo: bool
    categoria: CategoriaResumo

    class Config:
        from_attributes = True
