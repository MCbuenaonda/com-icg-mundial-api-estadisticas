# Endpoint de Estadísticas de Torneo

## Descripción
Este endpoint analiza y procesa datos de MongoDB para generar estadísticas completas y detalladas de torneos de fútbol.

## 📊 Estadísticas Disponibles

El endpoint retorna **13 categorías** de análisis estadístico:

1. ✅ **Información General** - Totales del torneo
2. 🔄 **Remontadas** - Equipos que remontaron 2+ goles
3. ⚽ **Goleadores** - Top scorers del torneo
4. 🌟 **Mejores Jugadores** - Por overall y rendimiento
5. 🏆 **Equipos** - Estadísticas completas de selecciones
6. 📋 **Disciplina** - Tarjetas amarillas y rojas
7. 🎪 **Partidos Destacados** - Más goles y asistencia
8. 🏟️ **Estadios** - Más partidos, goles y asistencia
9. 🏠 **Local vs Visitante** - Ventaja de jugar en casa con desglose de goles por tipo
10. 🚑 **Lesiones** - Jugadores lesionados por equipo
11. 👨‍⚖️ **Árbitros** - Más partidos, amarillas y rojas
12. 🎯 **Partidos Emocionantes** - Por índice de emoción
13. 💥 **Partidos Especiales** - Aburridos, agresivos, goleadas, último minuto

---

## Endpoint

```
GET /api/v1/torneo
```

**Headers requeridos:**
```
api_key: <tu_api_key>
```

## Respuesta

El endpoint retorna un objeto JSON con las siguientes secciones:

### 1. Información General del Torneo
```json
{
  "torneo": "Mundial",
  "total_partidos": 64,
  "total_equipos": 32,
  "total_goles": 172
}
```

### 2. Remontadas
Partidos donde un equipo remontó estando abajo por 2 o más goles:

```json
{
  "remontadas": {
    "total_remontadas": 5,
    "remontadas_2_goles": 3,
    "remontadas_3_o_mas_goles": 2,
    "equipos_con_mas_remontadas": [
      {
        "equipo": "Brasil",
        "remontadas": 2
      }
    ],
    "partidos": [
      {
        "partido_id": "...",
        "equipo_local": "Brasil",
        "equipo_visitante": "Argentina",
        "goles_local": 4,
        "goles_visitante": 3,
        "ganador": "Brasil",
        "equipo_remonto": "Brasil",
        "diferencia_maxima": 2,
        "marcador_inicial": "Perdía por 2 goles",
        "marcador_final": "4-3",
        "estadio": "Maracaná",
        "ciudad": "Río de Janeiro"
      }
    ]
  }
}
```

### 3. Goleadores
Top 10 goleadores del torneo:

```json
{
  "goleadores": {
    "total_goles_torneo": 172,
    "promedio_goles_partido": 2.69,
    "top_goleadores": [
      {
        "nombre": "Lionel Messi",
        "pais": "Argentina",
        "goles_totales": 98,
        "goles_torneo": 8,
        "partidos_jugados": 7,
        "promedio_goles": 1.14,
        "overall": 93
      }
    ],
    "goleador_maximo": { }
  }
}
```

### 4. Mejores Jugadores
Top 10 mejores jugadores basado en overall y rendimiento:

```json
{
  "mejores_jugadores": {
    "criterio_evaluacion": "Overall, goles y rendimiento en el torneo",
    "top_jugadores": [
      {
        "nombre": "Kylian Mbappé",
        "pais": "Francia",
        "overall": 91,
        "goles": 6,
        "rendimiento_promedio": 85,
        "partidos_jugados": 7,
        "forma_actual": 88,
        "atributos_destacados": {
          "precision_tiro": 87,
          "velocidad": 97,
          "fuerza_disparo": 88,
          "regate": 92,
          "vision_juego": 80
        }
      }
    ],
    "mejor_jugador_general": { }
  }
}
```

### 5. Estadísticas de Equipos
Rendimiento de todos los equipos participantes:

