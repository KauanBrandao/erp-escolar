from pydantic import BaseModel,EmailStr


class ModelUsuario(BaseModel):
    id:int
    nome:str
    email:EmailStr
    senhaHash:str
    ativo:bool
    criado_em:str
