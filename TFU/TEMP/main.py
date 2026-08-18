# -*- coding: utf-8 -*-
"""
main.py
-------
Ponto de entrada da API TechBuy. Roda com: fastapi dev main.py
"""

from fastapi import FastAPI

from routers import auth, categorias, produtos

app = FastAPI(
    title="TechBuy API",
    description=(
        "API RESTful da loja virtual de eletrônicos TechBuy. "
        "TFU do Módulo 5, dando continuidade ao banco de dados (Módulo 2), "
        "à modelagem UML (Módulo 3) e às classes em Python (Módulo 4)."
    ),
    version="1.0.0",
)

app.include_router(categorias.router)
app.include_router(produtos.router)
app.include_router(auth.router)


@app.get("/", tags=["Status"])
def raiz():
    """Rota simples só para confirmar que a API está no ar."""
    return {"mensagem": "API TechBuy no ar. Acesse /docs para ver a documentação (Swagger)."}
