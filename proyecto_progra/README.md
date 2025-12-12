# Procesador de Datos Interactivo

Sistema modular de procesamiento y análisis de datos desarrollado con **Python Standard Library**.

## 📋 Descripción

Este proyecto implementa un sistema completo de análisis de datos que permite:
- ✅ Cargar datos desde archivos CSV
- ✅ Limpiar y validar datos (duplicados, nulos, normalización)
- ✅ Transformar y filtrar datasets
- ✅ Realizar análisis estadísticos avanzados
- ✅ Generar análisis específicos de ventas
- ✅ Exportar reportes en múltiples formatos (TXT, JSON, XML)

## 🏗️ Arquitectura

El proyecto sigue una **arquitectura en capas** con separación clara de responsabilidades:

```
proyecto_progra/
├── data/                       # Datasets y archivos exportados
│   └── ventas.csv             # Dataset de ejemplo
├── src/                        # Código fuente
│   ├── main.py                # Punto de entrada principal
│   ├── modelos/               # Capa de Modelos de Datos
│   │   ├── registro.py        # Clase Registro
│   │   └── dataset.py         # Clase Dataset
│   ├── cargadores/            # Capa de Carga de Datos
│   │   ├── cargador_base.py   # Clase abstracta base
│   │   └── cargador_csv.py    # Cargador CSV
│   ├── procesadores/          # Capa de Procesamiento
│   │   ├── limpiador.py       # Limpieza de datos
│   │   └── transformador.py   # Transformaciones
│   ├── analizadores/          # Capa de Análisis
│   │   ├── analizador_base.py          # Clase abstracta base
│   │   ├── analizador_estadistico.py   # Análisis estadístico
│   │   └── analizador_ventas.py        # Análisis de ventas
│   ├── reportes/              # Capa de Reportes
│   │   ├── generador_base.py         # Clase abstracta base
│   │   ├── generador_consola.py      # Reportes en consola
│   │   └── generador_archivo.py      # Reportes en archivo
│   ├── persistencia/          # Capa de Persistencia (BD Local)
│   │   └── registro_operaciones.py   # Registro de operaciones
│   └── utilidades/            # Utilidades Compartidas
│       ├── validadores.py     # Validación de datos
│       └── formateadores.py   # Formateo de salida
├── operaciones.dat            # Base de datos local (generada automáticamente)
└── README.md
```

## 🎯 Principios de POO Aplicados

### 1. **Encapsulación**
- Cada clase maneja su propia lógica interna
- Los atributos son privados (prefijo `_`)
- Se accede mediante métodos públicos

### 2. **Abstracción**
- Clases base abstractas: `CargadorBase`, `AnalizadorBase`, `GeneradorReporteBase`
- Definen contratos que las subclases deben cumplir
- Uso del módulo `abc` (Abstract Base Classes)

### 3. **Herencia**
- Jerarquías claras de especialización
- Ejemplo: `CargadorCSV` hereda de `CargadorBase`
- Ejemplo: `AnalizadorEstadistico` hereda de `AnalizadorBase`

### 4. **Polimorfismo**
- Intercambiabilidad de implementaciones
- Diferentes analizadores comparten la misma interfaz
- Diferentes generadores de reportes usan el mismo método `generar()`

## 💾 Base de Datos Local (operaciones.dat)

El sistema incluye un **registro automático de todas las operaciones** realizadas:

### Información Registrada
- ✅ **Dataset utilizado**: Nombre del archivo de datos
- ✅ **Operación realizada**: Tipo de acción ejecutada
- ✅ **Parámetros**: Valores y configuración usados
- ✅ **Timestamp**: Fecha y hora de cada operación
- ✅ **Resultado**: Estado de la operación

### Operaciones Registradas
- Cargar dataset
- Ver resumen de datos
- Limpieza de datos (completa, duplicados, vacíos, nulos)
- Filtros (por campo, por rango)
- Ordenamiento
- Análisis estadístico
- Análisis de ventas
- Generación de reportes
- Exportación de datos