```json
{
  "equipos": {
    "total_equipos": 32,
    "equipo_mas_goleador": {
      "equipo": "Francia",
      "partidos_jugados": 7,
      "victorias": 6,
      "empates": 0,
      "derrotas": 1,
      "goles_favor": 18,
      "goles_contra": 8,
      "diferencia_goles": 10,
      "porcentaje_victorias": 85.71,
      "racha_actual": "N/A"
    },
    "mejor_defensa": { },
    "equipo_mas_victorias": { },
    "equipos": [ ]
  }
}
```

### 6. Disciplina
Tarjetas amarillas y rojas:

```json
{
  "disciplina": {
    "total_tarjetas_amarillas": 187,
    "total_tarjetas_rojas": 4,
    "promedio_amarillas_partido": 2.92,
    "promedio_rojas_partido": 0.06,
    "equipo_mas_indisciplinado": {
      "equipo": "Uruguay",
      "amarillas": 15,
      "rojas": 1
    },
    "jugador_mas_amonestado": {
      "jugador": "Sergio Ramos",
      "equipo": "España",
      "amarillas": 3,
      "rojas": 0
    }
  }
}
```

### 7. Partidos Destacados
Partidos más memorables del torneo:

```json
{
  "partidos_destacados": {
    "total_partidos": 64,
    "promedio_goles_partido": 2.69,
    "partido_mas_goles": {
      "partido_id": "...",
      "equipo_local": "Portugal",
      "equipo_visitante": "España",
      "goles_local": 3,
      "goles_visitante": 3,
      "total_goles": 6,
      "categoria": "más goles",
      "descripcion": "Partido con 6 goles",
      "estadio": "Fisht Stadium",
      "ciudad": "Sochi"
    },
    "partido_mas_asistencia": { },
    "partidos_destacados": [ ]
  }
}
```

### 8. Metadata
```json
{
  "fecha_generacion": "2025-12-13T10:30:00.123456",
  "mensaje": "Estadísticas del torneo generadas exitosamente"
}
```

---

## NUEVAS SECCIONES

### 9. Estadios
Estadísticas de los estadios que albergaron partidos:

```json
{
  "estadios": {
    "total_estadios": 12,
    "estadio_mas_partidos": {
      "estadio": "Estadio Azteca",
      "ciudad": "Ciudad de México",
      "partidos_jugados": 8,
      "total_goles": 22,
      "promedio_goles": 2.75,
      "asistencia_total": 520000,
      "asistencia_promedio": 65000
    },
    "estadio_mas_goleador": {
      "estadio": "Maracaná",
      "ciudad": "Río de Janeiro",
      "partidos_jugados": 7,
      "total_goles": 28,
      "promedio_goles": 4.0,
      "asistencia_total": 450000,
      "asistencia_promedio": 64285
    },
    "estadio_mayor_asistencia": { },
    "estadios": [ ]
  }
}
```

### 10. Local vs Visitante
Análisis de ventaja local con desglose de goles por tipo de jugada:

```json
{
  "local_visitante": {
    "total_partidos": 64,
    "victorias_local": 32,
    "victorias_visitante": 20,
    "empates": 12,
    "porcentaje_local": 50.0,
    "porcentaje_visitante": 31.25,
    "porcentaje_empate": 18.75,
    "goles_local_total": 95,
    "goles_visitante_total": 77,
    "promedio_goles_local": 1.48,
    "promedio_goles_visitante": 1.20,
    "goles_local_detalle": {
      "goles_penal": 12,
      "goles_corner": 18,
      "goles_jugada_normal": 65,
      "porcentaje_penal": 12.63,
      "porcentaje_corner": 18.95,
      "porcentaje_jugada_normal": 68.42
    },
    "goles_visitante_detalle": {
      "goles_penal": 8,
      "goles_corner": 14,
      "goles_jugada_normal": 55,
      "porcentaje_penal": 10.39,
      "porcentaje_corner": 18.18,
      "porcentaje_jugada_normal": 71.43
    }
  }
}
```

### 11. Lesiones
Estadísticas de jugadores lesionados:

