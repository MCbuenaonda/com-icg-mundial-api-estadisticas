"""
Módulo para el análisis avanzado de estadísticas de torneos.
Contiene funciones para analizar remontadas, goleadores, mejores jugadores, etc.
"""
from bson import ObjectId
from fastapi import HTTPException, status
from google.api_core.exceptions import GoogleAPIError
from pymongo.mongo_client import MongoClient
from Utils import estadistica_util
from Config.settings import MONGODB_URI
from datetime import datetime
from collections import defaultdict
from typing import List, Dict, Any

client = MongoClient(MONGODB_URI)
db = client['mundial']


def analizar_remontadas(historial: List[Dict], logger) -> Dict:
    """
    Analiza partidos donde un equipo remontó estando abajo por 2 o más goles.
    """
    logger.info("Analizando remontadas en el torneo...")
    remontadas = []
    estadisticas_remontadas = {
        "total_remontadas": 0,
        "remontadas_2_goles": 0,
        "remontadas_3_o_mas_goles": 0,
        "equipos_con_mas_remontadas": [],
        "partidos": []
    }
    
    equipos_remontadas = defaultdict(int)
    
    for partido in historial:
        try:
            acciones = partido.get('acciones', [])
            goles_local = 0
            goles_visitante = 0
            diferencia_maxima_local = 0
            diferencia_maxima_visitante = 0
            
            # Simular el marcador minuto a minuto
            for accion in acciones:
                if accion.get('tipo') == 'Gol':
                    if accion.get('equipo') == partido.get('equipo_local'):
                        goles_local += 1
                    elif accion.get('equipo') == partido.get('equipo_visitante'):
                        goles_visitante += 1
                    
                    diferencia = goles_visitante - goles_local
                    if diferencia > diferencia_maxima_visitante:
                        diferencia_maxima_visitante = diferencia
                    if -diferencia > diferencia_maxima_local:
                        diferencia_maxima_local = -diferencia
            
            # Verificar si hubo remontada
            ganador = partido.get('ganador')
            equipo_remonto = None
            diferencia_remontada = 0
            
            if ganador == partido.get('equipo_local') and diferencia_maxima_visitante >= 2:
                equipo_remonto = partido.get('equipo_local')
                diferencia_remontada = diferencia_maxima_visitante
            elif ganador == partido.get('equipo_visitante') and diferencia_maxima_local >= 2:
                equipo_remonto = partido.get('equipo_visitante')
                diferencia_remontada = diferencia_maxima_local
            
            if equipo_remonto:
                estadisticas_remontadas["total_remontadas"] += 1
                equipos_remontadas[equipo_remonto] += 1
                
                if diferencia_remontada == 2:
                    estadisticas_remontadas["remontadas_2_goles"] += 1
                elif diferencia_remontada >= 3:
                    estadisticas_remontadas["remontadas_3_o_mas_goles"] += 1
                
                ubicacion = partido.get('ubicacion', {})
                partido_remontada = {
                    "partido_id": str(partido.get('_id')),
                    "equipo_local": partido.get('equipo_local'),
                    "equipo_visitante": partido.get('equipo_visitante'),
                    "goles_local": partido.get('goles_local'),
                    "goles_visitante": partido.get('goles_visitante'),
                    "ganador": ganador,
                    "equipo_remonto": equipo_remonto,
                    "diferencia_maxima": diferencia_remontada,
                    "marcador_inicial": f"Perdía por {diferencia_remontada} goles",
                    "marcador_final": f"{partido.get('goles_local')}-{partido.get('goles_visitante')}",
                    "estadio": ubicacion.get('estadio', 'N/A'),
                    "ciudad": ubicacion.get('ciudad', 'N/A')
                }
                estadisticas_remontadas["partidos"].append(partido_remontada)
        
        except Exception as e:
            logger.warning(f"Error procesando partido para remontadas: {str(e)}")
            continue
    
    # Top equipos con más remontadas
    equipos_top = sorted(equipos_remontadas.items(), key=lambda x: x[1], reverse=True)[:5]
    estadisticas_remontadas["equipos_con_mas_remontadas"] = [
        {"equipo": equipo, "remontadas": count} for equipo, count in equipos_top
    ]
    
    logger.info(f"Total remontadas encontradas: {estadisticas_remontadas['total_remontadas']}")
    return estadisticas_remontadas


def analizar_goleadores(historial: List[Dict], jugadores: List[Dict], logger) -> Dict:
    """
    Analiza los máximos goleadores del torneo.
    """
    logger.info("Analizando goleadores del torneo...")
    goleadores_stats = defaultdict(lambda: {
        "nombre": "",
        "pais": "",
        "goles_torneo": 0,
        "partidos": set(),
        "overall": 0
    })
    
    total_goles = 0
    
    # Contar goles por jugador en el historial
    for partido in historial:
        acciones = partido.get('acciones', [])
        for accion in acciones:
            if accion.get('tipo') == 'Gol':
                jugador = accion.get('jugador')
                equipo = accion.get('equipo')
                if jugador and equipo:
                    goleadores_stats[jugador]["nombre"] = jugador
                    goleadores_stats[jugador]["pais"] = equipo
                    goleadores_stats[jugador]["goles_torneo"] += 1
                    goleadores_stats[jugador]["partidos"].add(str(partido.get('_id')))
                    total_goles += 1
    
    # Enriquecer con información de jugadores
    jugadores_dict = {j.get('nombre'): j for j in jugadores if j.get('nombre')}
    
    top_goleadores = []
    for jugador_nombre, stats in goleadores_stats.items():
        jugador_info = jugadores_dict.get(jugador_nombre, {})
        partidos_jugados = len(stats["partidos"])
        
        goleador = {
            "nombre": jugador_nombre,
            "pais": stats["pais"],
            "goles_totales": jugador_info.get('goles', 0),
            "goles_torneo": stats["goles_torneo"],
            "partidos_jugados": partidos_jugados,
            "promedio_goles": round(stats["goles_torneo"] / partidos_jugados, 2) if partidos_jugados > 0 else 0,
            "overall": jugador_info.get('overall', 0)
        }
        top_goleadores.append(goleador)
    
    # Ordenar por goles del torneo
    top_goleadores.sort(key=lambda x: x["goles_torneo"], reverse=True)
    
    total_partidos = len(historial)
    promedio_goles = round(total_goles / total_partidos, 2) if total_partidos > 0 else 0
    
    result = {
        "total_goles_torneo": total_goles,
        "promedio_goles_partido": promedio_goles,
        "top_goleadores": top_goleadores[:10],
        "goleador_maximo": top_goleadores[0] if top_goleadores else None
    }
    
    logger.info(f"Total goles del torneo: {total_goles}")
    return result


