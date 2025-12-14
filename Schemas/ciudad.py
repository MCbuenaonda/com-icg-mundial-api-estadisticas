from typing import Optional
from pydantic import BaseModel, Field

# --- Submodelos ---

class MongoID(BaseModel):
    """Modelo para el campo '_id' de MongoDB."""
    oid: str = Field(..., alias='$oid')

# --- Modelo Principal (Root) ---

class Ciudad(BaseModel):
    """Esquema para un objeto de Ubicación simple (Ciudad/Estadio)."""
    id_mongo: MongoID = Field(..., alias='_id')
    id: int
    nombre: str
    tipo: str
    estadio: str
    pais_id: int
    pais: str

# Ejemplo de uso:
# from pydantic import parse_obj_as
# json_data = { ... } # Tu JSON de ejemplo
# ubicacion = UbicacionMiniSchema(**json_data)
# print(ubicacion.nombre)