from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    email: str
    senha: str = Field(min_length=8, max_length=100)


class SetupAdminRequest(BaseModel):
    nome: str = Field(min_length=3, max_length=100)
    email: str
    senha: str = Field(min_length=8, max_length=100)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class MeResponse(BaseModel):
    id: int
    nome: str
    email: str
    ativo: bool
    perfil_id: int
    perfil_nome: str
