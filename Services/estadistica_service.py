from fastapi import HTTPException, status
from google.api_core.exceptions import GoogleAPIError
from pymongo.mongo_client import MongoClient
from Utils import estadistica_util
from Config.settings import MONGODB_URI
from bson.objectid import ObjectId
from datetime import datetime
from collections import defaultdict
from typing import List, Dict, Any
from Schemas.jugador import (
    PerfilGeneral, AtributosFisicosTecnicos, EstadoActual, HistorialTemporada,
    DatosDescriptivos, ProbabilidadesPredictivas, PrecisionBajoPresion,
    EstadisticasAnaliticas, JugadorDetalleResponse
)

client = MongoClient(MONGODB_URI)
db = client['mundial'] 

def get_pais_detalle(id, logger):
    try:        
        collection = db['paises']
        logger.info(f"Consultando coleccionable para el usuario {id}")
        # Ejecutar la consulta
        pais = collection.find_one({'_id': ObjectId(id)})
        
        if not pais:
            logger.info(f"Coleccionable para el usuario {id} no encontrado. Creando nuevo coleccionable.")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pais no encontrado")
        
        pais['partidos'] = list(db['historial'].find({"equipo_local": pais['nombre']})) + list(db['historial'].find({"equipo_visitante": pais['nombre']}))
        pais = estadistica_util.convertir_objectid_a_string(pais)
        
        return pais              
    except GoogleAPIError as e:
        logger.error(f"Error de MongoBD: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error de MongoBD: {str(e)}")
    except Exception as e:
        logger.error(f"Error al obtener el coleccionable: {str(e)}")
        raise HTTPException(status_code=409, detail=f"Error al obtener el coleccionable: {str(e)}")

def get_jugador_basic(id, logger):
    try:        
        collection = db['jugadores']
        logger.info(f"Consultando jugador con id {id}")
        
        # Ejecutar la consulta
        jugador = collection.find_one({'_id': ObjectId(id)})
        
        if not jugador:
            logger.info(f"Jugador con id {id} no encontrado.")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Jugador no encontrado")
        
        # Obtener información del país
        pais_info = db['paises'].find_one({'id': jugador.get('pais_id')})
        jugador['pais'] = pais_info['nombre'] if pais_info else 'Desconocido'
        
        # Obtener historial de partidos
        filtro_busqueda = {
            "acciones.jugador": jugador['nombre'],
            "acciones.equipo": jugador['pais']
        }
        partidos = list(db['historial'].find(filtro_busqueda))
        jugador['partidos'] = partidos
        
        # Convertir ObjectId a string
        jugador = estadistica_util.convertir_objectid_a_string(jugador)
        
        return jugador              
    except GoogleAPIError as e:
        logger.error(f"Error de MongoDB: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error de MongoDB: {str(e)}")
    except Exception as e:
        logger.error(f"Error al obtener el jugador: {str(e)}")
        raise HTTPException(status_code=409, detail=f"Error al obtener el jugador: {str(e)}")


