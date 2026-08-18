# -*- coding: utf-8 -*-
"""Model da tabela usuarios, usada para cadastro e login (autenticação)."""

from sqlalchemy import Column, Integer, String

from database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False, unique=True, index=True)
    senha_hash = Column(String(255), nullable=False)  # a senha nunca é salva em texto puro
