from bson.objectid import ObjectId
import math
from collections import Counter, defaultdict
from typing import List, Dict, Any

def convertir_objectid_a_string(obj):
        """Función recursiva para convertir todos los ObjectId a string en un objeto"""
        if isinstance(obj, ObjectId):
            return str(obj)
        elif isinstance(obj, dict):
            return {key: convertir_objectid_a_string(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [convertir_objectid_a_string(item) for item in obj]
        else:
            return obj


# ========== FUNCIONES DE CÁLCULO DE ESTADÍSTICAS DE JUGADOR ==========

def obtener_todas_acciones_jugador(partidos: List[Dict], nombre_jugador: str) -> List[Dict]:
    """Extrae todas las acciones de un jugador de su historial de partidos"""
    acciones_jugador = []
    for partido in partidos:
        if 'acciones' in partido:
            for accion in partido['acciones']:
                if accion.get('jugador') == nombre_jugador:
                    acciones_jugador.append(accion)
    return acciones_jugador

def mapear_posicion(posicion_id: int) -> str:
    """Mapea el ID de posición a su nombre"""
    mapeo_posiciones = {
        1: 'Portero',
        2: 'Defensa Central',
        3: 'Lateral Derecho',
        4: 'Lateral Izquierdo',
        5: 'Mediocampista Defensivo',
        6: 'Mediocampista Central',
        7: 'Mediocampista Ofensivo',
        8: 'Extremo Derecho',
        9: 'Extremo Izquierdo',
        10: 'Delantero Centro'
    }
    return mapeo_posiciones.get(posicion_id, 'Desconocido')

def calcular_asistencias(acciones: List[Dict]) -> int:
    """Calcula asistencias contando pases exitosos seguidos de gol en <30 segundos"""
    asistencias = 0
    for i in range(len(acciones) - 1):
        accion_actual = acciones[i]
        accion_siguiente = acciones[i + 1]
        
        # Verificar si el pase fue exitoso
        if (accion_actual.get('tipo') == 'Pase' and 
            accion_actual.get('exito') and
            accion_siguiente.get('tipo') == 'Gol'):
            
            # Verificar diferencia de tiempo (30 segundos)
            tiempo_actual = accion_actual.get('minuto', 0) * 60 + accion_actual.get('segundo', 0)
            tiempo_siguiente = accion_siguiente.get('minuto', 0) * 60 + accion_siguiente.get('segundo', 0)
            
            if abs(tiempo_siguiente - tiempo_actual) <= 30:
                asistencias += 1
    
    return asistencias

def calcular_probabilidad_exito_pases(jugador: Dict, acciones: List[Dict]) -> float:
    """Calcula la probabilidad de éxito en pases"""
    precision_pase = jugador.get('precision_pase', 70)
    vision_juego = jugador.get('vision_juego', 70)
    
    # Contar pases en acciones
    pases = [a for a in acciones if a.get('tipo') == 'Pase']
    if len(pases) == 0:
        return (precision_pase + vision_juego) / 200 * 100
    
    pases_exitosos = len([p for p in pases if p.get('exito')])
    tasa_historica = pases_exitosos / len(pases)
    
    return ((precision_pase + vision_juego) / 200 * 100) * tasa_historica

def calcular_probabilidad_precision_tiros(jugador: Dict, acciones: List[Dict]) -> float:
    """Calcula la precisión de tiros"""
    precision_tiro = jugador.get('precision_tiro', 70)
    
    # Contar tiros
    tiros = [a for a in acciones if a.get('tipo') == 'Tiro']
    if len(tiros) == 0:
        return precision_tiro
    
    tiros_exitosos = len([t for t in tiros if t.get('exito')])
    atajadas = len([a for a in acciones if a.get('tipo') == 'Atajada'])
    
    tiros_efectivos = max(tiros_exitosos - atajadas, 0)
    tasa_historica = tiros_efectivos / len(tiros) if len(tiros) > 0 else 0
    
    probabilidad_base = (precision_tiro / 100 * 100) * tasa_historica
    
    # Bonus si tira desde área chica
    tiros_area_chica = [t for t in tiros if 'area_chica' in t.get('sector', '').lower()]
    if len(tiros_area_chica) > 0:
        probabilidad_base += 10
    
    return min(probabilidad_base, 100)

def calcular_probabilidad_exito_regates(jugador: Dict, acciones: List[Dict]) -> float:
    """Calcula la probabilidad de éxito en regates"""
    regate = jugador.get('regate', 70)
    
    # Contar regates
    regates = [a for a in acciones if a.get('tipo') == 'Regate']
    if len(regates) == 0:
        return regate
    
    regates_exitosos = len([r for r in regates if r.get('exito')])
    tasa_historica = regates_exitosos / len(regates)
    
    probabilidad_base = (regate / 100 * 100) * tasa_historica
    
    # Bonus en medio central
    regates_medio = [r for r in regates if 'medio_central' in r.get('sector', '').lower()]
    if len(regates_medio) > 0:
        probabilidad_base += 5
    
    return min(probabilidad_base, 100)

def calcular_probabilidad_recuperaciones(jugador: Dict, acciones: List[Dict]) -> float:
    """Calcula la probabilidad de recuperaciones de balón"""
    anticipacion = jugador.get('anticipacion', 70)
    agresividad = jugador.get('agresividad', 50)
    
    # Contar acciones defensivas
    entradas = [a for a in acciones if a.get('tipo') == 'Entrada']
    intercepciones = [a for a in acciones if a.get('tipo') == 'Intercepcion']
    
    total_acciones = len(entradas) + len(intercepciones)
    if total_acciones == 0:
        return (anticipacion + agresividad) / 200 * 100
    
    exitosas = len([a for a in entradas if a.get('exito')]) + len([a for a in intercepciones if a.get('exito')])
    tasa_historica = exitosas / total_acciones
    
    return ((anticipacion + agresividad) / 200 * 100) * tasa_historica

def calcular_fatiga_desgaste(jugador: Dict, acciones: List[Dict]) -> float:
    """Calcula el nivel de fatiga/desgaste"""
    resistencia = jugador.get('resistencia', 70)
    
    # Obtener minutos jugados
    if len(acciones) == 0:
        minutos_jugados = 0
    else:
        minutos_jugados = max([a.get('minuto', 0) for a in acciones])
    
    fatiga = 100 - (resistencia / 100 * 100 * math.exp(-minutos_jugados / 90))
    return max(0, min(fatiga, 100))

def calcular_probabilidad_faltas(jugador: Dict, acciones: List[Dict]) -> float:
    """Calcula la probabilidad de cometer faltas"""
    agresividad = jugador.get('agresividad', 50)
    
    # Contar acciones físicas y faltas
    acciones_fisicas = [a for a in acciones if a.get('tipo') in ['Entrada', 'Falta', 'Intercepcion']]
    if len(acciones_fisicas) == 0:
        return agresividad / 2
    
    faltas = len([a for a in acciones if a.get('tipo') == 'Falta'])
    tasa_historica = faltas / len(acciones_fisicas)
    
    return (agresividad / 100 * 100) * tasa_historica

def calcular_contribucion_gol(jugador: Dict, acciones: List[Dict], partidos_jugados: int) -> float:
    """Calcula la contribución al gol"""
    vision_juego = jugador.get('vision_juego', 70)
    fuerza_disparo = jugador.get('fuerza_disparo', 70)
    goles_temp = jugador.get('goles_temp', 0)
    
    asistencias = calcular_asistencias(acciones)
    
    if partidos_jugados == 0:
        partidos_jugados = 1
    
    contribucion = ((vision_juego + fuerza_disparo) / 200 * 100) * ((goles_temp + asistencias) / partidos_jugados)
    return contribucion

def calcular_tasa_posesion_individual(acciones: List[Dict], total_acciones_equipo: int) -> float:
    """Calcula la tasa de posesión individual"""
    acciones_control = [a for a in acciones if a.get('tipo') in ['Pase', 'Regate'] and a.get('exito')]
    
    if total_acciones_equipo == 0:
        return 0
    
    return (len(acciones_control) / total_acciones_equipo) * 100

def calcular_pases_clave(acciones: List[Dict]) -> int:
    """Calcula los pases clave (que conducen a tiro)"""
    pases_clave = 0
    for i in range(len(acciones) - 1):
        if (acciones[i].get('tipo') == 'Pase' and 
            acciones[i].get('exito') and
            acciones[i + 1].get('tipo') == 'Tiro'):
            
            tiempo_actual = acciones[i].get('minuto', 0) * 60 + acciones[i].get('segundo', 0)
            tiempo_siguiente = acciones[i + 1].get('minuto', 0) * 60 + acciones[i + 1].get('segundo', 0)
            
            if abs(tiempo_siguiente - tiempo_actual) <= 30:
                pases_clave += 1
    
    return pases_clave

def calcular_precision_bajo_presion(acciones: List[Dict]) -> Dict[str, float]:
    """Calcula la precisión bajo presión por sector"""
    sectores = defaultdict(lambda: {'total': 0, 'exitos': 0})
    
    for accion in acciones:
        sector = accion.get('sector', 'desconocido')
        if accion.get('tipo') in ['Pase', 'Tiro', 'Regate']:
            sectores[sector]['total'] += 1
            if accion.get('exito'):
                sectores[sector]['exitos'] += 1
    
    precision = {}
    for sector, datos in sectores.items():
        if datos['total'] > 0:
            precision[sector] = (datos['exitos'] / datos['total']) * 100
        else:
            precision[sector] = 0
    
    return {
        'medio_central': precision.get('medio_central', 0),
        'defensivo': precision.get('defensivo', 0) + precision.get('defensivo_lateral_derecho', 0) + precision.get('defensivo_lateral_izquierdo', 0),
        'ofensivo': precision.get('ofensivo', 0) + precision.get('ofensivo_central', 0) + precision.get('ofensivo_area_chica', 0)
    }

def calcular_duelos_aereos(jugador: Dict, acciones: List[Dict]) -> float:
    """Calcula el porcentaje de duelos aéreos ganados"""
    juego_aereo = jugador.get('juego_aereo', 70)
    
    despejes = [a for a in acciones if a.get('tipo') == 'Despeje']
    if len(despejes) == 0:
        return juego_aereo
    
    despejes_exitosos = len([d for d in despejes if d.get('exito')])
    tasa_historica = despejes_exitosos / len(despejes)
    
    return (tasa_historica * 100) * (juego_aereo / 100)

def calcular_indice_creacion(jugador: Dict, acciones: List[Dict], minutos_totales: float) -> float:
    """Calcula el índice de creación de juego"""
    goles_temp = jugador.get('goles_temp', 0)
    asistencias = calcular_asistencias(acciones)
    pases_clave = calcular_pases_clave(acciones)
    
    if minutos_totales == 0:
        return 0
    
    partidos_90min = minutos_totales / 90
    if partidos_90min == 0:
        return 0
    
    return (goles_temp + asistencias + pases_clave) / partidos_90min

def calcular_eficiencia_defensiva(jugador: Dict, acciones: List[Dict]) -> float:
    """Calcula la eficiencia defensiva"""
    entradas = [a for a in acciones if a.get('tipo') == 'Entrada']
    intercepciones = [a for a in acciones if a.get('tipo') == 'Intercepcion']
    
    exitos_entrada = len([e for e in entradas if e.get('exito')])
    exitos_intercepcion = len([i for i in intercepciones if i.get('exito')])
    
    faltas_temp = jugador.get('faltas_temp', 0)
    
    return (exitos_entrada + exitos_intercepcion) - faltas_temp

def calcular_mapa_calor(acciones: List[Dict]) -> Dict[str, float]:
    """Calcula el mapa de calor (distribución por sectores)"""
    conteo_sectores = Counter([a.get('sector', 'desconocido') for a in acciones])
    total = sum(conteo_sectores.values())
    
    if total == 0:
        return {}
    
    return {sector: (count / total) * 100 for sector, count in conteo_sectores.items()}

def calcular_impacto_resultado(acciones: List[Dict]) -> float:
    """Calcula el impacto en el resultado del partido"""
    pesos_importancia = {
        'critica': 2.0,
        'alta': 1.5,
        'media': 1.0,
        'baja': 0.5
    }
    
    impacto_total = 0
    for accion in acciones:
        importancia = accion.get('importancia', 'baja').lower()
        peso = pesos_importancia.get(importancia, 0.5)
        exito = 1 if accion.get('exito') else 0
        impacto_total += peso * exito
    
    return impacto_total

def calcular_tendencia_forma(jugador: Dict, acciones: List[Dict]) -> float:
    """Calcula la tendencia de forma"""
    forma_actual = jugador.get('forma_actual', 70)
    
    # Contar fallos recientes
    if len(acciones) == 0:
        return 0
    
    # Últimas 10 acciones
    acciones_recientes = acciones[-10:] if len(acciones) >= 10 else acciones
    fallos = len([a for a in acciones_recientes if not a.get('exito')])
    
    # Calcular rendimiento promedio post-acciones
    rendimiento_post = forma_actual
    if fallos > 3:
        rendimiento_post -= 5
    
    return rendimiento_post - forma_actual