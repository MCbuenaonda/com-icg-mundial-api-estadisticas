from pydantic import BaseModel, Field
from typing import Optional

class Jugador(BaseModel):
    id: Optional[int]
    nombre: Optional[str]
    posicion_id: Optional[int]
    pais_id: Optional[int]
    goles: Optional[int]
    goles_temp: Optional[int]
    botin: Optional[int]
    estrella: Optional[int]
    faltas: Optional[int]
    faltas_temp: Optional[int]
    amarilla: Optional[int]
    amarilla_temp: Optional[int]
    roja: Optional[int]
    roja_temp: Optional[int]
    lesiones: Optional[int]
    titular: Optional[int]
    numero: Optional[int]
    rendimiento: Optional[int]
    overall: Optional[int]
    
    # ========== ATRIBUTOS TÉCNICOS (0-100) ==========
    precision_tiro: Optional[int] = Field(default=70, ge=0, le=100)
    precision_pase: Optional[int] = Field(default=70, ge=0, le=100)
    regate: Optional[int] = Field(default=70, ge=0, le=100)
    fuerza_disparo: Optional[int] = Field(default=70, ge=0, le=100)
    vision_juego: Optional[int] = Field(default=70, ge=0, le=100)
    anticipacion: Optional[int] = Field(default=70, ge=0, le=100)
    control_balon: Optional[int] = Field(default=70, ge=0, le=100)
    juego_aereo: Optional[int] = Field(default=70, ge=0, le=100)
    
    # ========== ATRIBUTOS FÍSICOS (0-100) ==========
    velocidad: Optional[int] = Field(default=70, ge=0, le=100)
    resistencia: Optional[int] = Field(default=70, ge=0, le=100)
    fuerza_fisica: Optional[int] = Field(default=70, ge=0, le=100)
    agilidad: Optional[int] = Field(default=70, ge=0, le=100)
    
    # ========== ATRIBUTOS MENTALES (0-100) ==========
    compostura: Optional[int] = Field(default=70, ge=0, le=100)
    agresividad: Optional[int] = Field(default=50, ge=0, le=100)
    concentracion: Optional[int] = Field(default=70, ge=0, le=100)
    
    # ========== ESTADO Y FORMA (0-100) ==========
    forma_actual: Optional[int] = Field(default=70, ge=0, le=100)
    moral: Optional[int] = Field(default=70, ge=0, le=100)
    
    # ========== ESPECIALIDADES ==========
    especialista_tiros_libres: Optional[bool] = False
    especialista_penales: Optional[bool] = False
    pie_habil: Optional[str] = "derecho"  # "derecho", "izquierdo", "ambidiestro"
    
    # ========== HISTORIAL DE BONIFICACIONES ==========
    bonificaciones: Optional[list] = Field(default_factory=list)  # Lista de logros especiales
