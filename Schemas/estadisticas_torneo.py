from pydantic import BaseModel
from typing import List, Optional, Dict, Any

# ========== MODELOS DE REMONTADAS ==========

class PartidoRemontada(BaseModel):
    """Detalles de un partido con remontada."""
    partido_id: str
    equipo_local: str
    equipo_visitante: str
    goles_local: int
    goles_visitante: int
    ganador: str
    equipo_remonto: str
    diferencia_maxima: int
    marcador_inicial: str
    marcador_final: str
    fecha: Optional[str] = None
    estadio: Optional[str] = None
    ciudad: Optional[str] = None
    acciones_clave: Optional[List[Any]] = []

class EstadisticasRemontadas(BaseModel):
    """Estadísticas de remontadas en el torneo."""
    total_remontadas: int
    remontadas_2_goles: int
    remontadas_3_o_mas_goles: int
    equipos_con_mas_remontadas: List[Dict[str, Any]]
    partidos: List[PartidoRemontada]

# ========== MODELOS DE GOLEADORES ==========

class Goleador(BaseModel):
    """Información de un goleador."""
    jugador_id: Optional[str] = None
    nombre: str
    pais: str
    goles_totales: int
    goles_torneo: int
    partidos_jugados: int
    promedio_goles: float
    overall: Optional[int] = None

class EstadisticasGoleadores(BaseModel):
    """Top goleadores del torneo."""
    total_goles_torneo: int
    promedio_goles_partido: float
    top_goleadores: List[Goleador]
    goleador_maximo: Optional[Goleador] = None

# ========== MODELOS DE MEJOR JUGADOR ==========

class MejorJugador(BaseModel):
    """Información del mejor jugador."""
    jugador_id: Optional[str] = None
    nombre: str
    pais: str
    overall: int
    goles: int
    rendimiento_promedio: float
    partidos_jugados: int
    forma_actual: Optional[int] = None
    atributos_destacados: Dict[str, int]

class EstadisticasMejoresJugadores(BaseModel):
    """Top mejores jugadores del torneo."""
    criterio_evaluacion: str
    top_jugadores: List[MejorJugador]
    mejor_jugador_general: Optional[MejorJugador] = None

# ========== MODELOS DE EQUIPOS ==========

class EstadisticasEquipo(BaseModel):
    """Estadísticas de un equipo en el torneo."""
    equipo: str
    partidos_jugados: int
    victorias: int
    empates: int
    derrotas: int
    goles_favor: int
    goles_contra: int
    diferencia_goles: int
    porcentaje_victorias: float
    racha_actual: str

class EstadisticasEquipos(BaseModel):
    """Estadísticas de equipos."""
    total_equipos: int
    equipo_mas_goleador: Optional[EstadisticasEquipo] = None
    mejor_defensa: Optional[EstadisticasEquipo] = None
    equipo_mas_victorias: Optional[EstadisticasEquipo] = None
    equipos: List[EstadisticasEquipo]

# ========== MODELOS DE TARJETAS Y DISCIPLINA ==========

class EstadisticasDisciplina(BaseModel):
    """Estadísticas de tarjetas y disciplina."""
    total_tarjetas_amarillas: int
    total_tarjetas_rojas: int
    promedio_amarillas_partido: float
    promedio_rojas_partido: float
    equipo_mas_indisciplinado: Optional[Dict[str, Any]] = None
    jugador_mas_amonestado: Optional[Dict[str, Any]] = None

# ========== MODELOS DE PARTIDOS DESTACADOS ==========

class PartidoDestacado(BaseModel):
    """Partido destacado."""
    partido_id: str
    equipo_local: str
    equipo_visitante: str
    goles_local: int
    goles_visitante: int
    total_goles: int
    categoria: str  # "más goles", "más reñido", "más asistencia"
    descripcion: str
    fecha: Optional[str] = None
    estadio: Optional[str] = None

class EstadisticasPartidos(BaseModel):
    """Estadísticas de partidos."""
    total_partidos: int
    promedio_goles_partido: float
    partido_mas_goles: Optional[PartidoDestacado] = None
    partido_mas_asistencia: Optional[PartidoDestacado] = None
    partidos_destacados: List[PartidoDestacado]

# ========== MODELOS DE ESTADIOS ==========

class EstadisticasEstadio(BaseModel):
    """Estadísticas de un estadio."""
    estadio: str
    ciudad: str
    partidos_jugados: int
    total_goles: int
    promedio_goles: float
    asistencia_total: int
    asistencia_promedio: int

class EstadisticasEstadios(BaseModel):
    """Estadísticas de estadios."""
    total_estadios: int
    estadio_mas_partidos: Optional[EstadisticasEstadio] = None
    estadio_mas_goleador: Optional[EstadisticasEstadio] = None
    estadio_mayor_asistencia: Optional[EstadisticasEstadio] = None
    estadios: List[EstadisticasEstadio]

# ========== MODELOS DE LOCAL/VISITANTE/EMPATE ==========

class DetallesGolesPorTipo(BaseModel):
    """Detalles de goles clasificados por tipo de jugada."""
    goles_penal: int
    goles_corner: int
    goles_jugada_normal: int
    porcentaje_penal: float
    porcentaje_corner: float
    porcentaje_jugada_normal: float

class EstadisticasLocalVisitante(BaseModel):
    """Estadísticas de resultados local vs visitante."""
    total_partidos: int
    victorias_local: int
    victorias_visitante: int
    empates: int
    porcentaje_local: float
    porcentaje_visitante: float
    porcentaje_empate: float
    goles_local_total: int
    goles_visitante_total: int
    promedio_goles_local: float
    promedio_goles_visitante: float
    goles_local_detalle: DetallesGolesPorTipo
    goles_visitante_detalle: DetallesGolesPorTipo