```json
{
  "lesiones": {
    "total_lesiones": 15,
    "promedio_lesiones_partido": 0.23,
    "equipo_mas_lesiones": {
      "equipo": "Brasil",
      "lesiones": 4
    },
    "jugadores_lesionados": [
      {
        "jugador": "Neymar Jr",
        "equipo": "Brasil",
        "partido_id": "...",
        "minuto": 67,
        "rival": "Argentina"
      }
    ]
  }
}
```

### 12. Árbitros
Estadísticas de arbitraje:

```json
{
  "arbitros": {
    "total_arbitros_principal": 20,
    "total_arbitros_linea": 15,
    "arbitro_mas_partidos": {
      "id": "68bb9703033a4535ed96cd19",
      "nombre": "Néstor Pitana",
      "pais": "Argentina",
      "puesto": "Árbitro Principal",
      "partidos_arbitrados": 5,
      "amarillas_mostradas": 18,
      "rojas_mostradas": 1,
      "promedio_amarillas": 3.6,
      "promedio_rojas": 0.2
    },
    "arbitro_mas_amarillas": {
      "id": "68bb9703033a4535ed96cd1a",
      "nombre": "Felix Brych",
      "pais": "Alemania",
      "puesto": "Árbitro Principal",
      "partidos_arbitrados": 4,
      "amarillas_mostradas": 22,
      "rojas_mostradas": 2,
      "promedio_amarillas": 5.5,
      "promedio_rojas": 0.5
    },
    "arbitro_mas_rojas": { },
    "arbitros_principales": [ ],
    "estadisticas_arbitros_linea": {
      "total_arbitros_linea": 15,
      "arbitros_linea_1": [
        {
          "id": "68bb9703033a4535ed96cd1b",
          "nombre": "Juan Carlos Torres",
          "pais": "México",
          "puesto": "Árbitro de Línea 1",
          "partidos_arbitrados": 6
        }
      ],
      "arbitros_linea_2": [ ],
      "cuarto_arbitro": [ ]
    }
  }
}
```

### 13. Partidos Especiales
Análisis de partidos con características únicas:

```json
{
  "partidos_especiales": {
    "partidos_emocionantes": [
      {
        "partido_id": "...",
        "equipo_local": "Francia",
        "equipo_visitante": "Argentina",
        "marcador": "4-3",
        "acciones_criticas": 25,
        "acciones_altas": 40,
        "total_acciones": 380,
        "indice_emocion": 135.0,
        "estadio": "Lusail Stadium"
      }
    ],
    "partidos_aburridos": [
      {
        "partido_id": "...",
        "equipo_local": "Dinamarca",
        "equipo_visitante": "Túnez",
        "marcador": "0-0",
        "total_acciones": 180,
        "total_goles": 0,
        "indice_aburrimiento": 64.0,
        "estadio": "Education City Stadium"
      }
    ],
    "partidos_agresivos": [
      {
        "partido_id": "...",
        "equipo_local": "Uruguay",
        "equipo_visitante": "Portugal",
        "marcador": "2-0",
        "total_faltas": 28,
        "tarjetas_amarillas": 8,
        "tarjetas_rojas": 1,
        "indice_agresividad": 49,
        "estadio": "Lusail Stadium"
      }
    ],
    "goles_ultimo_minuto": [
      {
        "partido_id": "...",
        "equipo_local": "Alemania",
        "equipo_visitante": "Suecia",
        "equipo_ganador": "Alemania",
        "marcador_final": "2-1",
        "marcador_antes_gol": "1-1",
        "minuto_gol_decisivo": 90,
        "jugador": "Toni Kroos",
        "descripcion": "Toni Kroos marcó en el minuto 90 para Alemania (el partido iba 1-1)"
      }
    ],
    "goleadas": [
      {
        "partido_id": "...",
        "equipo_ganador": "España",
        "equipo_perdedor": "Costa Rica",
        "marcador": "7-0",
        "diferencia_goles": 7,
        "categoria_humillacion": "Humillación épica",
        "estadio": "Al Thumama Stadium"
      },
      {
        "partido_id": "...",
        "equipo_ganador": "Portugal",
        "equipo_perdedor": "Suiza",
        "marcador": "6-1",
        "diferencia_goles": 5,
        "categoria_humillacion": "Humillación épica",
        "estadio": "Lusail Stadium"
      }
    ],
    "partido_menor_asistencia": {
      "partido_id": "...",
      "equipo_local": "Canadá",
      "equipo_visitante": "Marruecos",
      "marcador": "1-2",
      "asistencia": 35000,
      "estadio": "Al Thumama Stadium"
    },
    "partido_mayor_asistencia": {
      "partido_id": "...",
      "equipo_local": "Argentina",
      "equipo_visitante": "Francia",
      "marcador": "3-3",
      "asistencia": 88966,
      "estadio": "Lusail Stadium"
    }
  }
}
```

