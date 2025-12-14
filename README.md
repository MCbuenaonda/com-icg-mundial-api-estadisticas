# 📊 API de Estadísticas de Fútbol - Mundial

API REST completa para análisis y estadísticas avanzadas de torneos de fútbol, construida con FastAPI y MongoDB.

## 🚀 Características Principales

### Análisis Completo de Torneos
- ✅ **13 Categorías de Estadísticas** incluyendo:
  - Remontadas épicas
  - Goleadores y mejores jugadores
  - Análisis de equipos
  - Disciplina y arbitraje
  - Partidos especiales (emocionantes, aburridos, agresivos)
  - Goleadas y humillaciones
  - Estadios y asistencia
  - Lesiones
  - Y mucho más...

### Endpoints Disponibles

#### Estadísticas de Torneo
```http
GET /api/v1/torneo
```
Retorna análisis completo del torneo con todas las estadísticas.

#### Consultas Individuales
```http
GET /api/v1/pais/{id}          # Estadísticas de un país
GET /api/v1/jugador/{id}        # Estadísticas de un jugador
GET /api/v1/ciudad/{id}         # Estadísticas de una ciudad/estadio
```

## 📋 Requisitos

- Python 3.8+
- MongoDB 4.4+
- FastAPI
- Motor/PyMongo
- Pydantic

## 🔧 Instalación

1. Clonar el repositorio
```bash
git clone <repository_url>
cd com-icg-mundial-api-estadisticas
```

2. Crear entorno virtual
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar dependencias
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno
Crear archivo `.env`:
```env
SECRET_KEY=your_secret_key_here
MONGODB_URI=mongodb://localhost:27017/
```

5. Ejecutar la aplicación
```bash
uvicorn app:app --reload --port 8105
```

## 📖 Documentación

### Documentación Interactiva
Una vez iniciada la aplicación, accede a:
- **Swagger UI**: http://localhost:8105/docs
- **ReDoc**: http://localhost:8105/redoc

### Documentación Detallada
- [Guía Completa de Estadísticas](ESTADISTICAS_TORNEO.md)
- [Ejemplo de Respuesta](ejemplo_respuesta_completa.json)

## 🎯 Uso Rápido

### Con cURL
```bash
curl -X GET "http://localhost:8105/api/v1/torneo" \
  -H "api_key: b480eab3-5544-4a6b-ae34-b5e7e93ead60"
```

### Con Python
```python
import requests

url = "http://localhost:8105/api/v1/torneo"
headers = {"api_key": "b480eab3-5544-4a6b-ae34-b5e7e93ead60"}

response = requests.get(url, headers=headers)
estadisticas = response.json()

print(f"Total partidos: {estadisticas['total_partidos']}")
print(f"Goleador máximo: {estadisticas['goleadores']['goleador_maximo']['nombre']}")
print(f"Remontadas: {estadisticas['remontadas']['total_remontadas']}")
```

### Con JavaScript
```javascript
fetch('http://localhost:8105/api/v1/torneo', {
  headers: {
    'api_key': 'b480eab3-5544-4a6b-ae34-b5e7e93ead60'
  }
})
.then(response => response.json())
.then(data => {
  console.log('Total partidos:', data.total_partidos);
  console.log('Goleador:', data.goleadores.goleador_maximo.nombre);
  console.log('Remontadas:', data.remontadas.total_remontadas);
});
```

## 📊 Estructura de Datos

### Colecciones MongoDB
- `historial` - Historial de partidos con acciones minuto a minuto
- `jugadores` - Información detallada de jugadores
- `paises` - Datos de selecciones nacionales
- `ciudades` - Información de estadios y ubicaciones
- `juegos` - Datos de partidos programados

### Schemas Pydantic
- `Schemas/estadisticas_torneo.py` - Modelos de respuesta
- `Schemas/historial.py` - Modelo de historial de partido
- `Schemas/jugador.py` - Modelo de jugador
- `Schemas/pais.py` - Modelo de país
- `Schemas/juego.py` - Modelo de juego
- `Schemas/ciudad.py` - Modelo de ciudad

## 🏗️ Estructura del Proyecto

