from fastapi import APIRouter, HTTPException
from Config.settings import PREFIX_SERVER_PATH
from Services import estadistica_service
import logging
import uuid 

route = APIRouter(prefix=PREFIX_SERVER_PATH)
tag = 'Estadistica'
process_uuid = uuid.uuid4()

logging.basicConfig(level=logging.INFO, format=f'%(asctime)s - %(levelname)s - {process_uuid} - %(message)s')
logger = logging.getLogger(__name__)


@route.get("/pais/{id}", tags=[tag])
def get_pais_route(id: str):
    try:
        respuesta = estadistica_service.get_pais_detalle(id, logger)        
        return respuesta
    except Exception as e:
        logger.error(f"Error al obtener estadisticas: {str(e)}")
        raise HTTPException(status_code=409, detail=f"Error al obtener estadisticas: {str(e)}")

@route.get("/jugador/{id}", tags=[tag])
def get_jugador_route(id: str):
    try:
        respuesta = estadistica_service.get_jugador_detalle(id, logger)        
        return respuesta
    except Exception as e:
        logger.error(f"Error al obtener estadisticas: {str(e)}")
        raise HTTPException(status_code=409, detail=f"Error al obtener estadisticas: {str(e)}")
    
@route.get("/ciudad/{id}", tags=[tag])
def get_ciudad_route(id: str):
    try:
        respuesta = estadistica_service.get_ciudad_detalle(id, logger)        
        return respuesta
    except Exception as e:
        logger.error(f"Error al obtener estadisticas: {str(e)}")
        raise HTTPException(status_code=409, detail=f"Error al obtener estadisticas: {str(e)}")