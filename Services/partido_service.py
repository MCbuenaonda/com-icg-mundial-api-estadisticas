import logging
from fastapi import HTTPException
from bson.objectid import ObjectId
from google.api_core.exceptions import GoogleAPIError
from Config.settings import MONGODB_URI
from pymongo.mongo_client import MongoClient
import requests

# Configurar logger
logger = logging.getLogger(__name__)

client = MongoClient(MONGODB_URI)
db = client['mundial']
collection = db['juegos']


def obtener_partidos(logger):
    try:        
        partidos = collection.find({"estado": "finalizado"})
        return list(partidos)
    except GoogleAPIError as e:
        logger.error(f"Error de MongoBD: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error de MongoBD: {str(e)}")
    except Exception as e:
        logger.error(f"Error al obtener el partido: {str(e)}")
        raise HTTPException(status_code=409, detail=f"Error al obtener el partido: {str(e)}")


