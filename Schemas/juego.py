from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

# --- Submodelos ---

class MongoID(BaseModel):
    """Modelo para el campo '_id' de MongoDB."""
    oid: str = Field(..., alias='$oid')

class EquipoDetalle(BaseModel):
    """Modelo para los detalles del equipo (local o visitante)."""
    id_mongo: MongoID = Field(..., alias='_id')
    id: int
    nombre: str
    siglas: str
    iso: str
    rankin: int
    puntos: int
    jj: int
    jg: int
    je: int
    jp: int
    gf: int
    gc: int
    lat: int
    lng: int
    federacion: str
    confederacion_id: int
    valor: int
    p_ofensiva: int
    p_defensiva: int
    p_posesion: int
    tactica_id: int
    poder: int
    efectividad_gol: float
    promedio_gol: float
    user_id: int
    estadisticas: Optional[Any]
    estado: str

class Resultado(BaseModel):
    """Detalles del resultado final del partido."""
    goles_local: int
    goles_visitante: int
    ganador: str

class UbicacionDetalle(BaseModel):
    """Detalles de la ubicación del partido (ciudad/estadio)."""
    id: int
    nombre: str
    tipo: str
    estadio: str
    pais_id: int
    pais: str

class Previa(BaseModel):
    """Modelo para el bloque de la previa del partido."""
    titulo: str
    cuerpo: str
    equipo_local: str
    equipo_visitante: str
    fecha: str
    estadio: str

class NoticiaEquipos(BaseModel):
    """Submodelo para los equipos dentro de la noticia."""
    local: str
    visitante: str

class Noticia(BaseModel):
    """Modelo para el bloque de la noticia/resumen post-partido."""
    partido_id: str
    titulo: str
    resumen: str
    cuerpo: str
    marcador: str
    equipos: NoticiaEquipos
    fecha: str
    estadio: str

# --- Modelo Principal (Root) ---

class Juego(BaseModel):
    """Esquema principal para el objeto JSON del partido."""
    id_mongo: MongoID = Field(..., alias='_id')
    mundial_id: int
    grupo: str
    confederacion_id: int
    
    equipo_local: EquipoDetalle
    equipo_visitante: EquipoDetalle
    
    tipo: str
    fecha: str
    resultado: Resultado
    estado: str
    tag: str
    jornada: str
    fase_id: int
    hora: str
    fecha_completa: str
    fecha_hora_str: str
    
    ubicacion: UbicacionDetalle
    previo: Previa
    noticia: Noticia