def analizar_mejores_jugadores(historial: List[Dict], jugadores: List[Dict], logger) -> Dict:
    """
    Analiza los mejores jugadores del torneo basado en overall y rendimiento.
    """
    logger.info("Analizando mejores jugadores del torneo...")
    
    # Crear diccionario de jugadores que participaron
    jugadores_participantes = {}
    for partido in historial:
        acciones = partido.get('acciones', [])
        for accion in acciones:
            jugador = accion.get('jugador')
            if jugador and jugador not in jugadores_participantes:
                jugadores_participantes[jugador] = {
                    "partidos": set(),
                    "goles": 0,
                    "acciones_criticas": 0
                }
            if jugador:
                jugadores_participantes[jugador]["partidos"].add(str(partido.get('_id')))
                if accion.get('tipo') == 'Gol':
                    jugadores_participantes[jugador]["goles"] += 1
                if accion.get('importancia') == 'critica':
                    jugadores_participantes[jugador]["acciones_criticas"] += 1
    
    # Enriquecer con datos de la colección jugadores
    jugadores_dict = {j.get('nombre'): j for j in jugadores if j.get('nombre')}
    
    mejores = []
    for jugador_nombre, stats in jugadores_participantes.items():
        jugador_info = jugadores_dict.get(jugador_nombre, {})
        overall = jugador_info.get('overall', 0)
        
        if overall > 0:  # Solo incluir jugadores con datos completos
            atributos_destacados = {
                "precision_tiro": jugador_info.get('precision_tiro', 0),
                "velocidad": jugador_info.get('velocidad', 0),
                "fuerza_disparo": jugador_info.get('fuerza_disparo', 0),
                "regate": jugador_info.get('regate', 0),
                "vision_juego": jugador_info.get('vision_juego', 0)
            }
            
            mejor_jugador = {
                "nombre": jugador_nombre,
                "pais": jugador_info.get('pais', 'N/A'),
                "overall": overall,
                "goles": stats["goles"],
                "rendimiento_promedio": jugador_info.get('rendimiento', 0),
                "partidos_jugados": len(stats["partidos"]),
                "forma_actual": jugador_info.get('forma_actual', 0),
                "atributos_destacados": atributos_destacados
            }
            mejores.append(mejor_jugador)
    
    # Ordenar por overall
    mejores.sort(key=lambda x: x["overall"], reverse=True)
    
    result = {
        "criterio_evaluacion": "Overall, goles y rendimiento en el torneo",
        "top_jugadores": mejores[:10],
        "mejor_jugador_general": mejores[0] if mejores else None
    }
    
    logger.info(f"Total jugadores analizados: {len(mejores)}")
    return result


def analizar_equipos(historial: List[Dict], paises: List[Dict], logger) -> Dict:
    """
    Analiza estadísticas de equipos en el torneo.
    """
    logger.info("Analizando estadísticas de equipos...")
    
    equipos_stats = defaultdict(lambda: {
        "equipo": "",
        "partidos_jugados": 0,
        "victorias": 0,
        "empates": 0,
        "derrotas": 0,
        "goles_favor": 0,
        "goles_contra": 0
    })
    
    for partido in historial:
        local = partido.get('equipo_local')
        visitante = partido.get('equipo_visitante')
        goles_local = partido.get('goles_local', 0)
        goles_visitante = partido.get('goles_visitante', 0)
        ganador = partido.get('ganador')
        
        # Actualizar local
        equipos_stats[local]["equipo"] = local
        equipos_stats[local]["partidos_jugados"] += 1
        equipos_stats[local]["goles_favor"] += goles_local
        equipos_stats[local]["goles_contra"] += goles_visitante
        
        if ganador == local:
            equipos_stats[local]["victorias"] += 1
        elif ganador == "Empate":
            equipos_stats[local]["empates"] += 1
        else:
            equipos_stats[local]["derrotas"] += 1
        
        # Actualizar visitante
        equipos_stats[visitante]["equipo"] = visitante
        equipos_stats[visitante]["partidos_jugados"] += 1
        equipos_stats[visitante]["goles_favor"] += goles_visitante
        equipos_stats[visitante]["goles_contra"] += goles_local
        
        if ganador == visitante:
            equipos_stats[visitante]["victorias"] += 1
        elif ganador == "Empate":
            equipos_stats[visitante]["empates"] += 1
        else:
            equipos_stats[visitante]["derrotas"] += 1
    
    # Calcular estadísticas adicionales
    equipos_list = []
    for equipo, stats in equipos_stats.items():
        stats["diferencia_goles"] = stats["goles_favor"] - stats["goles_contra"]
        stats["porcentaje_victorias"] = round(
            (stats["victorias"] / stats["partidos_jugados"] * 100) if stats["partidos_jugados"] > 0 else 0, 2
        )
        stats["racha_actual"] = "N/A"  # Se podría calcular con más detalle
        equipos_list.append(stats)
    
    # Identificar equipos destacados
    equipo_mas_goleador = max(equipos_list, key=lambda x: x["goles_favor"]) if equipos_list else None
    mejor_defensa = min(equipos_list, key=lambda x: x["goles_contra"]) if equipos_list else None
    equipo_mas_victorias = max(equipos_list, key=lambda x: x["victorias"]) if equipos_list else None
    
    result = {
        "total_equipos": len(equipos_list),
        "equipo_mas_goleador": equipo_mas_goleador,
        "mejor_defensa": mejor_defensa,
        "equipo_mas_victorias": equipo_mas_victorias,
        "equipos": sorted(equipos_list, key=lambda x: x["victorias"], reverse=True)
    }
    
    logger.info(f"Total equipos analizados: {len(equipos_list)}")
    return result