### Funcionalidades del Historial
1. **Ver todas las operaciones**: Historial completo
2. **Ver últimas 10 operaciones**: Resumen reciente
3. **Estadísticas del historial**: Métricas de uso
4. **Exportar historial**: Guardar en archivo de texto
5. **Limpiar historial**: Borrar todas las operaciones

### Persistencia
- Archivo: `operaciones.dat` (raíz del proyecto)
- Formato: Serialización con `pickle` (Python Standard Library)
- Persistencia automática: Se guarda después de cada operación

## 🚀 Cómo Ejecutar

### Requisitos
- Python 3.7 o superior
- **No se requieren paquetes externos** (solo Python Standard Library)

### Ejecución

1. **Navegar al directorio del proyecto:**
   ```bash
   cd proyecto_progra
   ```

2. **Ejecutar la aplicación:**
   ```bash
   python src/main.py
   ```

3. **Seguir el menú interactivo:**
   - Seleccionar opciones ingresando el número correspondiente
   - El sistema guiará paso a paso

## 📊 Dataset de Ejemplo

El proyecto incluye un dataset de ventas en `data/ventas.csv` con **400 registros** que contienen:
- **id_venta**: Identificador único
- **fecha**: Fecha de la venta (2024, primeros 6 meses)
- **producto**: Nombre del producto (49 productos diferentes)
- **categoria**: Categoría del producto (11 categorías)
- **cantidad**: Unidades vendidas
- **precio_unitario**: Precio por unidad
- **total**: Total de la venta
- **region**: Región de venta (5 regiones)
- **vendedor**: Nombre del vendedor (10 vendedores)

**Estadísticas del dataset:**
- 400 registros de ventas
- 11 categorías de productos
- 49 productos únicos
- 5 regiones diferentes
- 10 vendedores
- Rango de fechas: Enero - Junio 2024

## 🔧 Funcionalidades Principales

### 1. Cargar Dataset
- Selección de archivos CSV desde `/data`
- Validación automática de estructura
- Conversión a objetos Python

### 2. Limpieza de Datos
- ✅ Eliminación de duplicados
- ✅ Eliminación de registros vacíos
- ✅ Manejo de valores nulos
- ✅ Normalización de texto
- ✅ Reporte de calidad de datos

### 3. Transformaciones
- Filtrado por campo específico
- Filtrado por rango numérico
- Ordenamiento ascendente/descendente
- Agrupación y totales
- Selección de primeros N registros

### 4. Análisis Estadístico
- Media, mediana, moda
- Desviación estándar y varianza
- Valores mínimos y máximos
- Distribución de frecuencias
- Análisis por tipo de dato (numérico/categórico)

### 5. Análisis de Ventas
- Ventas totales
- Ventas por región
- Ventas por producto
- Ventas por categoría
- Top 5 productos
- Top 5 vendedores

### 6. Generación de Reportes
- **Consola**: Visualización formateada en terminal
- **TXT**: Archivo de texto estructurado
- **JSON**: Formato JSON para integración
- **XML**: Formato XML estructurado

### 7. Historial de Operaciones 🆕
- **Ver operaciones realizadas**: Todas o últimas 10
- **Estadísticas de uso**: Resumen de actividad
- **Exportar historial**: Guardar en archivo de texto
- **Limpiar historial**: Borrar registro de operaciones

> **Nota importante:** Todos los archivos JSON y XML se guardan automáticamente en la carpeta `/data`

## 📝 Ejemplo de Uso

```
1. Seleccionar opción "1. Cargar Dataset"
2. Elegir "ventas.csv"
3. Seleccionar opción "3. Limpiar Datos"
4. Elegir "1. Limpieza completa"
5. Seleccionar opción "6. Análisis de Ventas"
6. Ver resultados en consola
7. Seleccionar opción "7. Generar Reportes"
8. Elegir "2. Reporte de Ventas"
9. Seleccionar "3. Archivo JSON"
10. El reporte se guardará en /data
```

