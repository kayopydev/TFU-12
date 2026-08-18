# -*- coding: utf-8 -*-
"""
utils.py
--------
Funções auxiliares usadas pelas rotas da API.
"""

from fastapi import HTTPException, status


def obter_ou_404(db, modelo, id_valor, coluna_id, mensagem="Registro não encontrado."):
    """Busca um registro pelo id; se não existir, já lança o erro 404.

    Isso evita repetir o mesmo 'if not encontrado: raise HTTPException(...)'
    em cada rota de busca, atualização e remoção.
    """
    objeto = db.query(modelo).filter(coluna_id == id_valor).first()
    if not objeto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=mensagem)
    return objeto