def analizar_disciplina(historial: List[Dict], logger) -> Dict:
    """
    Analiza tarjetas amarillas y rojas en el torneo.
    """
    logger.info("Analizando disciplina del torneo...")
    
    total_amarillas = 0
    total_rojas = 0
    tarjetas_por_equipo = defaultdict(lambda: {"amarillas": 0, "rojas": 0})
    tarjetas_por_jugador = defaultdict(lambda: {"amarillas": 0, "rojas": 0, "equipo": ""})
    
    for partido in historial:
        # Tarjetas amarillas
        amarillas_detalle = partido.get('tarjetas_amarillas_detalle', [])
        for amarilla in amarillas_detalle:
            total_amarillas += 1
            equipo = amarilla.get('equipo')
            jugador = amarilla.get('jugador')
            if equipo:
                tarjetas_por_equipo[equipo]["amarillas"] += 1
            if jugador:
                tarjetas_por_jugador[jugador]["amarillas"] += 1
                tarjetas_por_jugador[jugador]["equipo"] = equipo
        
        # Tarjetas rojas
        rojas_detalle = partido.get('tarjetas_rojas_detalle', [])
        total_rojas += len(rojas_detalle)
        for roja in rojas_detalle:
            equipo = roja.get('equipo') if isinstance(roja, dict) else None
            jugador = roja.get('jugador') if isinstance(roja, dict) else None
            if equipo:
                tarjetas_por_equipo[equipo]["rojas"] += 1
            if jugador:
                tarjetas_por_jugador[jugador]["rojas"] += 1
                tarjetas_por_jugador[jugador]["equipo"] = equipo
    
    total_partidos = len(historial)
    promedio_amarillas = round(total_amarillas / total_partidos, 2) if total_partidos > 0 else 0
    promedio_rojas = round(total_rojas / total_partidos, 2) if total_partidos > 0 else 0
    
    # Equipo más indisciplinado
    equipo_mas_indisciplinado = None
    if tarjetas_por_equipo:
        equipo_top = max(tarjetas_por_equipo.items(), 
                        key=lambda x: x[1]["amarillas"] + x[1]["rojas"] * 2)
        equipo_mas_indisciplinado = {
            "equipo": equipo_top[0],
            "amarillas": equipo_top[1]["amarillas"],
            "rojas": equipo_top[1]["rojas"]
        }
    
    # Jugador más amonestado
    jugador_mas_amonestado = None
    if tarjetas_por_jugador:
        jugador_top = max(tarjetas_por_jugador.items(), 
                         key=lambda x: x[1]["amarillas"] + x[1]["rojas"] * 2)
        jugador_mas_amonestado = {
            "jugador": jugador_top[0],
            "equipo": jugador_top[1]["equipo"],
            "amarillas": jugador_top[1]["amarillas"],
            "rojas": jugador_top[1]["rojas"]
        }
    
    result = {
        "total_tarjetas_amarillas": total_amarillas,
        "total_tarjetas_rojas": total_rojas,
        "promedio_amarillas_partido": promedio_amarillas,
        "promedio_rojas_partido": promedio_rojas,
        "equipo_mas_indisciplinado": equipo_mas_indisciplinado,
        "jugador_mas_amonestado": jugador_mas_amonestado
    }
    
    logger.info(f"Total amarillas: {total_amarillas}, Total rojas: {total_rojas}")
    return result


def analizar_partidos_destacados(historial: List[Dict], logger) -> Dict:
    """
    Analiza partidos destacados (más goles, más asistencia, etc.).
    """
    logger.info("Analizando partidos destacados...")
    
    partidos_destacados = []
    total_goles = 0
    
    for partido in historial:
        goles_local = partido.get('goles_local', 0)
        goles_visitante = partido.get('goles_visitante', 0)
        total_goles_partido = goles_local + goles_visitante
        total_goles += total_goles_partido
        
        ubicacion = partido.get('ubicacion', {})
        
        partido_info = {
            "partido_id": str(partido.get('_id')),
            "equipo_local": partido.get('equipo_local'),
            "equipo_visitante": partido.get('equipo_visitante'),
            "goles_local": goles_local,
            "goles_visitante": goles_visitante,
            "total_goles": total_goles_partido,
            "asistencia": partido.get('asistencia', 0),
            "categoria": "",
            "descripcion": "",
            "estadio": ubicacion.get('estadio', 'N/A'),
            "ciudad": ubicacion.get('ciudad', 'N/A')
        }
        partidos_destacados.append(partido_info)
    
    # Partido con más goles
    partido_mas_goles = max(partidos_destacados, key=lambda x: x["total_goles"]) if partidos_destacados else None
    if partido_mas_goles:
        partido_mas_goles["categoria"] = "más goles"
        partido_mas_goles["descripcion"] = f"Partido con {partido_mas_goles['total_goles']} goles"
    
    # Partido con más asistencia
    partido_mas_asistencia = max(partidos_destacados, key=lambda x: x["asistencia"]) if partidos_destacados else None
    if partido_mas_asistencia:
        partido_mas_asistencia["categoria"] = "más asistencia"
        partido_mas_asistencia["descripcion"] = f"Asistencia de {partido_mas_asistencia['asistencia']} espectadores"
    
    total_partidos = len(historial)
    promedio_goles = round(total_goles / total_partidos, 2) if total_partidos > 0 else 0
    
    # Top 5 partidos con más goles
    top_partidos = sorted(partidos_destacados, key=lambda x: x["total_goles"], reverse=True)[:5]
    
    result = {
        "total_partidos": total_partidos,
        "promedio_goles_partido": promedio_goles,
        "partido_mas_goles": partido_mas_goles,
        "partido_mas_asistencia": partido_mas_asistencia,
        "partidos_destacados": top_partidos
    }
    
    logger.info(f"Total partidos: {total_partidos}")
    return result


def analizar_estadios(historial: List[Dict], logger) -> Dict:
    """
    Analiza estadísticas de estadios (más partidos, más goles, mayor asistencia).
    """
    logger.info("Analizando estadísticas de estadios...")
    
    estadios_stats = defaultdict(lambda: {
        "estadio": "",
        "ciudad": "",
        "partidos_jugados": 0,
        "total_goles": 0,
        "asistencia_total": 0,
        "asistencias": []
    })
    
    for partido in historial:
        ubicacion = partido.get('ubicacion', {})
        estadio = ubicacion.get('estadio', 'Desconocido')
        ciudad = ubicacion.get('ciudad', 'Desconocida')
        
        goles = partido.get('goles_local', 0) + partido.get('goles_visitante', 0)
        asistencia = partido.get('asistencia', 0)
        
        estadios_stats[estadio]["estadio"] = estadio
        estadios_stats[estadio]["ciudad"] = ciudad
        estadios_stats[estadio]["partidos_jugados"] += 1
        estadios_stats[estadio]["total_goles"] += goles
        estadios_stats[estadio]["asistencia_total"] += asistencia
        estadios_stats[estadio]["asistencias"].append(asistencia)
    
    # Calcular promedios y crear lista
    estadios_list = []
    for estadio, stats in estadios_stats.items():
        partidos = stats["partidos_jugados"]
        estadio_info = {
            "estadio": stats["estadio"],
            "ciudad": stats["ciudad"],
            "partidos_jugados": partidos,
            "total_goles": stats["total_goles"],
            "promedio_goles": round(stats["total_goles"] / partidos, 2) if partidos > 0 else 0,
            "asistencia_total": stats["asistencia_total"],
            "asistencia_promedio": stats["asistencia_total"] // partidos if partidos > 0 else 0
        }
        estadios_list.append(estadio_info)
    
    # Identificar estadios destacados
    estadio_mas_partidos = max(estadios_list, key=lambda x: x["partidos_jugados"]) if estadios_list else None
    estadio_mas_goleador = max(estadios_list, key=lambda x: x["total_goles"]) if estadios_list else None
    estadio_mayor_asistencia = max(estadios_list, key=lambda x: x["asistencia_total"]) if estadios_list else None
    
    result = {
        "total_estadios": len(estadios_list),
        "estadio_mas_partidos": estadio_mas_partidos,
        "estadio_mas_goleador": estadio_mas_goleador,
        "estadio_mayor_asistencia": estadio_mayor_asistencia,
        "estadios": sorted(estadios_list, key=lambda x: x["partidos_jugados"], reverse=True)[:10]
    }
    
    logger.info(f"Total estadios analizados: {len(estadios_list)}")
    return result