## 💾 Exportación de Datos

Los reportes y datos exportados se almacenan en:
- **Ubicación:** `proyecto_progra/data/`
- **Formatos disponibles:** TXT, JSON, XML
- **Nombres:** Se pueden personalizar o usar timestamp automático

## 🔍 Validaciones Implementadas

- ✅ Validación de datasets vacíos
- ✅ Validación de tipos numéricos
- ✅ Validación de rangos
- ✅ Validación de opciones de menú
- ✅ Manejo de errores de lectura de archivos
- ✅ Manejo de codificaciones (UTF-8, Latin-1)

## 🎨 Características Destacadas

### Formateo Profesional
- Separadores visuales
- Barras de progreso
- Formateo de moneda
- Tablas alineadas
- Mensajes con emojis

### Robustez
- Manejo de excepciones
- Validación de entrada de usuario
- Mensajes de error descriptivos
- Recuperación ante fallos

### Modularidad
- Código organizado en módulos
- Responsabilidad única por clase
- Fácil de extender y mantener
- Documentación completa

## 📚 Módulos de Python Standard Library Utilizados

- `csv`: Lectura de archivos CSV
- `json`: Exportación JSON
- `pathlib`: Manejo de rutas
- `datetime`: Fechas y timestamps
- `statistics`: Cálculos estadísticos
- `abc`: Clases abstractas
- `collections`: Estructuras de datos (defaultdict)
- `os`, `sys`: Operaciones del sistema

## 👨‍💻 Estructura de Clases Principales

### Modelos
- **Registro**: Representa una fila de datos
- **Dataset**: Contenedor de registros

### Cargadores
- **CargadorBase** (abstracta): Interfaz para cargadores
- **CargadorCSV**: Implementación para CSV

### Procesadores
- **Limpiador**: Limpieza de datos
- **Transformador**: Filtrado y transformaciones

### Analizadores
- **AnalizadorBase** (abstracta): Interfaz para análisis
- **AnalizadorEstadistico**: Estadísticas generales
- **AnalizadorVentas**: Análisis de negocio

### Generadores de Reportes
- **GeneradorReporteBase** (abstracta): Interfaz para reportes
- **GeneradorReporteConsola**: Salida en consola
- **GeneradorReporteArchivo**: Exportación a archivos

## 🔄 Flujo de Ejecución

```
Inicio
  ↓
Cargar Dataset desde CSV
  ↓
Crear objetos Registro y Dataset
  ↓
Aplicar Limpieza (opcional)
  ↓
Aplicar Transformaciones (opcional)
  ↓
Ejecutar Análisis
  ↓
Generar Reportes
  ↓
Exportar Resultados (opcional)
  ↓
Fin
```

## 📖 Documentación del Código

Todos los archivos incluyen:
- ✅ Docstrings en español
- ✅ Comentarios explicativos
- ✅ Descripción de parámetros y retornos
- ✅ Ejemplos de uso cuando es relevante

## 🎓 Conceptos Demostrados

Este proyecto demuestra:
1. **Diseño orientado a objetos** con jerarquías claras
2. **Arquitectura en capas** con separación de responsabilidades
3. **Patrones de diseño**: Abstract Factory, Template Method, Strategy
4. **Principios SOLID** aplicados
5. **Manejo profesional de archivos** y datos
6. **Validación y limpieza de datos** robusta
7. **Análisis estadístico** con Python nativo
8. **Interacción con usuario** mediante consola
9. **Exportación multi-formato** (TXT, JSON, XML)

## 📄 Licencia

Proyecto Final - Programación Orientada a Objetos

---

**Desarrollado con:** Python Standard Library  
**Versión:** 1.0.0  
**Autor:** Proyecto Final  
