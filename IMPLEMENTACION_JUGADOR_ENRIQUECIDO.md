# Documentación de Implementación - Endpoint Jugador Enriquecido

## Resumen de Cambios

Se ha enriquecido el endpoint `GET /api/v1/jugador/{player_id}` para incluir estadísticas detalladas, probabilidades predictivas y analíticas de rendimiento del jugador.

## Archivos Modificados

### 1. `Schemas/jugador.py`
Se agregaron los siguientes modelos Pydantic:

- **PerfilGeneral**: Información básica (nombre, posición, pie hábil, número, equipo/país, titular)
- **AtributosFisicosTecnicos**: Promedios físicos y técnicos + lista completa de atributos
- **EstadoActual**: Rendimiento, forma actual, moral y bonificaciones
- **HistorialTemporada**: Goles totales, asistencias, faltas acumuladas, lesiones
- **DatosDescriptivos**: Agrupa todos los datos descriptivos
- **ProbabilidadesPredictivas**: 7 probabilidades calculadas (pases, tiros, regates, recuperaciones, fatiga, faltas, contribución)
- **PrecisionBajoPresion**: Precisión por sector (medio central, defensivo, ofensivo)
- **EstadisticasAnaliticas**: Métricas avanzadas (tasa posesión, pases clave, duelos aéreos, índice creación, etc.)
- **JugadorDetalleResponse**: Modelo de respuesta completo

### 2. `Utils/estadistica_util.py`
Se agregaron 20+ funciones de cálculo:

#### Funciones de Extracción y Mapeo:
- `obtener_todas_acciones_jugador()`: Extrae acciones del historial de partidos
- `mapear_posicion()`: Convierte posicion_id a nombre descriptivo

#### Funciones de Cálculo de Estadísticas Básicas:
- `calcular_asistencias()`: Cuenta pases exitosos seguidos de gol en <30 segundos

#### Funciones de Probabilidades Predictivas:
- `calcular_probabilidad_exito_pases()`: Basado en precision_pase + vision_juego + historial
- `calcular_probabilidad_precision_tiros()`: Basado en precision_tiro + historial + bonus por sector
- `calcular_probabilidad_exito_regates()`: Basado en regate + historial + bonus medio central
- `calcular_probabilidad_recuperaciones()`: Basado en anticipacion + agresividad + historial
- `calcular_fatiga_desgaste()`: Modelo exponencial basado en resistencia y minutos jugados
- `calcular_probabilidad_faltas()`: Basado en agresividad + ratio faltas/acciones físicas
- `calcular_contribucion_gol()`: Basado en vision + fuerza_disparo + (goles + asistencias) por partido

#### Funciones de Estadísticas Analíticas:
- `calcular_tasa_posesion_individual()`: % de acciones de control exitosas vs equipo
- `calcular_pases_clave()`: Pases que conducen a tiro en <30 segundos
- `calcular_precision_bajo_presion()`: Precisión por sector del campo
- `calcular_duelos_aereos()`: % de despejes exitosos ajustado por juego_aereo
- `calcular_indice_creacion()`: (goles + asistencias + pases clave) por 90 minutos
- `calcular_eficiencia_defensiva()`: (entradas + intercepciones exitosas) - faltas
- `calcular_mapa_calor()`: Distribución % de acciones por sector
- `calcular_impacto_resultado()`: Suma ponderada de acciones exitosas por importancia
- `calcular_tendencia_forma()`: Cambio de forma basado en fallos recientes

### 3. `Services/estadistica_service.py`
Se modificó la función `get_jugador_detalle()`:

- Extrae todas las acciones del jugador del historial de partidos
- Calcula todas las métricas usando las funciones de `estadistica_util`
- Construye la respuesta usando los modelos Pydantic
- Retorna un objeto JSON estructurado con:
  - `jugador_base`: Todos los datos originales del jugador
  - `datos_descriptivos`: Información organizada y derivada
  - `probabilidades_predictivas`: 7 métricas de probabilidad
  - `estadisticas_analiticas`: 9 métricas analíticas avanzadas

## Estructura de la Respuesta JSON

