# -*- coding: utf-8 -*-
"""Rotas de autenticação: cadastro de usuário, login (JWT) e usuário logado."""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from database import SessionDep
from models.usuario import Usuario
from schemas.usuario import Token, UsuarioCreate, UsuarioResponse
from security import criar_token_acesso, gerar_hash_senha, obter_usuario_atual, verificar_senha

router = APIRouter(tags=["Autenticação"])


@router.post("/usuarios", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def registrar_usuario(usuario: UsuarioCreate, db: SessionDep):
    """Cadastra um novo usuário. A senha é salva apenas como hash."""
    existente = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Já existe um usuário cadastrado com esse e-mail.",
        )
    novo_usuario = Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha_hash=gerar_hash_senha(usuario.senha),
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario


@router.post("/token", response_model=Token)
def login(db: SessionDep, form_data: OAuth2PasswordRequestForm = Depends()):
    """Confere e-mail e senha e devolve um token JWT (login).

    O Swagger usa o campo 'username' do formulário para enviar o e-mail.
    """
    usuario = db.query(Usuario).filter(Usuario.email == form_data.username).first()
    if not usuario or not verificar_senha(form_data.password, usuario.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = criar_token_acesso({"sub": usuario.email})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/usuarios/me", response_model=UsuarioResponse)
def obter_meu_usuario(db: SessionDep, email_logado: str = Depends(obter_usuario_atual)):
    """Rota protegida: só responde se um token JWT válido for enviado."""
    usuario = db.query(Usuario).filter(Usuario.email == email_logado).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado."
        )
    return usuario
