# Arquivo de validação de dados de entrada/saída
from pydantic import BaseModel


class Message(BaseModel):
    message: str
