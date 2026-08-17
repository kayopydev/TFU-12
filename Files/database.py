# -*- coding: utf-8 -*-
"""
database.py
------------
Configuração da conexão com o banco de dados SQLite via SQLAlchemy.

Define também o SessionDep, usado como injeção de dependência nas rotas,
evitando repetir "with SessionLocal() as db" em cada endpoint.
"""

from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

# Banco de dados SQLite local (arquivo techbuy.db na raiz do projeto)
SQLALCHEMY_DATABASE_URL = "sqlite:///./techbuy.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Abre uma sessão do banco para a requisição e garante o fechamento no final."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Apelido usado nas rotas: def rota(db: SessionDep): ...
SessionDep = Annotated[Session, Depends(get_db)]
