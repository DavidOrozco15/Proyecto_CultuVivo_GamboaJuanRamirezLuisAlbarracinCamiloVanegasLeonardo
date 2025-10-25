
# Análisis de Validaciones en el Programa CultuVivo

He revisado exhaustivamente todo el código del programa actualizado, incluyendo los archivos principales (`main.py`, `messages.py`, `administracion.py`, `artistas.py`, `asistentes.py`, `modules/utils.py`) y los datos JSON. El programa es una aplicación de consola para gestión de eventos culturales, con roles de administrador y asistente. A continuación, identifico los errores de validación que aún persisten en el programa, basándome en el comportamiento esperado (validar en tiempo real y repetir hasta que el input sea correcto, en lugar de permitir continuar y fallar al final). Me enfoco en errores que no cumplen su rol adecuadamente.

## Errores Persistentes en Validaciones

### 1. Errores en `crear_evento()` (administracion.py)
- **Capacidad en eventos.json inconsistente**: En `eventos.json`, algunos eventos tienen `"capacidad": "200"` (string) y otros `"capacidad": 400` (int). `validar_evento()` espera int, pero no valida consistencia en carga/guardado. Puede causar errores al modificar eventos con capacidad string.
- **ID de evento no único si se eliminan eventos**: Los IDs se generan como `len(cargar_eventos()) + 1`, lo que puede duplicar IDs si se eliminan eventos intermedios (ej. eliminar ID 2, crear nuevo: ID 3, pero si había 4 eventos, el nuevo debería ser 5).

### 2. Errores en `modificar_evento()` (administracion.py)
- **Lugar no valida en loop**: Para `lugar`, pide input pero no valida que no esté vacío si se proporciona nuevo valor. Si se ingresa vacío, mantiene anterior, pero no repite si se quiere cambiar a vacío.
- **Artista: loop infinito potencial**: Si el artista no está disponible, pregunta "¿Desea elegir otro artista?", pero si responde "s", continúa el loop interno sin resetear. Si siempre elige no disponible, puede loopear indefinidamente.
- **Validación de duplicados solo si cambia nombre o fecha**: Pero no valida si cambia hora o lugar, permitiendo duplicados en misma fecha pero hora diferente.

### 3. Errores en `registrar_artista()` (artistas.py)
- **Nombre en artistas.json inconsistente**: En `artistas.json`, `"nombre": "Diplo"` (capitalizado) vs `"nombre": "corso"` (minúscula). No valida consistencia de capitalización.
- **Tipo presentación inconsistente**: `"tipo_presentacion": "Concierto"` vs `"danza"` (minúscula). No valida formato consistente.

### 4. Errores en `registrar_asistente()` (asistentes.py)
- **Archivo asistentes.json corrupto**: El archivo `data/asistentes.json` contiene caracteres extraños (`{}`), lo que indica corrupción. `cargar_asistentes()` maneja JSONDecodeError retornando {}, pero no valida integridad del archivo ni repara automáticamente.

### 5. Errores en Login y Menús (messages.py)
- **Login admin sin contraseña**: Solo valida `usuario == "admin"`, sin contraseña. Permite acceso sin autenticación real.
- **Login asistente sin validar formato ID**: No valida que ID sea numérico o alfanumérico; solo verifica existencia en JSON.
- **Menú asistente opción 1 no implementada**: Imprime "Funcion aun no disponible..." sin validación alguna.

### 6. Errores en `modules/utils.py`
- **validar_existencia() inconsistente**: En `administracion.py`, se usa para validar duplicados por nombre (ignorando fecha), pero en `utils.py` valida por nombre y fecha. Inconsistencia entre funciones.
- **pedir_nombre_n() valida solo letras**: Usa `nombre.replace(" ", "").isalpha()`, que permite números y símbolos si hay espacios, pero falla si hay acentos o caracteres especiales (ej. "café" falla).
- **validar_disponibilidad_artista() recursiva**: Importa `cargar_eventos` dentro de la función, causando dependencia circular potencial si se llama desde `administracion.py`.
- **Capacidad en eventos mixta**: `pedir_capacidad()` retorna int, pero `eventos.json` tiene strings. No normaliza al guardar.

### 7. Errores en Datos JSON
- **eventos.json capacidad inconsistente**: Mezcla strings e ints, causando TypeError en validaciones que esperan int.
- **artistas.json formato inconsistente**: Nombres y tipos sin capitalización uniforme.
- **asistentes.json corrupto**: Contiene BOM o caracteres inválidos, impidiendo carga correcta.

### 8. Errores en Manejo de Errores General
- **No valida existencia de directorio data**: Si `data/` no existe, funciones fallan sin crear automáticamente.
- **Errores de JSON no reparan archivos**: Solo retornan vacíos, pero no limpian archivos corruptos.
- **IDs no regeneran tras eliminaciones**: Eventos eliminados dejan huecos en IDs, potencialmente causando confusiones.

### 9. Errores en `generar_reporte()` (administracion.py)
- **No valida si eventos tienen datos consistentes**: Imprime campos asumiendo existen, pero si JSON corrupto, puede fallar con KeyError.

### 10. Errores en `eliminar_evento()` (administracion.py)
- **No valida si ID existe antes de confirmar eliminación**: Solo filtra lista, pero no avisa si ID no encontrado hasta después de intentar guardar.