```json
{
  "jugador_base": {
    "_id": "68ed9d63d8343c17bb6424f2",
    "nombre": "Lionel Messi",
    "posicion_id": 10,
    "pais": "Argentina",
    "goles": 5,
    "goles_temp": 3,
    "precision_tiro": 94,
    "precision_pase": 91,
    "regate": 95,
    // ... todos los campos originales
    "partidos": [...]
  },
  "datos_descriptivos": {
    "perfil_general": {
      "nombre": "Lionel Messi",
      "posicion": "Delantero Centro",
      "pie_habil": "izquierdo",
      "numero": 10,
      "equipo_pais": "Argentina",
      "titular": true
    },
    "atributos_fisicos_tecnicos": {
      "fisico": 78.5,
      "tecnico": 93.3,
      "lista_completa": {
        "precision_tiro": 94,
        "precision_pase": 91,
        // ... todos los atributos
      }
    },
    "estado_actual": {
      "rendimiento": 88,
      "forma_actual": 90,
      "moral": 85,
      "bonificaciones": ["Especialista en tiros libres", "Especialista en penales"]
    },
    "historial_temporada": {
      "goles_totales": 8,
      "asistencias": 5,
      "faltas_acumuladas": 2,
      "lesiones_total": 0
    }
  },
  "probabilidades_predictivas": {
    "exito_pases": 92.5,
    "precision_tiros": 85.3,
    "exito_regates": 88.7,
    "recuperaciones": 65.2,
    "fatiga_desgaste": 35.8,
    "faltas_cometidas": 15.2,
    "contribucion_gol": 78.9
  },
  "estadisticas_analiticas": {
    "tasa_posesion_individual": 18.5,
    "pases_clave": 12,
    "precision_bajo_presion": {
      "medio_central": 85.5,
      "defensivo": 78.2,
      "ofensivo": 92.1
    },
    "duelos_aereos_ganados": 45.3,
    "indice_creacion": 2.8,
    "eficiencia_defensiva": -1.5,
    "mapa_calor": {
      "ofensivo_central": 35.2,
      "medio_central": 42.8,
      "ofensivo_lateral_derecho": 12.5,
      "ofensivo_lateral_izquierdo": 9.5
    },
    "impacto_resultado": 45.8,
    "tendencia_forma": -5.0
  }
}
```

## Fórmulas Implementadas

### Probabilidades Predictivas

1. **Éxito Pases**: `((precision_pase + vision_juego)/200 * 100) * (pases_exitosos / total_pases)`

2. **Precisión Tiros**: `(precision_tiro/100 * 100) * ((tiros_exitosos - atajadas) / total_tiros) + bonus_area_chica(10%)`

3. **Éxito Regates**: `(regate/100 * 100) * (regates_exitosos / total_regates) + bonus_medio_central(5%)`

4. **Recuperaciones**: `((anticipacion + agresividad)/200 * 100) * ((entradas_exitosas + intercepciones_exitosas) / total)`

5. **Fatiga/Desgaste**: `100 - (resistencia/100 * 100 * e^(-minutos_jugados/90))`

6. **Faltas Cometidas**: `(agresividad/100 * 100) * (faltas / acciones_fisicas)`

7. **Contribución Gol**: `((vision_juego + fuerza_disparo)/200 * 100) * ((goles_temp + asistencias) / partidos_jugados)`

### Estadísticas Analíticas

- **Tasa Posesión Individual**: `(acciones_control_exitosas / total_acciones_equipo) * 100`
- **Pases Clave**: Conteo de pases seguidos de tiro en <30 segundos
- **Duelos Aéreos**: `(despejes_exitosos / total_despejes) * 100 * (juego_aereo/100)`
- **Índice Creación**: `(goles + asistencias + pases_clave) / (minutos_totales / 90)`
- **Eficiencia Defensiva**: `(entradas_exitosas + intercepciones_exitosas) - faltas_temp`
- **Impacto Resultado**: `Σ(importancia_peso * exito * factor)` donde importancia: crítica=2, alta=1.5, media=1, baja=0.5

## Casos Edge Manejados

1. **Sin acciones en historial**: Se usan valores base de atributos (0-100)
2. **Sin partidos jugados**: Se asume partidos_jugados = 1 para evitar división por cero
3. **Probabilidades > 100**: Se limitan a 100% máximo
4. **Valores negativos**: Se limitan a 0 mínimo donde aplique
5. **País no encontrado**: Se asigna "Desconocido"

## Uso del Endpoint

### Request
```http
GET http://127.0.0.1:8105/api/v1/jugador/68ed9d63d8343c17bb6424f2
api-key: b480eab3-5544-4a6b-ae34-b5e7e93ead60
```

### Response
Status 200 OK con JSON estructurado como se muestra arriba.

## Dependencias
- FastAPI
- Pydantic
- MongoDB (pymongo)
- Python 3.10+
- math (librería estándar)
- collections (librería estándar)

## Compatibilidad
✅ Compatible con FastAPI 0.100+
✅ Compatible con Python 3.10+
✅ No rompe compatibilidad con consumidores existentes (respuesta extendida)

## Testing Sugerido
```bash
# Probar endpoint enriquecido
curl -X GET "http://127.0.0.1:8105/api/v1/jugador/68ed9d63d8343c17bb6424f2" \
  -H "api-key: b480eab3-5544-4a6b-ae34-b5e7e93ead60"
```
