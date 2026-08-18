# -*- coding: utf-8 -*-
"""Schemas (Pydantic) de entrada e saída para Usuario e para o Token de login."""

from pydantic import BaseModel, EmailStr, Field


class UsuarioCreate(BaseModel):
    """Dados recebidos no cadastro de um novo usuário."""
    nome: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    senha: str = Field(..., min_length=6, description="Mínimo de 6 caracteres")


class UsuarioResponse(BaseModel):
    """Dados devolvidos pela API. A senha (e o hash) nunca aparecem aqui."""
    id_usuario: int
    nome: str
    email: EmailStr

    class Config:
        from_attributes = True


class Token(BaseModel):
    """Resposta do endpoint de login."""
    access_token: str
    token_type: str