---

## Colecciones MongoDB Utilizadas

El endpoint consulta las siguientes colecciones:

1. **historial**: Contiene el historial de partidos con acciones minuto a minuto
2. **jugadores**: Información de jugadores con atributos técnicos y físicos
3. **paises**: Datos de selecciones nacionales
4. **ciudades**: Información de ubicaciones (usado indirectamente)

## Análisis Realizados

### 1. Análisis de Remontadas
- Simula el marcador minuto a minuto
- Detecta cuando un equipo estaba perdiendo por 2+ goles
- Verifica si terminó ganando el partido

### 2. Análisis de Goleadores
- Cuenta goles por jugador en el torneo
- Calcula promedio de goles
- Enriquece con datos de la colección jugadores

### 3. Análisis de Mejores Jugadores
- Evalúa participación en partidos
- Considera overall, goles y acciones críticas
- Muestra atributos destacados

### 4. Análisis de Equipos
- Calcula victorias, empates, derrotas
- Goles a favor y en contra
- Diferencia de goles y porcentaje de victorias

### 5. Análisis de Disciplina
- Contabiliza tarjetas amarillas y rojas
- Identifica equipos y jugadores más indisciplinados
- Calcula promedios por partido

### 6. Análisis de Partidos Destacados
- Identifica partidos con más goles
- Partidos con mayor asistencia
- Top 5 partidos más espectaculares

### 7. Análisis de Estadios (NUEVO)
- Estadio con más partidos albergados
- Estadio más goleador
- Estadio con mayor asistencia total
- Top 10 estadios por partidos jugados

### 8. Análisis Local vs Visitante (NUEVO)
- Victorias locales, visitantes y empates
- Porcentajes de cada resultado
- Promedios de goles local y visitante

### 9. Análisis de Lesiones (NUEVO)
- Total de lesiones en el torneo
- Promedio de lesiones por partido
- Equipo con más lesiones
- Lista de jugadores lesionados

### 10. Análisis de Árbitros (NUEVO)
- Árbitro con más partidos pitados
- Árbitro con más amarillas mostradas
- Árbitro con más rojas mostradas
- Estadísticas de árbitros principales
- **Usa la colección real de árbitros de MongoDB**
- Soporte para Árbitro de Línea 1, Línea 2 y 4to Árbitro

### 11. Análisis de Partidos Especiales (NUEVO)
- **Partidos Emocionantes**: Alto índice de acciones críticas
- **Partidos Aburridos**: Pocas acciones y goles
- **Partidos Agresivos**: Muchas faltas y tarjetas
- **Goles Último Minuto**: Goles decisivos en minuto 85+ **cuando el partido iba empatado**
- **Goleadas**: Partidos con diferencia de 3+ goles (humillaciones)
- **Menor/Mayor Asistencia**: Partidos con extremos de público


## Ejemplo de Uso

### Con cURL
```bash
curl -X GET "http://localhost:8105/api/v1/torneo" \
  -H "api_key: your_api_key_here"
```

### Con Python (requests)
```python
import requests

url = "http://localhost:8105/api/v1/torneo"
headers = {"api_key": "your_api_key_here"}

response = requests.get(url, headers=headers)
estadisticas = response.json()

print(f"Total de partidos: {estadisticas['total_partidos']}")
print(f"Goleador máximo: {estadisticas['goleadores']['goleador_maximo']['nombre']}")
print(f"Total remontadas: {estadisticas['remontadas']['total_remontadas']}")
```