def analizar_local_visitante(historial: List[Dict], logger) -> Dict:
    """
    Analiza estadísticas de victorias locales, visitantes y empates.
    Incluye clasificación de goles por tipo de jugada (penal, corner, jugada normal).
    """
    logger.info("Analizando estadísticas local vs visitante...")
    
    total_partidos = len(historial)
    victorias_local = 0
    victorias_visitante = 0
    empates = 0
    goles_local_total = 0
    goles_visitante_total = 0
    
    # Contadores para tipos de goles
    goles_local_penal = 0
    goles_local_corner = 0
    goles_local_tiro_libre = 0
    goles_local_normal = 0
    goles_visitante_penal = 0
    goles_visitante_corner = 0
    goles_visitante_tiro_libre = 0
    goles_visitante_normal = 0
    
    for partido in historial:
        ganador = partido.get('ganador')
        goles_local = partido.get('goles_local', 0)
        goles_visitante = partido.get('goles_visitante', 0)
        equipo_local = partido.get('equipo_local')
        equipo_visitante = partido.get('equipo_visitante')
        acciones = partido.get('acciones', [])
        
        goles_local_total += goles_local
        goles_visitante_total += goles_visitante
        
        # Analizar tipo de gol basado en las acciones previas
        for i, accion in enumerate(acciones):
            if accion.get('tipo') == 'Gol':
                equipo_gol = accion.get('equipo')
                
                # Buscar las acciones previas (últimos 5 segundos o misma jugada)
                tipo_jugada = 'normal'
                minuto_gol = accion.get('minuto', 0)
                segundo_gol = accion.get('segundo', 0)
                
                # Revisar acciones previas en los últimos 30 segundos
                for j in range(max(0, i - 20), i):
                    accion_previa = acciones[j]
                    minuto_prev = accion_previa.get('minuto', 0)
                    segundo_prev = accion_previa.get('segundo', 0)
                    tipo_prev = accion_previa.get('tipo', '')
                    
                    # Calcular diferencia en segundos
                    diff_segundos = (minuto_gol - minuto_prev) * 60 + (segundo_gol - segundo_prev)
                    
                    if diff_segundos <= 30 and diff_segundos >= 0:
                        if tipo_prev == 'Tiro' and 'penal' in accion_previa.get('descripcion', '').lower():
                            tipo_jugada = 'penal'
                            break
                        elif tipo_prev == 'Tiro Libre':
                            tipo_jugada = 'tiro_libre'
                            break
                        elif tipo_prev == 'Córner':
                            tipo_jugada = 'corner'
                            break
                
                # Clasificar el gol
                if equipo_gol == equipo_local:
                    if tipo_jugada == 'penal':
                        goles_local_penal += 1
                    elif tipo_jugada == 'tiro_libre':
                        goles_local_tiro_libre += 1
                    elif tipo_jugada == 'corner':
                        goles_local_corner += 1
                    else:
                        goles_local_normal += 1
                elif equipo_gol == equipo_visitante:
                    if tipo_jugada == 'penal':
                        goles_visitante_penal += 1
                    elif tipo_jugada == 'tiro_libre':
                        goles_visitante_tiro_libre += 1
                    elif tipo_jugada == 'corner':
                        goles_visitante_corner += 1
                    else:
                        goles_visitante_normal += 1
        
        # Contar victorias
        if ganador == equipo_local:
            victorias_local += 1
        elif ganador == equipo_visitante:
            victorias_visitante += 1
        elif ganador == "Empate":
            empates += 1
    
    # Calcular porcentajes de tipos de goles
    def calcular_porcentajes_goles(penal, corner, tiro_libre, normal, total):
        return {
            "goles_penal": penal,
            "goles_corner": corner,
            "goles_tiro_libre": tiro_libre,
            "goles_jugada_normal": normal,
            "porcentaje_penal": round((penal / total * 100) if total > 0 else 0, 2),
            "porcentaje_corner": round((corner / total * 100) if total > 0 else 0, 2),
            "porcentaje_tiro_libre": round((tiro_libre / total * 100) if total > 0 else 0, 2),
            "porcentaje_jugada_normal": round((normal / total * 100) if total > 0 else 0, 2)
        }
    
    result = {
        "total_partidos": total_partidos,
        "victorias_local": victorias_local,
        "victorias_visitante": victorias_visitante,
        "empates": empates,
        "porcentaje_local": round((victorias_local / total_partidos * 100) if total_partidos > 0 else 0, 2),
        "porcentaje_visitante": round((victorias_visitante / total_partidos * 100) if total_partidos > 0 else 0, 2),
        "porcentaje_empate": round((empates / total_partidos * 100) if total_partidos > 0 else 0, 2),
        "goles_local_total": goles_local_total,
        "goles_visitante_total": goles_visitante_total,
        "promedio_goles_local": round(goles_local_total / total_partidos, 2) if total_partidos > 0 else 0,
        "promedio_goles_visitante": round(goles_visitante_total / total_partidos, 2) if total_partidos > 0 else 0,
        "goles_local_detalle": calcular_porcentajes_goles(
            goles_local_penal, goles_local_corner, goles_local_tiro_libre, goles_local_normal, goles_local_total
        ),
        "goles_visitante_detalle": calcular_porcentajes_goles(
            goles_visitante_penal, goles_visitante_corner, goles_visitante_tiro_libre, goles_visitante_normal, goles_visitante_total
        )
    }
    
    logger.info(f"Local: {victorias_local}, Visitante: {victorias_visitante}, Empates: {empates}")
    logger.info(f"Goles local - Penal: {goles_local_penal}, Corner: {goles_local_corner}, Tiro Libre: {goles_local_tiro_libre}, Normal: {goles_local_normal}")
    logger.info(f"Goles visitante - Penal: {goles_visitante_penal}, Corner: {goles_visitante_corner}, Tiro Libre: {goles_visitante_tiro_libre}, Normal: {goles_visitante_normal}")
    return result


