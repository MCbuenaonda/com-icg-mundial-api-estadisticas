from pydantic import BaseModel
from typing import Optional, List

# Sub Models
class Estadistica(BaseModel):
    puntos: Optional[int]
    juegos_jugados: Optional[int]
    juegos_ganados: Optional[int]
    juegos_empatados: Optional[int]
    juegos_perdidos: Optional[int]
    goles_favor: Optional[int]
    goles_contra: Optional[int]
    diferencia_goles: Optional[int]
    efectividad_gol: Optional[int]
    promedio_gol: Optional[int]
    rankin: Optional[int]
    poder: Optional[int]
    ultima_actualizacion: Optional[dict]

# Main Model
class Pais(BaseModel):
    _id: Optional[str]    
    id: Optional[int]
    nombre: Optional[str]
    siglas: Optional[str]
    iso: Optional[str]
    rankin: Optional[int]
    puntos: Optional[int]
    jj: Optional[int]
    jg: Optional[int]
    je: Optional[int]
    jp: Optional[int]
    gf: Optional[int]
    gc: Optional[int]
    lat: Optional[int]
    lng: Optional[int]
    federacion: Optional[str]
    confederacion_id: Optional[int]
    valor: Optional[int]
    p_ofensiva: Optional[int]
    p_defensiva: Optional[int]
    p_posesion: Optional[int]
    tactica_id: Optional[int]
    poder: Optional[int]
    efectividad_gol: Optional[int]
    promedio_gol: Optional[int]
    user_id: Optional[int]
    estado: Optional[str]
    estadisticas: Optional[List[Estadistica]] = []