# ========== MODELOS DE LESIONES ==========

class JugadorLesionado(BaseModel):
    """Información de un jugador lesionado."""
    jugador: str
    equipo: str
    partido_id: str
    minuto: Optional[int] = None
    rival: str

class EstadisticasLesiones(BaseModel):
    """Estadísticas de lesiones."""
    total_lesiones: int
    promedio_lesiones_partido: float
    equipo_mas_lesiones: Optional[Dict[str, Any]] = None
    jugadores_lesionados: List[JugadorLesionado]

# ========== MODELOS DE ÁRBITROS ==========

class ArbitroDetalle(BaseModel):
    """Información detallada de un árbitro."""
    id: str
    nombre: str
    pais: str
    puesto: str
    partidos_arbitrados: int
    amarillas_mostradas: int
    rojas_mostradas: int
    promedio_amarillas: float
    promedio_rojas: float

class EstadisticasArbitros(BaseModel):
    """Estadísticas de arbitraje."""
    total_arbitros_principal: int
    total_arbitros_linea: int
    arbitro_mas_partidos: Optional[ArbitroDetalle] = None
    arbitro_mas_amarillas: Optional[ArbitroDetalle] = None
    arbitro_mas_rojas: Optional[ArbitroDetalle] = None
    arbitros_principales: List[ArbitroDetalle]
    estadisticas_arbitros_linea: Optional[Dict[str, Any]] = None

# ========== MODELOS DE PARTIDOS ESPECIALES ==========

class PartidoEmocionante(BaseModel):
    """Partido emocionante por cantidad de acciones."""
    partido_id: str
    equipo_local: str
    equipo_visitante: str
    marcador: str
    acciones_criticas: int
    acciones_altas: int
    total_acciones: int
    indice_emocion: float
    estadio: Optional[str] = None

class PartidoAburrido(BaseModel):
    """Partido aburrido por pocas acciones."""
    partido_id: str
    equipo_local: str
    equipo_visitante: str
    marcador: str
    total_acciones: int
    total_goles: int
    indice_aburrimiento: float
    estadio: Optional[str] = None

class PartidoAgresivo(BaseModel):
    """Partido agresivo por faltas y tarjetas."""
    partido_id: str
    equipo_local: str
    equipo_visitante: str
    marcador: str
    total_faltas: int
    tarjetas_amarillas: int
    tarjetas_rojas: int
    indice_agresividad: float
    estadio: Optional[str] = None

class PartidoUltimoMinuto(BaseModel):
    """Partido decidido en el último minuto (cuando iba empatado)."""
    partido_id: str
    equipo_local: str
    equipo_visitante: str
    equipo_ganador: str
    marcador_final: str
    minuto_gol_decisivo: int
    jugador: str
    marcador_antes_gol: str
    descripcion: str

class PartidoGoleada(BaseModel):
    """Partido con goleada (humillación)."""
    partido_id: str
    equipo_ganador: str
    equipo_perdedor: str
    marcador: str
    diferencia_goles: int
    categoria_humillacion: str
    estadio: Optional[str] = None

class EstadisticasPartidosEspeciales(BaseModel):
    """Estadísticas de partidos con características especiales."""
    partidos_emocionantes: List[PartidoEmocionante]
    partidos_aburridos: List[PartidoAburrido]
    partidos_agresivos: List[PartidoAgresivo]
    goles_ultimo_minuto: List[PartidoUltimoMinuto]
    goleadas: List[PartidoGoleada]
    partido_menor_asistencia: Optional[Dict[str, Any]] = None
    partido_mayor_asistencia: Optional[Dict[str, Any]] = None

# ========== MODELOS DE GRÁFICAS ==========

class DatasetGrafica(BaseModel):
    """Dataset para una gráfica."""
    label: Optional[str] = None
    data: List[Any]
    backgroundColor: Optional[Any] = None  # Puede ser string o lista
    borderColor: Optional[str] = None
    pointBackgroundColor: Optional[str] = None
    fill: Optional[bool] = None

class Grafica(BaseModel):
    """Modelo genérico para una gráfica."""
    tipo: str  # bar, pie, line, doughnut, radar, horizontalBar
    titulo: str
    labels: List[str]
    datasets: List[DatasetGrafica]

class DatosGraficas(BaseModel):
    """Datos preparados para gráficas del frontend."""
    victorias_local_visitante: Grafica
    tipos_goles: Grafica
    top_goleadores: Grafica
    goles_local_vs_visitante: Grafica
    distribucion_tarjetas: Grafica
    equipos_goleadores: Grafica
    balance_goles_equipos: Grafica
    porcentajes_resultados: Grafica
    estadisticas_promedio: Grafica
    goles_por_jornada: Grafica
    disciplina_por_equipo: Grafica

# ========== MODELO PRINCIPAL ==========

class EstadisticasTorneoCompletas(BaseModel):
    """Respuesta completa con todas las estadísticas del torneo."""
    torneo: str
    total_partidos: int
    total_equipos: int
    total_goles: int
    
    # Estadísticas específicas
    remontadas: EstadisticasRemontadas
    goleadores: EstadisticasGoleadores
    mejores_jugadores: EstadisticasMejoresJugadores
    equipos: EstadisticasEquipos
    disciplina: EstadisticasDisciplina
    partidos_destacados: EstadisticasPartidos
    
    # Nuevas estadísticas
    estadios: EstadisticasEstadios
    local_visitante: EstadisticasLocalVisitante
    lesiones: EstadisticasLesiones
    arbitros: EstadisticasArbitros
    partidos_especiales: EstadisticasPartidosEspeciales
    
    # Datos para gráficas
    graficas: DatosGraficas
    
    # Metadata
    fecha_generacion: str
    mensaje: str
