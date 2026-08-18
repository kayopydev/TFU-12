# -*- coding: utf-8 -*-
"""
criar_tabelas.py
-----------------
Cria as tabelas do banco de dados a partir dos models do SQLAlchemy.
Rode este arquivo uma vez, antes de subir a API pela primeira vez:

    python criar_tabelas.py
"""

from database import Base, engine
from models.categoria import Categoria
from models.produto import Produto
from models.usuario import Usuario

Base.metadata.create_all(bind=engine)

print("Tabelas criadas com sucesso em techbuy.db!")