```
com-icg-mundial-api-estadisticas/
├── app.py                          # Aplicación principal FastAPI
├── Config/
│   └── settings.py                 # Configuración global
├── Routes/
│   ├── estadistica_route.py        # Rutas de estadísticas
│   └── test_route.py               # Rutas de prueba
├── Services/
│   ├── estadistica_service.py      # Lógica de negocio básica
│   └── analisis_torneo_service.py  # Análisis avanzado de torneos
├── Schemas/
│   ├── estadisticas_torneo.py      # Modelos de estadísticas
│   ├── historial.py                # Modelo de historial
│   ├── jugador.py                  # Modelo de jugador
│   ├── pais.py                     # Modelo de país
│   ├── juego.py                    # Modelo de juego
│   └── ciudad.py                   # Modelo de ciudad
├── Utils/
│   └── estadistica_util.py         # Utilidades
├── ESTADISTICAS_TORNEO.md          # Documentación detallada
├── ejemplo_respuesta_completa.json # Ejemplo de respuesta
├── requests.http                   # Ejemplos de peticiones
└── requirements.txt                # Dependencias
```

## 🎨 Ejemplos de Análisis

### Remontadas Épicas
Encuentra partidos donde un equipo estaba perdiendo por 2+ goles y terminó ganando:
```json
{
  "remontadas": {
    "total_remontadas": 5,
    "remontadas_2_goles": 3,
    "remontadas_3_o_mas_goles": 2,
    "partidos": [...]
  }
}
```

### Goleadas y Humillaciones
Partidos con diferencias de 3+ goles, categorizados por nivel de humillación:
```json
{
  "goleadas": [
    {
      "equipo_ganador": "España",
      "equipo_perdedor": "Costa Rica",
      "marcador": "7-0",
      "diferencia_goles": 7,
      "categoria_humillacion": "Humillación épica"
    }
  ]
}
```

### Partidos Emocionantes
Basado en un índice de emoción calculado con acciones críticas:
```json
{
  "partidos_emocionantes": [
    {
      "equipo_local": "Argentina",
      "equipo_visitante": "Francia",
      "marcador": "3-3",
      "indice_emocion": 151.5,
      "acciones_criticas": 28
    }
  ]
}
```

### Goles de Último Minuto
Goles decisivos marcados en el minuto 85 o posterior:
```json
{
  "goles_ultimo_minuto": [
    {
      "equipo_ganador": "Alemania",
      "jugador": "Toni Kroos",
      "minuto_gol_decisivo": 90,
      "descripcion": "Toni Kroos marcó en el minuto 90 para Alemania"
    }
  ]
}
```

## 🔐 Seguridad

- Autenticación mediante API Key en headers
- Validación de datos con Pydantic
- Protección CORS configurada
- Manejo de errores centralizado

## 🧪 Testing

Para probar los endpoints, puedes usar el archivo `requests.http` con la extensión REST Client de VS Code:

```http
GET http://127.0.0.1:8105/api/v1/torneo
api-key: b480eab3-5544-4a6b-ae34-b5e7e93ead60
```

## 📈 Rendimiento

- Procesamiento de 64+ partidos en ~2-5 segundos
- Análisis de 700+ jugadores
- Generación de 13 categorías de estadísticas
- Cálculo de índices de emoción, agresividad y aburrimiento

### Optimizaciones Recomendadas
- Implementar caché con Redis
- Indexar colecciones MongoDB
- Paginación para listas grandes
- Compresión de respuestas

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT.

## 👥 Autores

- Desarrollador Principal - [@tu_usuario](https://github.com/tu_usuario)

## 🙏 Agradecimientos

- FastAPI por el excelente framework
- MongoDB por la base de datos flexible
- Pydantic por la validación de datos

## 📞 Soporte

Para soporte y preguntas:
- 📧 Email: soporte@ejemplo.com
- 💬 Issues: [GitHub Issues](https://github.com/tu_usuario/repo/issues)
- 📖 Docs: [Documentación Completa](ESTADISTICAS_TORNEO.md)

---

⭐️ Si este proyecto te fue útil, considera darle una estrella en GitHub!
