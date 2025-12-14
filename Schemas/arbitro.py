from typing import Optional
from pydantic import BaseModel, Field

# --- Submodelo ---

class MongoID(BaseModel):
    """Modelo para el campo '_id' de MongoDB."""
    oid: str = Field(..., alias='$oid')

# --- Modelo Principal (Root) ---

class Arbitro(BaseModel):
    """Esquema para un oficial de partido (Árbitro, Árbitro de línea, etc.)."""
    id_mongo: MongoID = Field(..., alias='_id')
    nombre: str
    pais_id: int
    puesto: str
    pais: str

# Ejemplo de uso:
# from pydantic import parse_obj_as
# json_data = { ... } # Tu JSON de ejemplo
# arbitro = ArbitroSchema(**json_data)
# print(arbitro.nombre) # Deniz Aytekin