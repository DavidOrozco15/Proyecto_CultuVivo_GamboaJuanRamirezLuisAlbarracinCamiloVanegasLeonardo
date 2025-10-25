
# LUIS

## 1. Validaciones en `crear_evento()` (administracion.py)
- **Problema principal (como mencionas)**: Los inputs se solicitan secuencialmente sin validación inmediata. Si se ingresa una fecha inválida (ej. "2023-13-45"), el programa continúa pidiendo los demás campos (hora, lugar, etc.) y solo valida al final con `validar_evento()`. Si falla, imprime el error y retorna sin guardar ni repetir el proceso. Esto permite "llenar el formulario" con datos inválidos y falla tarde.
- **Otras validaciones deficientes**:
  - No valida que `capacidad` sea un entero positivo inmediatamente; solo al final.
  - No valida que `categoria` no esté vacía inmediatamente.
  - No valida que el ID de artista exista inmediatamente (solo asigna None si no).
  - Si `validar_evento()` falla, no repite el input; simplemente sale de la función.
- **Mejora necesaria**: Implementar loops para cada input, validando en tiempo real y repitiendo hasta que sea correcto. Por ejemplo, para fecha: pedir hasta que `datetime.strptime(fecha, "%Y-%m-%d")` no lance ValueError.

## 2. Validaciones en `modificar_evento()` (administracion.py)
- **Problema**: Similar a `crear_evento()`. Pide todos los nuevos valores (dejando vacío para no cambiar), pero valida solo al final con `validar_evento()`. Si falla (ej. fecha inválida), imprime error y retorna sin actualizar ni repetir.
- **Otras validaciones deficientes**:
  - No valida inmediatamente si el ID del evento es un entero válido (usa try/except, pero no repite si falla).
  - Para artista, valida existencia solo si se ingresa un ID, pero no repite si es inválido.
- **Mejora necesaria**: Validar cada campo modificado en loops, repitiendo hasta que sea válido. Si se deja vacío, usar el valor anterior sin validación adicional (asumiendo que ya era válido).

# CAMILO

## 3. Validaciones en `registrar_artista()` (artistas.py)
- **Problema**: Solicita todos los inputs (`nRegistro`, `nombre`, etc.) y valida al final. Si hay errores (ej. nombre con números, duración no numérica), imprime la lista de errores y retorna sin guardar ni repetir. No permite corregir inputs específicos.
- **Validaciones existentes pero insuficientes**:
  - `validar_registro()`: Solo verifica dígitos, pero no repite.
  - `validar_nombre()`: Usa regex para letras/espacios, pero no se aplica en loop.
  - `validar_tipo()` y `validar_duracion()`: Básicas, pero fallan tarde.
- **Mejora necesaria**: Validar cada campo en un loop individual, repitiendo hasta que pase la validación. Por ejemplo, para nombre: pedir hasta que `validar_nombre()` retorne True.

## 4. Validaciones en `registrar_asistente()` (asistentes.py)
- **Problema parcial**: Para `correo`, ya hay un loop que repite hasta que `validar_correo()` pase. Esto es bueno. Pero para otros campos (`identificacion`, `nombre`, `tipo_boleto`):
  - No valida inmediatamente; solo verifica al final si están vacíos o si `identificacion` ya existe.
  - Si falla (ej. campos vacíos), imprime error y retorna sin repetir.
  - `tipo_boleto` no valida formato (debe ser "General", "Vip", "Cortesia"); solo capitaliza.
- **Mejora necesaria**: Agregar loops para `identificacion` (validar único y no vacío), `nombre` (validar letras/espacios, similar a artistas), y `tipo_boleto` (validar que sea uno de los permitidos).