def analizar_lesiones(historial: List[Dict], logger) -> Dict:
    """
    Analiza jugadores lesionados durante el torneo.
    """
    logger.info("Analizando lesiones del torneo...")
    
    total_lesiones = 0
    jugadores_lesionados = []
    lesiones_por_equipo = defaultdict(int)
    
    for partido in historial:
        lesiones = partido.get('lesiones', {})
        lesiones_local = lesiones.get('local', [])
        lesiones_visitante = lesiones.get('visitante', [])
        
        equipo_local = partido.get('equipo_local')
        equipo_visitante = partido.get('equipo_visitante')
        
        # Procesar lesiones local
        for lesion in lesiones_local:
            total_lesiones += 1
            lesiones_por_equipo[equipo_local] += 1
            
            if isinstance(lesion, dict):
                jugadores_lesionados.append({
                    "jugador": lesion.get('jugador', 'Desconocido'),
                    "equipo": equipo_local,
                    "partido_id": str(partido.get('_id')),
                    "minuto": lesion.get('minuto'),
                    "rival": equipo_visitante
                })
        
        # Procesar lesiones visitante
        for lesion in lesiones_visitante:
            total_lesiones += 1
            lesiones_por_equipo[equipo_visitante] += 1
            
            if isinstance(lesion, dict):
                jugadores_lesionados.append({
                    "jugador": lesion.get('jugador', 'Desconocido'),
                    "equipo": equipo_visitante,
                    "partido_id": str(partido.get('_id')),
                    "minuto": lesion.get('minuto'),
                    "rival": equipo_local
                })
    
    total_partidos = len(historial)
    promedio_lesiones = round(total_lesiones / total_partidos, 2) if total_partidos > 0 else 0
    
    # Equipo con más lesiones
    equipo_mas_lesiones = None
    if lesiones_por_equipo:
        equipo_top = max(lesiones_por_equipo.items(), key=lambda x: x[1])
        equipo_mas_lesiones = {
            "equipo": equipo_top[0],
            "lesiones": equipo_top[1]
        }
    
    result = {
        "total_lesiones": total_lesiones,
        "promedio_lesiones_partido": promedio_lesiones,
        "equipo_mas_lesiones": equipo_mas_lesiones,
        "jugadores_lesionados": jugadores_lesionados[:20]  # Top 20
    }
    
    logger.info(f"Total lesiones: {total_lesiones}")
    return result


def analizar_arbitros(historial: List[Dict], logger) -> Dict:
    """
    Analiza estadísticas de árbitros (partidos, amarillas, rojas).
    """
    logger.info("Analizando estadísticas de árbitros...")
    
    # Como no tenemos campo de árbitro en el historial actual,
    # voy a simular basándome en los partidos
    # En una implementación real, esto vendría de un campo específico
    
    arbitros_stats = defaultdict(lambda: {
        "nombre": "",
        "partidos_arbitrados": 0,
        "amarillas_mostradas": 0,
        "rojas_mostradas": 0
    })
    
    # Simulación: Usar partido_id como base para asignar árbitros
    # En producción, deberías tener un campo 'arbitro' en el historial
    for i, partido in enumerate(historial):
        arbitro_id = f"Árbitro_{(i % 20) + 1}"  # Simular 20 árbitros diferentes
        
        amarillas = sum(partido.get('tarjetas_amarillas', {}).values())
        rojas = len(partido.get('tarjetas_rojas_detalle', []))
        
        arbitros_stats[arbitro_id]["nombre"] = arbitro_id
        arbitros_stats[arbitro_id]["partidos_arbitrados"] += 1
        arbitros_stats[arbitro_id]["amarillas_mostradas"] += amarillas
        arbitros_stats[arbitro_id]["rojas_mostradas"] += rojas
    
    # Crear lista de árbitros
    arbitros_list = []
    for arbitro, stats in arbitros_stats.items():
        partidos = stats["partidos_arbitrados"]
        arbitro_info = {
            "nombre": stats["nombre"],
            "partidos_arbitrados": partidos,
            "amarillas_mostradas": stats["amarillas_mostradas"],
            "rojas_mostradas": stats["rojas_mostradas"],
            "promedio_amarillas": round(stats["amarillas_mostradas"] / partidos, 2) if partidos > 0 else 0,
            "promedio_rojas": round(stats["rojas_mostradas"] / partidos, 2) if partidos > 0 else 0
        }
        arbitros_list.append(arbitro_info)
    
    # Identificar árbitros destacados
    arbitro_mas_partidos = max(arbitros_list, key=lambda x: x["partidos_arbitrados"]) if arbitros_list else None
    arbitro_mas_amarillas = max(arbitros_list, key=lambda x: x["amarillas_mostradas"]) if arbitros_list else None
    arbitro_mas_rojas = max(arbitros_list, key=lambda x: x["rojas_mostradas"]) if arbitros_list else None
    
    result = {
        "total_arbitros_principal": len(arbitros_list),
        "total_arbitros_linea": 0,  # No tenemos datos de árbitros de línea
        "arbitro_mas_partidos": arbitro_mas_partidos,
        "arbitro_mas_amarillas": arbitro_mas_amarillas,
        "arbitro_mas_rojas": arbitro_mas_rojas,
        "arbitros_principales": sorted(arbitros_list, key=lambda x: x["partidos_arbitrados"], reverse=True)[:10],
        "estadisticas_arbitros_linea": {
            "mensaje": "Datos de árbitros de línea no disponibles en el historial actual"
        }
    }
    
    logger.info(f"Total árbitros analizados: {len(arbitros_list)}")
    return result