### Con JavaScript (fetch)
```javascript
fetch('http://localhost:8105/api/v1/torneo', {
  headers: {
    'api_key': 'your_api_key_here'
  }
})
.then(response => response.json())
.then(data => {
  console.log('Total partidos:', data.total_partidos);
  console.log('Goleador:', data.goleadores.goleador_maximo.nombre);
  console.log('Remontadas:', data.remontadas.total_remontadas);
});
```

## Notas de Rendimiento

- El endpoint procesa todas las colecciones en cada llamada
- Para torneos grandes (100+ partidos), el tiempo de respuesta puede ser de 2-5 segundos
- Se recomienda implementar caché para consultas frecuentes
- Los ObjectIds de MongoDB se convierten automáticamente a strings

## Posibles Mejoras Futuras

1. **Filtros opcionales**: 
   - Filtrar por fase del torneo, grupo, fecha
   - Filtrar por equipo específico
   - Rango de fechas

2. **Caché**: 
   - Implementar Redis para mejorar rendimiento
   - Invalidación inteligente de caché

3. **Paginación**: 
   - Para listas muy largas de jugadores/equipos
   - Límites configurables

4. **Más estadísticas**: 
   - Asistencias por jugador (pases que terminan en gol)
   - Efectividad de tiros (goles/tiros totales)
   - Posesión de balón promedio por equipo
   - Análisis de táctica (formaciones más efectivas)
   - Jugadores más valiosos (MVP)
   - Racha de victorias/derrotas
   - Heat maps de acciones
   - xG (Expected Goals) por partido

5. **Exportación**: 
   - Generar PDF con las estadísticas
   - Exportar a Excel/CSV
   - Generar infografías

6. **Datos de árbitros reales**:
   - Actualmente se simulan los árbitros
   - Agregar campo de árbitro en el historial
   - Incluir árbitros de línea y 4to árbitro

7. **Machine Learning**:
   - Predicción de resultados
   - Análisis de patrones de juego
   - Detección de anomalías

8. **Comparativas**:
   - Comparar torneos diferentes
   - Evolución de equipos entre torneos
   - Head-to-head entre equipos

## 🔧 Notas Técnicas

### Datos Simulados
- **Árbitros**: Actualmente se simulan basándose en el índice del partido. En producción, deberías agregar un campo `arbitro` en la colección `historial`.

### Índices de Análisis

**Índice de Emoción** = `(acciones_críticas × 3) + (acciones_altas × 1.5)`
- Umbral para partido emocionante: > 50

**Índice de Aburrimiento** = `100 - (total_acciones × 0.2 + total_goles × 10)`
- Partidos con < 200 acciones y ≤ 1 gol

**Índice de Agresividad** = `faltas + (amarillas × 2) + (rojas × 5)`
- Umbral para partido agresivo: > 20

**Categorías de Humillación**:
- 3 goles: "Goleada contundente"
- 4 goles: "Goleada histórica"
- 5+ goles: "Humillación épica"

---

## 📝 Changelog

### Versión 2.1 (2025-12-13)
- ✅ Agregado desglose de goles por tipo en local_visitante (penal, corner, jugada normal)
- ✅ Implementado análisis de acciones previas para clasificar goles
- ✅ Agregados porcentajes de goles por tipo de jugada

### Versión 2.0 (2025-12-13)
- ✅ Agregado análisis de estadios
- ✅ Agregado análisis local vs visitante
- ✅ Agregado análisis de lesiones
- ✅ Agregado análisis de árbitros con catálogo real
- ✅ Agregado análisis de partidos emocionantes
- ✅ Agregado análisis de partidos aburridos
- ✅ Agregado análisis de partidos agresivos
- ✅ Agregado análisis de goles último minuto (solo partidos empatados)
- ✅ Agregado análisis de goleadas (humillaciones)
- ✅ Agregado análisis de asistencia mínima/máxima

### Versión 1.0 (2025-12-13)
- 🎉 Lanzamiento inicial con 6 categorías de análisis

