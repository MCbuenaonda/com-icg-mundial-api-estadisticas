from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

# --- Submodelos ---

class MongoID(BaseModel):
    """Modelo para el campo '_id' de MongoDB."""
    oid: str = Field(..., alias='$oid')

class Tactica(BaseModel):
    """Detalles de la táctica del equipo."""
    formacion: str
    nombre: str
    descripcion: str
    estilo_posesion: str
    desgaste: str

class Ubicacion(BaseModel):
    """Detalles de la ubicación del partido."""
    ciudad: str
    pais: str
    estadio: str
    tipo_partido: str
    descripcion: str
    alineacion_local: str
    alineacion_visitante: str
    tactica_local: Tactica
    tactica_visitante: Tactica

class CambiosRealizados(BaseModel):
    """Conteo de cambios realizados."""
    local: int
    visitante: int
    total: int
    limite_por_equipo: int

class Expulsiones(BaseModel):
    """Detalles de las expulsiones (tarjetas rojas)."""
    local: List[Any]  # Asumo que es una lista vacía o de objetos que no se definieron
    visitante: List[Any]
    total_local: int
    total_visitante: int

class TarjetaAmarillaDetalle(BaseModel):
    """Detalles de una tarjeta amarilla individual."""
    jugador: str
    equipo: str
    minuto: int

class FactorEfecto(BaseModel):
    """Factores de efecto por expulsiones (factor_gol, factor_defensa)."""
    factor_gol: float
    factor_defensa: float
    descripcion: str

class EfectosExpulsiones(BaseModel):
    """Detalle de los efectos de las expulsiones."""
    factor_local: FactorEfecto
    factor_visitante: FactorEfecto
    goles_afectados: bool

class Lesiones(BaseModel):
    """Detalles de las lesiones."""
    local: List[Any]
    visitante: List[Any]
    total_local: int
    total_visitante: int
    detalles: List[Any]

class Accion(BaseModel):
    """Modelo para cada acción individual del partido."""
    clave: str
    minuto: int
    segundo: int
    tipo: str
    jugador: str
    equipo: str
    descripcion: str
    importancia: str
    sector: str
    direccion_balon: str
    exito: bool
    lado: str
    posicion: str
    stamina: float
    icono: str

class AccionesAgrupadas(BaseModel):
    """Acciones del partido agrupadas por importancia."""
    criticas: List[Accion]
    altas: List[Accion]
    medias: List[Accion]
    bajas: List[Accion]

class ConteoPorTipo(BaseModel):
    """Conteo de acciones por tipo."""
    Gol: int
    Falta: int
    Tiro: int
    Atajada: int
    Tarjeta_Amarilla: int = Field(..., alias='Tarjeta Amarilla')
    Centro: int
    Fuera_de_juego: int = Field(..., alias='Fuera de juego')
    Cambio: int
    Inicio: int
    Saque_de_Centro: int = Field(..., alias='Saque de Centro')
    Tiro_Libre: int = Field(..., alias='Tiro Libre')
    Bloqueado: int
    Intercepción: int
    Poste: int
    Despeje: int
    Señalización_árbitro: int = Field(..., alias='Señalización árbitro')
    Solicitud_VAR: int = Field(..., alias='Solicitud VAR')
    Revisión_VAR: int = Field(..., alias='Revisión VAR')
    Pase: int
    Regate: int
    Desviado: int
    Córner: int
    Entrada: int
    Descanso: int
    Final: int

class EstadisticasAcciones(BaseModel):
    """Estadísticas resumidas de las acciones."""
    total_acciones: int
    acciones_criticas: int
    acciones_altas: int
    acciones_medias: int
    acciones_bajas: int
    conteo_por_tipo: ConteoPorTipo

class Jugador(BaseModel):
    """Modelo para un jugador (titular o suplente)."""
    id_mongo: MongoID = Field(..., alias='_id')
    id: int
    nombre: str
    posicion_id: int
    pais_id: int
    goles: int
    goles_temp: int
    botin: int
    estrella: int
    faltas: int
    faltas_temp: int
    amarilla: int
    amarilla_temp: int
    roja: int
    roja_temp: int
    lesiones: int
    titular: int
    numero: int
    rendimiento: int
    agilidad: int
    agresividad: int
    anticipacion: int
    compostura: int
    concentracion: int
    control_balon: Optional[int] = Field(None, alias='control_balón') # Manejo el alias para la inconsistencia
    especialista_penales: bool
    especialista_tiros_libres: bool
    forma_actual: int
    fuerza_disparo: int
    fuerza_fisica: int
    juego_aereo: int
    moral: int
    overall: int
    pie_habil: str
    precision_pase: int
    precision_tiro: int
    regate: int
    resistencia: int
    velocidad: int
    vision_juego: int
    bonificaciones: Optional[Any] # Puede ser null o un objeto/dict más complejo
    pais: str

# --- Modelo Principal (Root) ---

class Historia(BaseModel):
    """Esquema principal para el objeto JSON del partido."""
    id_mongo: MongoID = Field(..., alias='_id')
    equipo_local: str
    equipo_visitante: str
    goles_local: int
    goles_visitante: int
    ganador: str
    clima: str
    asistencia: int
    nivel_asistencia: str
    porcentaje_asistencia: int
    descripcion_asistencia: str
    ubicacion: Ubicacion
    cambios_realizados: CambiosRealizados
    expulsiones: Expulsiones
    tarjetas_amarillas: Dict[str, int]
    tarjetas_amarillas_detalle: List[TarjetaAmarillaDetalle]
    tarjetas_rojas_detalle: List[Any]
    efectos_expulsiones: EfectosExpulsiones
    lesiones: Lesiones
    acciones: List[Accion]
    acciones_agrupadas: AccionesAgrupadas
    estadisticas_acciones: EstadisticasAcciones
    titulares_local: List[Jugador]
    titulares_visitante: List[Jugador]
    suplentes_local: List[Jugador]
    suplentes_visitante: List[Jugador]
    partido_original_id: str

# Ejemplo de cómo usarías el esquema (requiere Python y Pydantic instalados):
# import json
# json_data = YOUR_JSON_STRING
# parsed_data = json.loads(json_data)
# partido = PartidoSchema(**parsed_data)
# print(partido.equipo_local) # Acceso a datos validados