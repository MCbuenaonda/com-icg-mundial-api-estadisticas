from fastapi import HTTPException, status
from google.api_core.exceptions import GoogleAPIError
from pymongo.mongo_client import MongoClient
from Utils import estadistica_util
from Config.settings import MONGODB_URI
from bson.objectid import ObjectId

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
        else:
            pais = estadistica_util.convertir_objectid_a_string(pais)
        
        return pais              
    except GoogleAPIError as e:
        logger.error(f"Error de MongoBD: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error de MongoBD: {str(e)}")
    except Exception as e:
        logger.error(f"Error al obtener el coleccionable: {str(e)}")
        raise HTTPException(status_code=409, detail=f"Error al obtener el coleccionable: {str(e)}")

def get_jugador_detalle(id, logger):
    try:        
        collection = db['jugadores']
        logger.info(f"Consultando coleccionable para el usuario {id}")
        # Ejecutar la consulta
        jugador = collection.find_one({'_id': ObjectId(id)})
        if not jugador:
            logger.info(f"Coleccionable para el usuario {id} no encontrado. Creando nuevo coleccionable.")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Jugador no encontrado")
        else:
            jugador = estadistica_util.convertir_objectid_a_string(jugador)
        
        return jugador              
    except GoogleAPIError as e:
        logger.error(f"Error de MongoBD: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error de MongoBD: {str(e)}")
    except Exception as e:
        logger.error(f"Error al obtener el coleccionable: {str(e)}")
        raise HTTPException(status_code=409, detail=f"Error al obtener el coleccionable: {str(e)}")

def get_ciudad_detalle(id, logger):
    try:        
        collection = db['ciudades']
        logger.info(f"Consultando coleccionable para el usuario {id}")
        # Ejecutar la consulta
        ciudad = collection.find_one({'_id': ObjectId(id)})
        if not ciudad:
            logger.info(f"Coleccionable para el usuario {id} no encontrado. Creando nuevo coleccionable.")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ciudad no encontrada")
        else:
            ciudad = estadistica_util.convertir_objectid_a_string(ciudad)
        
        return ciudad              
    except GoogleAPIError as e:
        logger.error(f"Error de MongoBD: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error de MongoBD: {str(e)}")
    except Exception as e:
        logger.error(f"Error al obtener el coleccionable: {str(e)}")
        raise HTTPException(status_code=409, detail=f"Error al obtener el coleccionable: {str(e)}")
