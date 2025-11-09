from bson.objectid import ObjectId

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