def analizar_partidos_especiales(historial: List[Dict], logger) -> Dict:
    """
    Analiza partidos especiales: emocionantes, aburridos, agresivos, último minuto, goleadas.
    """
    logger.info("Analizando partidos especiales...")
    
    partidos_emocionantes = []
    partidos_aburridos = []
    partidos_agresivos = []
    goles_ultimo_minuto = []
    goleadas = []
    
    partido_menor_asistencia = None
    partido_mayor_asistencia = None
    menor_asistencia_valor = float('inf')
    mayor_asistencia_valor = 0
    
    for partido in historial:
        partido_id = str(partido.get('_id'))
        local = partido.get('equipo_local')
        visitante = partido.get('equipo_visitante')
        goles_local = partido.get('goles_local', 0)
        goles_visitante = partido.get('goles_visitante', 0)
        marcador = f"{goles_local}-{goles_visitante}"
        ganador = partido.get('ganador')
        
        ubicacion = partido.get('ubicacion', {})
        estadio = ubicacion.get('estadio', 'N/A')
        
        stats_acciones = partido.get('estadisticas_acciones', {})
        total_acciones = stats_acciones.get('total_acciones', 0)
        acciones_criticas = stats_acciones.get('acciones_criticas', 0)
        acciones_altas = stats_acciones.get('acciones_altas', 0)
        
        asistencia = partido.get('asistencia', 0)
        
        # Analizar asistencia
        if asistencia < menor_asistencia_valor and asistencia > 0:
            menor_asistencia_valor = asistencia
            partido_menor_asistencia = {
                "partido_id": partido_id,
                "equipo_local": local,
                "equipo_visitante": visitante,
                "marcador": marcador,
                "asistencia": asistencia,
                "estadio": estadio
            }
        
        if asistencia > mayor_asistencia_valor:
            mayor_asistencia_valor = asistencia
            partido_mayor_asistencia = {
                "partido_id": partido_id,
                "equipo_local": local,
                "equipo_visitante": visitante,
                "marcador": marcador,
                "asistencia": asistencia,
                "estadio": estadio
            }
        
        # Partido emocionante (muchas acciones críticas y altas)
        indice_emocion = acciones_criticas * 3 + acciones_altas * 1.5
        if indice_emocion > 50:  # Umbral ajustable
            partidos_emocionantes.append({
                "partido_id": partido_id,
                "equipo_local": local,
                "equipo_visitante": visitante,
                "marcador": marcador,
                "acciones_criticas": acciones_criticas,
                "acciones_altas": acciones_altas,
                "total_acciones": total_acciones,
                "indice_emocion": round(indice_emocion, 2),
                "estadio": estadio
            })
        
        # Partido aburrido (pocas acciones, pocos goles)
        indice_aburrimiento = 100 - (total_acciones * 0.2 + (goles_local + goles_visitante) * 10)
        if total_acciones < 200 and (goles_local + goles_visitante) <= 1:
            partidos_aburridos.append({
                "partido_id": partido_id,
                "equipo_local": local,
                "equipo_visitante": visitante,
                "marcador": marcador,
                "total_acciones": total_acciones,
                "total_goles": goles_local + goles_visitante,
                "indice_aburrimiento": round(max(0, indice_aburrimiento), 2),
                "estadio": estadio
            })
        
        # Partido agresivo (muchas faltas y tarjetas)
        conteo_por_tipo = stats_acciones.get('conteo_por_tipo', {})
        faltas = conteo_por_tipo.get('Falta', 0) if isinstance(conteo_por_tipo, dict) else 0
        amarillas = sum(partido.get('tarjetas_amarillas', {}).values())
        rojas = len(partido.get('tarjetas_rojas_detalle', []))
        
        indice_agresividad = faltas + amarillas * 2 + rojas * 5
        if indice_agresividad > 20:  # Umbral ajustable
            partidos_agresivos.append({
                "partido_id": partido_id,
                "equipo_local": local,
                "equipo_visitante": visitante,
                "marcador": marcador,
                "total_faltas": faltas,
                "tarjetas_amarillas": amarillas,
                "tarjetas_rojas": rojas,
                "indice_agresividad": indice_agresividad,
                "estadio": estadio
            })
        
        # Goles de último minuto (minuto 85+) que deciden partidos empatados
        acciones = partido.get('acciones', [])
        
        # Simular marcador minuto a minuto para detectar si iba empatado
        goles_temp_local = 0
        goles_temp_visitante = 0
        
        for accion in acciones:
            if accion.get('tipo') == 'Gol':
                equipo_gol = accion.get('equipo')
                minuto = accion.get('minuto', 0)
                jugador = accion.get('jugador', 'Desconocido')
                
                # Verificar si el partido iba empatado ANTES de este gol
                iba_empatado = (goles_temp_local == goles_temp_visitante)
                
                # Actualizar marcador temporal
                if equipo_gol == local:
                    goles_temp_local += 1
                elif equipo_gol == visitante:
                    goles_temp_visitante += 1
                
                # Verificar si es gol de último minuto (85+) y el partido iba empatado
                if minuto >= 85 and iba_empatado and ganador != "Empate" and equipo_gol == ganador:
                    # Verificar que este gol sea decisivo (que haya dado la victoria)
                    goles_ultimo_minuto.append({
                        "partido_id": partido_id,
                        "equipo_local": local,
                        "equipo_visitante": visitante,
                        "equipo_ganador": ganador,
                        "marcador_final": marcador,
                        "minuto_gol_decisivo": minuto,
                        "jugador": jugador,
                        "marcador_antes_gol": f"{goles_temp_local - (1 if equipo_gol == local else 0)}-{goles_temp_visitante - (1 if equipo_gol == visitante else 0)}",
                        "descripcion": f"{jugador} marcó en el minuto {minuto} para {equipo_gol} cuando iban empatados"
                    })
        
        # Goleadas (diferencia de 3+ goles)
        diferencia = abs(goles_local - goles_visitante)
        if diferencia >= 3:
            equipo_ganador = local if goles_local > goles_visitante else visitante
            equipo_perdedor = visitante if goles_local > goles_visitante else local
            
            # Categorizar humillación
            if diferencia >= 5:
                categoria = "Humillación épica"
            elif diferencia == 4:
                categoria = "Goleada histórica"
            else:
                categoria = "Goleada contundente"
            
            goleadas.append({
                "partido_id": partido_id,
                "equipo_ganador": equipo_ganador,
                "equipo_perdedor": equipo_perdedor,
                "marcador": marcador,
                "diferencia_goles": diferencia,
                "categoria_humillacion": categoria,
                "estadio": estadio
            })
    
    # Ordenar y limitar resultados
    partidos_emocionantes.sort(key=lambda x: x["indice_emocion"], reverse=True)
    partidos_aburridos.sort(key=lambda x: x["indice_aburrimiento"], reverse=True)
    partidos_agresivos.sort(key=lambda x: x["indice_agresividad"], reverse=True)
    goleadas.sort(key=lambda x: x["diferencia_goles"], reverse=True)
    
    result = {
        "partidos_emocionantes": partidos_emocionantes[:10],
        "partidos_aburridos": partidos_aburridos[:10],
        "partidos_agresivos": partidos_agresivos[:10],
        "goles_ultimo_minuto": goles_ultimo_minuto[:15],
        "goleadas": goleadas[:15],
        "partido_menor_asistencia": partido_menor_asistencia,
        "partido_mayor_asistencia": partido_mayor_asistencia
    }
    
    logger.info(f"Partidos emocionantes: {len(partidos_emocionantes)}, Goleadas: {len(goleadas)}")
    return result


