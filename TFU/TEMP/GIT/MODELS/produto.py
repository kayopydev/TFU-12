# -*- coding: utf-8 -*-
"""Model da tabela produtos."""

from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Produto(Base):
    __tablename__ = "produtos"

    id_produto = Column(Integer, primary_key=True, index=True)
    nome = Column(String(150), nullable=False)
    marca = Column(String(100), nullable=True)
    preco = Column(Float, nullable=False)
    estoque = Column(Integer, nullable=False, default=0)
    ativo = Column(Boolean, default=True)

    # cada produto pertence a uma única categoria
    id_categoria = Column(Integer, ForeignKey("categorias.id_categoria"), nullable=False)
    categoria = relationship("Categoria", back_populates="produtos")
