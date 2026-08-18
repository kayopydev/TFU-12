# -*- coding: utf-8 -*-
"""
security.py
------------
Funções de apoio à autenticação:
- hash e verificação de senha (nunca guardamos senha em texto puro);
- criação e leitura de token JWT;
- dependência para proteger rotas que exigem login.
"""

from datetime import datetime, timedelta

import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

# Em um projeto real, esta chave viria de uma variável de ambiente (.env),
# nunca ficaria escrita direto no código.
SECRET_KEY = "techbuy-chave-secreta-para-fins-didaticos-modulo5"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# aponta para a rota de login, usada pelo Swagger para pedir usuário/senha
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


def gerar_hash_senha(senha: str) -> str:
    """Transforma a senha em texto puro em um hash seguro (bcrypt)."""
    senha_bytes = senha.encode("utf-8")
    hash_bytes = bcrypt.hashpw(senha_bytes, bcrypt.gensalt())
    return hash_bytes.decode("utf-8")


def verificar_senha(senha: str, senha_hash: str) -> bool:
    """Confere se a senha informada no login bate com o hash salvo."""
    return bcrypt.checkpw(senha.encode("utf-8"), senha_hash.encode("utf-8"))


def criar_token_acesso(dados: dict) -> str:
    """Gera um token JWT com prazo de expiração."""
    dados_para_codificar = dados.copy()
    expira_em = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    dados_para_codificar.update({"exp": expira_em})
    return jwt.encode(dados_para_codificar, SECRET_KEY, algorithm=ALGORITHM)


def obter_usuario_atual(token: str = Depends(oauth2_scheme)) -> str:
    """Lê o token enviado na requisição e devolve o e-mail do usuário logado.

    Usada como dependência (Depends) em rotas que só podem ser acessadas
    por quem estiver autenticado.
    """
    erro_credenciais = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise erro_credenciais
    except JWTError:
        raise erro_credenciais
    return email