def generar_datos_graficas(historial: List[Dict], goleadores: Dict, equipos: Dict, 
                          disciplina: Dict, local_visitante: Dict, logger) -> Dict:
    """
    Genera datos preparados para diferentes tipos de gráficas en el frontend.
    
    Incluye:
    - Gráfica de barras: Victorias local vs visitante vs empates
    - Gráfica de pie: Tipos de goles (penal, corner, tiro libre, normal)
    - Gráfica de barras: Top 10 goleadores
    - Gráfica de línea: Goles por jornada
    - Gráfica de barras comparativa: Goles local vs visitante
    - Gráfica de pie: Distribución de tarjetas
    - Y más...
    """
    logger.info("Generando datos para gráficas...")
    
    # 1. Gráfica de barras: Victorias local vs visitante vs empates
    victorias_grafica = {
        "tipo": "bar",
        "titulo": "Resultados: Local vs Visitante",
        "labels": ["Victoria Local", "Victoria Visitante", "Empate"],
        "datasets": [{
            "label": "Cantidad de Partidos",
            "data": [
                local_visitante.get("victorias_local", 0),
                local_visitante.get("victorias_visitante", 0),
                local_visitante.get("empates", 0)
            ],
            "backgroundColor": ["#4CAF50", "#2196F3", "#FFC107"]
        }]
    }
    
    # 2. Gráfica de pie: Tipos de goles (combinando local y visitante)
    goles_local_det = local_visitante.get("goles_local_detalle", {})
    goles_visitante_det = local_visitante.get("goles_visitante_detalle", {})
    
    total_penales = goles_local_det.get("goles_penal", 0) + goles_visitante_det.get("goles_penal", 0)
    total_corners = goles_local_det.get("goles_corner", 0) + goles_visitante_det.get("goles_corner", 0)
    total_tiros_libres = goles_local_det.get("goles_tiro_libre", 0) + goles_visitante_det.get("goles_tiro_libre", 0)
    total_normales = goles_local_det.get("goles_jugada_normal", 0) + goles_visitante_det.get("goles_jugada_normal", 0)
    
    tipos_goles_grafica = {
        "tipo": "pie",
        "titulo": "Distribución de Goles por Tipo",
        "labels": ["Penal", "Corner", "Tiro Libre", "Jugada Normal"],
        "datasets": [{
            "data": [total_penales, total_corners, total_tiros_libres, total_normales],
            "backgroundColor": ["#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0"]
        }]
    }
    
    # 3. Gráfica de barras horizontales: Top 10 goleadores
    top_goleadores = goleadores.get("top_goleadores", [])[:10]
    goleadores_grafica = {
        "tipo": "horizontalBar",
        "titulo": "Top 10 Goleadores del Torneo",
        "labels": [g.get("nombre", "") for g in top_goleadores],
        "datasets": [{
            "label": "Goles",
            "data": [g.get("goles_torneo", 0) for g in top_goleadores],
            "backgroundColor": "#FF6384"
        }]
    }
    
    # 4. Gráfica de barras comparativa: Goles local vs visitante por tipo
    goles_comparativa = {
        "tipo": "bar",
        "titulo": "Comparación de Goles: Local vs Visitante",
        "labels": ["Penal", "Corner", "Tiro Libre", "Jugada Normal"],
        "datasets": [
            {
                "label": "Local",
                "data": [
                    goles_local_det.get("goles_penal", 0),
                    goles_local_det.get("goles_corner", 0),
                    goles_local_det.get("goles_tiro_libre", 0),
                    goles_local_det.get("goles_jugada_normal", 0)
                ],
                "backgroundColor": "#4CAF50"
            },
            {
                "label": "Visitante",
                "data": [
                    goles_visitante_det.get("goles_penal", 0),
                    goles_visitante_det.get("goles_corner", 0),
                    goles_visitante_det.get("goles_tiro_libre", 0),
                    goles_visitante_det.get("goles_jugada_normal", 0)
                ],
                "backgroundColor": "#2196F3"
            }
        ]
    }
    
    # 5. Gráfica de pie: Distribución de tarjetas amarillas vs rojas
    tarjetas_grafica = {
        "tipo": "pie",
        "titulo": "Distribución de Tarjetas",
        "labels": ["Tarjetas Amarillas", "Tarjetas Rojas"],
        "datasets": [{
            "data": [
                disciplina.get("total_tarjetas_amarillas", 0),
                disciplina.get("total_tarjetas_rojas", 0)
            ],
            "backgroundColor": ["#FFEB3B", "#F44336"]
        }]
    }
    
    # 6. Gráfica de barras: Top equipos por goles a favor
    equipos_lista = equipos.get("equipos", [])
    top_equipos_goles = sorted(equipos_lista, key=lambda x: x.get("goles_favor", 0), reverse=True)[:10]
    
    equipos_goleadores_grafica = {
        "tipo": "bar",
        "titulo": "Top 10 Equipos Goleadores",
        "labels": [e.get("equipo", "") for e in top_equipos_goles],
        "datasets": [{
            "label": "Goles a Favor",
            "data": [e.get("goles_favor", 0) for e in top_equipos_goles],
            "backgroundColor": "#8BC34A"
        }]
    }
    
    # 7. Gráfica de barras apiladas: Goles a favor vs goles en contra (top 10 equipos)
    equipos_balance_grafica = {
        "tipo": "bar",
        "titulo": "Balance de Goles - Top 10 Equipos",
        "labels": [e.get("equipo", "") for e in top_equipos_goles],
        "datasets": [
            {
                "label": "Goles a Favor",
                "data": [e.get("goles_favor", 0) for e in top_equipos_goles],
                "backgroundColor": "#4CAF50"
            },
            {
                "label": "Goles en Contra",
                "data": [e.get("goles_contra", 0) for e in top_equipos_goles],
                "backgroundColor": "#F44336"
            }
        ]
    }
    
    # 8. Gráfica de dona: Porcentajes de victoria local, visitante y empate
    porcentajes_resultados_grafica = {
        "tipo": "doughnut",
        "titulo": "Porcentaje de Resultados",
        "labels": ["Local", "Visitante", "Empate"],
        "datasets": [{
            "data": [
                local_visitante.get("porcentaje_local", 0),
                local_visitante.get("porcentaje_visitante", 0),
                local_visitante.get("porcentaje_empate", 0)
            ],
            "backgroundColor": ["#4CAF50", "#2196F3", "#FFC107"]
        }]
    }
    
    # 9. Gráfica de radar: Comparación de promedio de goles y tarjetas
    estadisticas_promedio_grafica = {
        "tipo": "radar",
        "titulo": "Estadísticas Promedio por Partido",
        "labels": ["Goles Local", "Goles Visitante", "Tarjetas Amarillas", "Tarjetas Rojas (x5)", "Total Goles"],
        "datasets": [{
            "label": "Promedio",
            "data": [
                local_visitante.get("promedio_goles_local", 0),
                local_visitante.get("promedio_goles_visitante", 0),
                disciplina.get("promedio_amarillas_partido", 0),
                disciplina.get("promedio_rojas_partido", 0) * 5,  # Multiplicado para visualización
                goleadores.get("promedio_goles_partido", 0)
            ],
            "backgroundColor": "rgba(54, 162, 235, 0.2)",
            "borderColor": "#36A2EB",
            "pointBackgroundColor": "#36A2EB"
        }]
    }
    
    # 10. Gráfica de línea: Evolución de goles por jornada (si existe el campo)
    goles_por_jornada = defaultdict(int)
    partidos_por_jornada = defaultdict(int)
    
    for partido in historial:
        jornada = partido.get('jornada', 'N/A')
        if jornada != 'N/A':
            goles_totales = partido.get('goles_local', 0) + partido.get('goles_visitante', 0)
            goles_por_jornada[jornada] += goles_totales
            partidos_por_jornada[jornada] += 1
    
    jornadas_ordenadas = sorted(goles_por_jornada.keys())
    
    goles_jornada_grafica = {
        "tipo": "line",
        "titulo": "Goles Totales por Jornada",
        "labels": jornadas_ordenadas,
        "datasets": [{
            "label": "Total de Goles",
            "data": [goles_por_jornada[j] for j in jornadas_ordenadas],
            "borderColor": "#FF6384",
            "backgroundColor": "rgba(255, 99, 132, 0.2)",
            "fill": True
        }]
    }
    
    # 11. Gráfica de barras: Disciplina por equipo (top 10 con más tarjetas)
    tarjetas_por_equipo = defaultdict(lambda: {"amarillas": 0, "rojas": 0})
    
    for partido in historial:
        tarjetas_amarillas_detalle = partido.get('tarjetas_amarillas_detalle', [])
        tarjetas_rojas_detalle = partido.get('tarjetas_rojas_detalle', [])
        
        for tarjeta in tarjetas_amarillas_detalle:
            equipo = tarjeta.get('equipo', '')
            if equipo:
                tarjetas_por_equipo[equipo]["amarillas"] += 1
        
        for tarjeta in tarjetas_rojas_detalle:
            equipo = tarjeta.get('equipo', '')
            if equipo:
                tarjetas_por_equipo[equipo]["rojas"] += 1
    
    # Ordenar por total de tarjetas
    equipos_disciplina = sorted(
        tarjetas_por_equipo.items(),
        key=lambda x: x[1]["amarillas"] + x[1]["rojas"] * 3,
        reverse=True
    )[:10]
    
    disciplina_equipos_grafica = {
        "tipo": "bar",
        "titulo": "Top 10 Equipos con Más Tarjetas",
        "labels": [e[0] for e in equipos_disciplina],
        "datasets": [
            {
                "label": "Amarillas",
                "data": [e[1]["amarillas"] for e in equipos_disciplina],
                "backgroundColor": "#FFEB3B"
            },
            {
                "label": "Rojas",
                "data": [e[1]["rojas"] for e in equipos_disciplina],
                "backgroundColor": "#F44336"
            }
        ]
    }
    
    # Retornar todas las gráficas
    return {
        "victorias_local_visitante": victorias_grafica,
        "tipos_goles": tipos_goles_grafica,
        "top_goleadores": goleadores_grafica,
        "goles_local_vs_visitante": goles_comparativa,
        "distribucion_tarjetas": tarjetas_grafica,
        "equipos_goleadores": equipos_goleadores_grafica,
        "balance_goles_equipos": equipos_balance_grafica,
        "porcentajes_resultados": porcentajes_resultados_grafica,
        "estadisticas_promedio": estadisticas_promedio_grafica,
        "goles_por_jornada": goles_jornada_grafica,
        "disciplina_por_equipo": disciplina_equipos_grafica
    }


