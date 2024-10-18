from ninja import Schema
from pydantic import Field
from typing import Optional

class EventoSchema(Schema):
    id: str
    nome: str
    data_inicio: str
    data_fim: str
    valor: str
    local: str
    descricao: str
    link_validacao: str
    url_imagem: str
    
    class Config:
        from_attributes = True

class CreateEventoSchema(Schema):
    id: str= Field(..., alias="id")
    nome: str = Field(..., max_length=500)
    data_inicio: str = Field(..., alias="data_inicio")
    data_fim: str = Field(..., alias="data_fim")
    valor: str = Field(..., alias="valor")
    local: str = Field(..., max_length=500)
    descricao: str = Field(..., alias="descricao")
    link_validacao: str = Field(..., alias="link_validacao")
    url_imagem: str = Field(..., alias="url_imagem")
    
    class Config:
        from_attributes = True
        
class UpdateEventoSchema(Schema):
    nome: Optional[str] = Field(None, max_length=500)
    data_inicio: Optional[str]
    data_fim: Optional[str]
    valor: Optional[str]
    local: Optional[str] = Field(None, max_length=500)
    descricao: Optional[str]
    link_validacao: Optional[str]
    url_imagem: Optional[str]

    class Config:
        from_attributes = True
