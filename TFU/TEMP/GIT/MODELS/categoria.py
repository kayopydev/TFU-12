# -*- coding: utf-8 -*-
"""Model da tabela categorias."""

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Categoria(Base):
    __tablename__ = "categorias"

    id_categoria = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False, unique=True)
    descricao = Column(String(255), nullable=True)

    # uma categoria tem vários produtos (relacionamento um-para-muitos)
    produtos = relationship("Produto", back_populates="categoria")