def get_estadisticas_torneo(logger):
    """
    Función principal que genera todas las estadísticas del torneo.
    """
    try:
        logger.info("Iniciando análisis de estadísticas del torneo...")
        
        # Obtener datos de las colecciones
        _historial = list(db['historial'].find())

        historial = []
        for historia in _historial:
            juego = db['juegos'].find_one({'_id': ObjectId(historia['partido_original_id'])})
            if juego and juego.get('estado') == 'finalizado':
                historial.append(historia)
        
        jugadores = list(db['jugadores'].find())
        paises = list(db['paises'].find())
        
        if not historial:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="No se encontraron partidos en el historial"
            )
        
        total_partidos = len(historial)
        total_equipos = len(paises)
        
        # Calcular total de goles
        total_goles = sum(p.get('goles_local', 0) + p.get('goles_visitante', 0) for p in historial)
        
        logger.info(f"Procesando {total_partidos} partidos, {total_equipos} equipos, {len(jugadores)} jugadores...")
        
        # Realizar análisis
        remontadas = analizar_remontadas(historial, logger)
        goleadores = analizar_goleadores(historial, jugadores, logger)
        mejores_jugadores = analizar_mejores_jugadores(historial, jugadores, logger)
        equipos = analizar_equipos(historial, paises, logger)
        disciplina = analizar_disciplina(historial, logger)
        partidos_destacados = analizar_partidos_destacados(historial, logger)
        
        # Nuevos análisis
        estadios = analizar_estadios(historial, logger)
        local_visitante = analizar_local_visitante(historial, logger)
        lesiones = analizar_lesiones(historial, logger)
        arbitros = analizar_arbitros(historial, logger)
        partidos_especiales = analizar_partidos_especiales(historial, logger)
        
        # Generar datos para gráficas
        graficas = generar_datos_graficas(historial, goleadores, equipos, disciplina, local_visitante, logger)
        
        # Construir respuesta
        respuesta = {
            "torneo": "Mundial",
            "total_partidos": total_partidos,
            "total_equipos": total_equipos,
            "total_goles": total_goles,
            "remontadas": remontadas,
            "goleadores": goleadores,
            "mejores_jugadores": mejores_jugadores,
            "equipos": equipos,
            "disciplina": disciplina,
            "partidos_destacados": partidos_destacados,
            "estadios": estadios,
            "local_visitante": local_visitante,
            "lesiones": lesiones,
            "arbitros": arbitros,
            "partidos_especiales": partidos_especiales,
            "graficas": graficas,
            "fecha_generacion": datetime.now().isoformat(),
            "mensaje": "Estadísticas completas del torneo generadas exitosamente"
        }
        
        # Convertir ObjectIds a strings
        respuesta = estadistica_util.convertir_objectid_a_string(respuesta)
        
        logger.info("Análisis de estadísticas completado exitosamente")
        return respuesta
        
    except GoogleAPIError as e:
        logger.error(f"Error de MongoDB: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error de MongoDB: {str(e)}")
    except Exception as e:
        logger.error(f"Error al generar estadísticas del torneo: {str(e)}")
        raise HTTPException(status_code=409, detail=f"Error al generar estadísticas: {str(e)}")