def get_jugador_detalle(id, logger):
    try:        
        collection = db['jugadores']
        logger.info(f"Consultando jugador con id {id}")
        
        # Ejecutar la consulta
        jugador = collection.find_one({'_id': ObjectId(id)})
        
        if not jugador:
            logger.info(f"Jugador con id {id} no encontrado.")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Jugador no encontrado")
        
        # Obtener información del país
        pais_info = db['paises'].find_one({'id': jugador.get('pais_id')})
        jugador['pais'] = pais_info['nombre'] if pais_info else 'Desconocido'
        
        # Obtener historial de partidos
        filtro_busqueda = {
            "acciones.jugador": jugador['nombre'],
            "acciones.equipo": jugador['pais']
        }
        partidos = list(db['historial'].find(filtro_busqueda))
        jugador['partidos'] = partidos
        
        # Extraer todas las acciones del jugador
        acciones_jugador = estadistica_util.obtener_todas_acciones_jugador(partidos, jugador['nombre'])
        
        # Calcular estadísticas adicionales
        partidos_jugados = len(partidos) if len(partidos) > 0 else 1
        
        # ========== DATOS DESCRIPTIVOS ==========
        
        # Perfil general
        perfil_general = PerfilGeneral(
            nombre=jugador.get('nombre', 'Desconocido'),
            posicion=estadistica_util.mapear_posicion(jugador.get('posicion_id', 0)),
            pie_habil=jugador.get('pie_habil', 'derecho'),
            numero=jugador.get('numero', 0),
            equipo_pais=jugador['pais'],
            titular=bool(jugador.get('titular', 0))
        )
        
        # Atributos físicos y técnicos
        velocidad = int(jugador.get('velocidad', 70))
        resistencia = int(jugador.get('resistencia', 70))
        fuerza_fisica = int(jugador.get('fuerza_fisica', 70))
        control_balon = int(jugador.get('control_balon', 70))
        regate = int(jugador.get('regate', 70))
        precision_pase = int(jugador.get('precision_pase', 70))
        
        fisico_promedio = (velocidad + resistencia + fuerza_fisica) / 3
        tecnico_promedio = (control_balon + regate + precision_pase) / 3
        
        lista_atributos = {
            'precision_tiro': int(jugador.get('precision_tiro', 70)),
            'precision_pase': int(jugador.get('precision_pase', 70)),
            'regate': int(jugador.get('regate', 70)),
            'fuerza_disparo': int(jugador.get('fuerza_disparo', 70)),
            'vision_juego': int(jugador.get('vision_juego', 70)),
            'anticipacion': int(jugador.get('anticipacion', 70)),
            'control_balon': int(jugador.get('control_balon', 70)),
            'juego_aereo': int(jugador.get('juego_aereo', 70)),
            'velocidad': velocidad,
            'resistencia': resistencia,
            'fuerza_fisica': fuerza_fisica,
            'agilidad': int(jugador.get('agilidad', 70)),
            'compostura': int(jugador.get('compostura', 70)),
            'agresividad': int(jugador.get('agresividad', 50)),
            'concentracion': int(jugador.get('concentracion', 70))
        }
        
        atributos_fisicos_tecnicos = AtributosFisicosTecnicos(
            fisico=round(fisico_promedio, 2),
            tecnico=round(tecnico_promedio, 2),
            lista_completa=lista_atributos
        )
        
        # Estado actual
        bonificaciones_lista = []
        if jugador.get('especialista_penales'):
            bonificaciones_lista.append('Especialista en penales')
        if jugador.get('especialista_tiros_libres'):
            bonificaciones_lista.append('Especialista en tiros libres')
        if jugador.get('bonificaciones'):
            bonificaciones_lista.extend(jugador.get('bonificaciones', []))
        
        estado_actual = EstadoActual(
            rendimiento=int(jugador.get('rendimiento', 70)),
            forma_actual=int(jugador.get('forma_actual', 70)),
            moral=int(jugador.get('moral', 70)),
            bonificaciones=bonificaciones_lista
        )
        
        # Historial temporada
        asistencias_calculadas = estadistica_util.calcular_asistencias(acciones_jugador)
        
        historial_temporada = HistorialTemporada(
            goles_totales=jugador.get('goles', 0) + jugador.get('goles_temp', 0),
            asistencias=asistencias_calculadas,
            faltas_acumuladas=jugador.get('faltas', 0) + jugador.get('faltas_temp', 0),
            lesiones_total=jugador.get('lesiones', 0)
        )
        
        datos_descriptivos = DatosDescriptivos(
            perfil_general=perfil_general,
            atributos_fisicos_tecnicos=atributos_fisicos_tecnicos,
            estado_actual=estado_actual,
            historial_temporada=historial_temporada
        )
        
        # ========== PROBABILIDADES PREDICTIVAS ==========
        
        probabilidades_predictivas = ProbabilidadesPredictivas(
            exito_pases=round(estadistica_util.calcular_probabilidad_exito_pases(jugador, acciones_jugador), 2),
            precision_tiros=round(estadistica_util.calcular_probabilidad_precision_tiros(jugador, acciones_jugador), 2),
            exito_regates=round(estadistica_util.calcular_probabilidad_exito_regates(jugador, acciones_jugador), 2),
            recuperaciones=round(estadistica_util.calcular_probabilidad_recuperaciones(jugador, acciones_jugador), 2),
            fatiga_desgaste=round(estadistica_util.calcular_fatiga_desgaste(jugador, acciones_jugador), 2),
            faltas_cometidas=round(estadistica_util.calcular_probabilidad_faltas(jugador, acciones_jugador), 2),
            contribucion_gol=round(estadistica_util.calcular_contribucion_gol(jugador, acciones_jugador, partidos_jugados), 2)
        )
        
        # ========== ESTADÍSTICAS ANALÍTICAS ==========
        
        # Calcular total de acciones del equipo
        total_acciones_equipo = 0
        for partido in partidos:
            if 'acciones' in partido:
                acciones_equipo = [a for a in partido['acciones'] if a.get('equipo') == jugador['pais']]
                total_acciones_equipo += len(acciones_equipo)
        
        if total_acciones_equipo == 0:
            total_acciones_equipo = 1
        
        # Calcular minutos totales
        minutos_totales = 0
        if len(acciones_jugador) > 0:
            minutos_totales = max([a.get('minuto', 0) for a in acciones_jugador])
        
        precision_presion = estadistica_util.calcular_precision_bajo_presion(acciones_jugador)
        
        estadisticas_analiticas = EstadisticasAnaliticas(
            tasa_posesion_individual=round(estadistica_util.calcular_tasa_posesion_individual(
                acciones_jugador, total_acciones_equipo), 2),
            pases_clave=estadistica_util.calcular_pases_clave(acciones_jugador),
            precision_bajo_presion=PrecisionBajoPresion(
                medio_central=round(precision_presion.get('medio_central', 0), 2),
                defensivo=round(precision_presion.get('defensivo', 0), 2),
                ofensivo=round(precision_presion.get('ofensivo', 0), 2)
            ),
            duelos_aereos_ganados=round(estadistica_util.calcular_duelos_aereos(jugador, acciones_jugador), 2),
            indice_creacion=round(estadistica_util.calcular_indice_creacion(jugador, acciones_jugador, minutos_totales), 2),
            eficiencia_defensiva=round(estadistica_util.calcular_eficiencia_defensiva(jugador, acciones_jugador), 2),
            mapa_calor=estadistica_util.calcular_mapa_calor(acciones_jugador),
            impacto_resultado=round(estadistica_util.calcular_impacto_resultado(acciones_jugador), 2),
            tendencia_forma=round(estadistica_util.calcular_tendencia_forma(jugador, acciones_jugador), 2)
        )
        
        # Convertir ObjectId a string
        jugador = estadistica_util.convertir_objectid_a_string(jugador)
        
        # Crear respuesta completa
        respuesta = JugadorDetalleResponse(
            jugador_base=jugador,
            datos_descriptivos=datos_descriptivos,
            probabilidades_predictivas=probabilidades_predictivas,
            estadisticas_analiticas=estadisticas_analiticas
        )
        
        return respuesta.dict()
              
    except GoogleAPIError as e:
        logger.error(f"Error de MongoDB: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error de MongoDB: {str(e)}")
    except Exception as e:
        logger.error(f"Error al obtener el jugador: {str(e)}")
        raise HTTPException(status_code=409, detail=f"Error al obtener el jugador: {str(e)}")

def get_ciudad_detalle(id, logger):
    try:        
        collection = db['ciudades']
        logger.info(f"Consultando coleccionable para el usuario {id}")
        # Ejecutar la consulta
        ciudad = collection.find_one({'_id': ObjectId(id)})
        
        if not ciudad:
            logger.info(f"Coleccionable para el usuario {id} no encontrado. Creando nuevo coleccionable.")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ciudad no encontrada")
        
        ciudad['pais'] = db['paises'].find_one({'id': ciudad['pais_id']})['nombre']        
        ciudad['partidos'] = list(db['historial'].find({"ubicacion.ciudad": ciudad['nombre'], "ubicacion.pais": ciudad['pais']}))
        ciudad = estadistica_util.convertir_objectid_a_string(ciudad)
        
        return ciudad              
    except GoogleAPIError as e:
        logger.error(f"Error de MongoBD: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error de MongoBD: {str(e)}")
    except Exception as e:
        logger.error(f"Error al obtener el coleccionable: {str(e)}")
        raise HTTPException(status_code=409, detail=f"Error al obtener el coleccionable: {str(e)}")
