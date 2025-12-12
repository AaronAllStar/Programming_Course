"""
Procesador de Datos Interactivo
Archivo Principal - main.py

Sistema modular de procesamiento y análisis de datos usando Python Standard Library.
Implementa arquitectura en capas con principios de POO.

Aaron Medrano
Versión: 1.0.0
"""

import sys
import os
from pathlib import Path

# Agregar el directorio raíz al path para importaciones
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importaciones de módulos del proyecto
from src.modelos.dataset import Dataset
from src.cargadores.cargador_csv import CargadorCSV
from src.procesadores.limpiador import Limpiador
from src.procesadores.transformador import Transformador
from src.analizadores.analizador_estadistico import AnalizadorEstadistico
from src.analizadores.analizador_ventas import AnalizadorVentas
from src.reportes.generador_consola import GeneradorReporteConsola
from src.reportes.generador_archivo import GeneradorReporteArchivo
from src.utilidades.validadores import Validador
from src.utilidades.formateadores import Formateador
from src.persistencia.registro_operaciones import RegistroOperaciones


class AplicacionProcesadorDatos:
    """
    Clase principal de la aplicación.
    
    Coordina todas las funcionalidades del sistema y gestiona
    la interacción con el usuario a través de un menú.
    
    Atributos:
        dataset (Dataset): Dataset cargado en memoria
        dataset_original (Dataset): Copia del dataset original para restaurar
        limpiador (Limpiador): Procesador de limpieza de datos
        transformador (Transformador): Procesador de transformación de datos
        registro_bd (RegistroOperaciones): Gestor de base de datos de operaciones
    """
    
    def __init__(self):
        """
        Inicializa la aplicación.
        """
        self.dataset = None
        self.dataset_original = None
        self.limpiador = None
        self.transformador = None
        self.ruta_data = Path(__file__).parent.parent / "data"
        # Inicializar registro de operaciones (BD local)
        self.registro_bd = RegistroOperaciones()
        
    def ejecutar(self):
        """
        Punto de entrada principal de la aplicación.
        Muestra el menú y gestiona la navegación.
        """
        self._mostrar_bienvenida()
        
        # Bucle principal del programa
        while True:
            self._mostrar_menu_principal()
            opcion = input("\nSeleccione una opción: ").strip()
            
            if opcion == "1":
                self._cargar_dataset()
            elif opcion == "2":
                self._ver_resumen_datos()
            elif opcion == "3":
                self._limpiar_datos()
            elif opcion == "4":
                self._aplicar_filtros()
            elif opcion == "5":
                self._analizar_estadisticas()
            elif opcion == "6":
                self._analizar_ventas()
            elif opcion == "7":
                self._generar_reportes()
            elif opcion == "8":
                self._exportar_datos()
            elif opcion == "9":
                self._restaurar_dataset_original()
            elif opcion == "10":
                self._ver_historial_operaciones()
            elif opcion == "0":
                self._salir()
                break
            else:
                print("\n❌ Opción inválida. Por favor intente de nuevo.")
            
            # Pausa para que el usuario pueda leer la salida
            input("\nPresione Enter para continuar...")
    
    def _mostrar_bienvenida(self):
        """
        Muestra el mensaje de bienvenida.
        """
        print(Formateador.titulo("PROCESADOR DE DATOS INTERACTIVO", 70))
        print("Sistema modular de análisis de datos")
        print("Desarrollado con Python Standard Library\n")
        print("Este sistema permite:")
        print("  • Cargar datos desde archivos CSV")
        print("  • Limpiar y transformar datos")
        print("  • Realizar análisis estadísticos")
        print("  • Generar reportes en múltiples formatos")
        print(Formateador.separador(70, "="))
    
    def _mostrar_menu_principal(self):
        """
        Muestra el menú principal de opciones.
        """
        print("\n" + Formateador.separador(70, "="))
        print("MENÚ PRINCIPAL".center(70))
        print(Formateador.separador(70, "="))
        
        # Indicar si hay dataset cargado
        if self.dataset:
            print(f"📊 Dataset actual: {self.dataset.obtener_nombre()} ({self.dataset.cantidad_registros()} registros)")
        else:
            print("⚠  No hay dataset cargado")
        
        print(Formateador.separador(70, "-"))
        print("1. Cargar Dataset")
        print("2. Ver Resumen de Datos")
        print("3. Limpiar Datos")
        print("4. Aplicar Filtros y Transformaciones")
        print("5. Análisis Estadístico")
        print("6. Análisis de Ventas")
        print("7. Generar Reportes")
        print("8. Exportar Datos")
        print("9. Restaurar Dataset Original")
        print("10. Ver Historial de Operaciones")
        print("0. Salir")
        print(Formateador.separador(70, "="))
    
    def _cargar_dataset(self):
        """
        Carga un dataset desde un archivo CSV.
        """
        print(Formateador.titulo("CARGAR DATASET", 70))
        
        # Listar archivos CSV disponibles en /data
        archivos_csv = list(self.ruta_data.glob("*.csv"))
        
        if not archivos_csv:
            print("⚠  No se encontraron archivos CSV en la carpeta /data")
            print(f"   Ruta: {self.ruta_data}")
            return
        
        print("Archivos CSV disponibles:\n")
        for i, archivo in enumerate(archivos_csv, 1):
            print(f"  {i}. {archivo.name}")
        
        # Solicitar selección
        seleccion = input(f"\nSeleccione un archivo (1-{len(archivos_csv)}): ").strip()
        
        if not Validador.es_entero(seleccion):
            print("❌ Selección inválida")
            return
        
        indice = int(seleccion) - 1
        if indice < 0 or indice >= len(archivos_csv):
            print("❌ Número fuera de rango")
            return
        
        # Cargar el archivo seleccionado
        archivo_seleccionado = archivos_csv[indice]
        print(f"\n🔄 Cargando {archivo_seleccionado.name}...")
        
        try:
            cargador = CargadorCSV(str(archivo_seleccionado))
            self.dataset = cargador.cargar()
            
            # Guardar copia del dataset original
            # Nota: En una implementación más robusta, se haría una copia profunda
            cargador_copia = CargadorCSV(str(archivo_seleccionado))
            self.dataset_original = cargador_copia.cargar()
            
            # Inicializar procesadores
            self.limpiador = Limpiador(self.dataset)
            self.transformador = Transformador(self.dataset)
            
            # Registrar operación en BD
            self.registro_bd.registrar_operacion(
                dataset=self.dataset.obtener_nombre(),
                operacion="Cargar Dataset",
                parametros={'archivo': archivo_seleccionado.name, 'registros': self.dataset.cantidad_registros()}
            )
            
            print(f"\n✅ Dataset cargado exitosamente!")
            print(f"   • Registros: {self.dataset.cantidad_registros()}")
            print(f"   • Campos: {len(self.dataset.obtener_campos())}")
            
        except Exception as e:
            print(f"\n❌ Error al cargar el dataset: {str(e)}")
    
    def _ver_resumen_datos(self):
        """
        Muestra un resumen del dataset cargado.
        """
        if not self._validar_dataset_cargado():
            return
        
        print(Formateador.titulo("RESUMEN DE DATOS", 70))
        
        print(f"Nombre del Dataset: {self.dataset.obtener_nombre()}")
        print(f"Total de Registros: {self.dataset.cantidad_registros()}")
        print(f"Total de Campos: {len(self.dataset.obtener_campos())}\n")
        
        # Mostrar campos
        print("CAMPOS DISPONIBLES:")
        print(Formateador.separador(70, "-"))
        campos = self.dataset.obtener_campos()
        for i, campo in enumerate(campos, 1):
            valores_unicos = len(self.dataset.obtener_valores_unicos(campo))
            print(f"  {i}. {campo} ({valores_unicos} valores únicos)")
        
        # Mostrar primeros registros
        print(f"\nPRIMEROS 5 REGISTROS:")
        print(Formateador.separador(70, "-"))
        
        for i in range(min(5, self.dataset.cantidad_registros())):
            registro = self.dataset.obtener_registro(i)
            print(f"\nRegistro {i+1}:")
            datos = registro.obtener_todos_campos()
            for campo, valor in datos.items():
                print(f"  • {campo}: {valor}")
        
        # Registrar operación en BD
        self.registro_bd.registrar_operacion(
            dataset=self.dataset.obtener_nombre(),
            operacion="Ver Resumen",
            parametros={'registros_mostrados': min(5, self.dataset.cantidad_registros())}
        )
    
    def _limpiar_datos(self):
        """
        Ejecuta el proceso de limpieza de datos.
        """
        if not self._validar_dataset_cargado():
            return
        
        print(Formateador.titulo("LIMPIEZA DE DATOS", 70))
        
        print("Opciones de limpieza:\n")
        print("1. Limpieza completa (duplicados + vacíos)")
        print("2. Solo eliminar duplicados")
        print("3. Solo eliminar registros vacíos")
        print("4. Limpiar valores nulos de campos específicos")
        print("5. Ver reporte de calidad de datos")
        print("0. Volver")
        
        opcion = input("\nSeleccione una opción: ").strip()
        
        if opcion == "1":
            resultado = self.limpiador.limpiar_completo()
            self.registro_bd.registrar_operacion(
                dataset=self.dataset.obtener_nombre(),
                operacion="Limpieza Completa",
                parametros={'duplicados_eliminados': resultado.get('duplicados_eliminados', 0), 
                           'vacios_eliminados': resultado.get('vacios_eliminados', 0)}
            )
        elif opcion == "2":
            duplicados = self.limpiador.eliminar_duplicados()
            if duplicados == 0:
                print("✓ No se encontraron duplicados")
            self.registro_bd.registrar_operacion(
                dataset=self.dataset.obtener_nombre(),
                operacion="Eliminar Duplicados",
                parametros={'duplicados_eliminados': duplicados}
            )
        elif opcion == "3":
            vacios = self.limpiador.eliminar_registros_vacios()
            if vacios == 0:
                print("✓ No se encontraron registros vacíos")
            self.registro_bd.registrar_operacion(
                dataset=self.dataset.obtener_nombre(),
                operacion="Eliminar Vacíos",
                parametros={'vacios_eliminados': vacios}
            )
        elif opcion == "4":
            self._limpiar_valores_nulos()
        elif opcion == "5":
            self._mostrar_reporte_calidad()
        elif opcion == "0":
            return
        else:
            print("❌ Opción inválida")
    
    def _limpiar_valores_nulos(self):
        """
        Limpia valores nulos de campos específicos.
        """
        print("\nCAMPOS DISPONIBLES:")
        campos = self.dataset.obtener_campos()
        for i, campo in enumerate(campos, 1):
            print(f"  {i}. {campo}")
        
        seleccion = input("\nIngrese números de campos separados por comas (o 'todos'): ").strip()
        
        if seleccion.lower() == 'todos':
            campos_limpiar = None
        else:
            try:
                indices = [int(x.strip()) - 1 for x in seleccion.split(',')]
                campos_limpiar = [campos[i] for i in indices if 0 <= i < len(campos)]
            except:
                print("❌ Selección inválida")
                return
        
        valor_reemplazo = input("Valor de reemplazo (default: '0'): ").strip() or "0"
        
        resultado = self.limpiador.limpiar_valores_nulos(campos_limpiar, valor_reemplazo)
        
        # Registrar operación en BD
        self.registro_bd.registrar_operacion(
            dataset=self.dataset.obtener_nombre(),
            operacion="Limpiar Valores Nulos",
            parametros={'campos': str(campos_limpiar), 'valor_reemplazo': valor_reemplazo, 'valores_reemplazados': resultado}
        )
    
    def _mostrar_reporte_calidad(self):
        """
        Muestra el reporte de calidad de datos.
        """
        reporte = self.limpiador.obtener_reporte_calidad()
        
        generador = GeneradorReporteConsola("Reporte de Calidad de Datos")
        generador.establecer_datos(reporte)
        generador.generar()
    
    def _aplicar_filtros(self):
        """
        Aplica filtros y transformaciones al dataset.
        """
        if not self._validar_dataset_cargado():
            return
        
        print(Formateador.titulo("FILTROS Y TRANSFORMACIONES", 70))
        
        print("Opciones:\n")
        print("1. Filtrar por campo específico")
        print("2. Filtrar por rango numérico")
        print("3. Ordenar por campo")
        print("4. Ver registros agrupados por campo")
        print("5. Mostrar solo primeros N registros")
        print("0. Volver")
        
        opcion = input("\nSeleccione una opción: ").strip()
        
        if opcion == "1":
            self._filtrar_por_campo()
        elif opcion == "2":
            self._filtrar_por_rango()
        elif opcion == "3":
            self._ordenar_por_campo()
        elif opcion == "4":
            self._agrupar_por_campo()
        elif opcion == "5":
            self._mostrar_primeros_n()
        elif opcion == "0":
            return
        else:
            print("❌ Opción inválida")
    
    def _filtrar_por_campo(self):
        """
        Filtra el dataset por un campo y valor específico.
        """
        campos = self.dataset.obtener_campos()
        
        print("\nCAMPOS DISPONIBLES:")
        for i, campo in enumerate(campos, 1):
            print(f"  {i}. {campo}")
        
        seleccion = input(f"\nSeleccione campo (1-{len(campos)}): ").strip()
        
        if not Validador.es_entero(seleccion):
            print("❌ Selección inválida")
            return
        
        indice = int(seleccion) - 1
        if indice < 0 or indice >= len(campos):
            print("❌ Número fuera de rango")
            return
        
        campo_seleccionado = campos[indice]
        
        # Mostrar valores únicos
        valores_unicos = self.dataset.obtener_valores_unicos(campo_seleccionado)
        print(f"\nValores únicos en '{campo_seleccionado}':")
        for i, valor in enumerate(valores_unicos[:10], 1):
            print(f"  {i}. {valor}")
        if len(valores_unicos) > 10:
            print(f"  ... y {len(valores_unicos) - 10} más")
        
        valor = input(f"\nIngrese el valor a filtrar: ").strip()
        
        dataset_filtrado = self.transformador.filtrar_por_campo(campo_seleccionado, valor)
        
        # Registrar operación en BD
        self.registro_bd.registrar_operacion(
            dataset=self.dataset.obtener_nombre(),
            operacion="Filtrar por Campo",
            parametros={'campo': campo_seleccionado, 'valor': valor, 'registros_resultantes': dataset_filtrado.cantidad_registros()}
        )
        
        # Actualizar el dataset actual con el filtrado
        self.dataset = dataset_filtrado
        self.transformador = Transformador(self.dataset)
        self.limpiador = Limpiador(self.dataset)
    
    def _filtrar_por_rango(self):
        """
        Filtra por rango numérico.
        """
        campos = self.dataset.obtener_campos()
        
        print("\nCAMPOS DISPONIBLES:")
        for i, campo in enumerate(campos, 1):
            print(f"  {i}. {campo}")
        
        seleccion = input(f"\nSeleccione campo numérico (1-{len(campos)}): ").strip()
        
        if not Validador.es_entero(seleccion):
            print("❌ Selección inválida")
            return
        
        indice = int(seleccion) - 1
        if indice < 0 or indice >= len(campos):
            print("❌ Número fuera de rango")
            return
        
        campo_seleccionado = campos[indice]
        
        minimo = input("Valor mínimo: ").strip()
        maximo = input("Valor máximo: ").strip()
        
        if not Validador.es_numero(minimo) or not Validador.es_numero(maximo):
            print("❌ Los valores deben ser numéricos")
            return
        
        dataset_filtrado = self.transformador.filtrar_por_rango_numerico(
            campo_seleccionado, float(minimo), float(maximo)
        )
        
        # Registrar operación en BD
        self.registro_bd.registrar_operacion(
            dataset=self.dataset.obtener_nombre(),
            operacion="Filtrar por Rango",
            parametros={'campo': campo_seleccionado, 'minimo': minimo, 'maximo': maximo, 
                       'registros_resultantes': dataset_filtrado.cantidad_registros()}
        )
        
        self.dataset = dataset_filtrado
        self.transformador = Transformador(self.dataset)
        self.limpiador = Limpiador(self.dataset)
    
    def _ordenar_por_campo(self):
        """
        Ordena el dataset por un campo.
        """
        campos = self.dataset.obtener_campos()
        
        print("\nCAMPOS DISPONIBLES:")
        for i, campo in enumerate(campos, 1):
            print(f"  {i}. {campo}")
        
        seleccion = input(f"\nSeleccione campo (1-{len(campos)}): ").strip()
        
        if not Validador.es_entero(seleccion):
            print("❌ Selección inválida")
            return
        
        indice = int(seleccion) - 1
        if indice < 0 or indice >= len(campos):
            print("❌ Número fuera de rango")
            return
        
        campo_seleccionado = campos[indice]
        
        orden = input("¿Orden descendente? (s/n): ").strip().lower()
        descendente = orden == 's'
        
        self.transformador.ordenar_por_campo(campo_seleccionado, descendente)
        
        # Registrar operación en BD
        self.registro_bd.registrar_operacion(
            dataset=self.dataset.obtener_nombre(),
            operacion="Ordenar por Campo",
            parametros={'campo': campo_seleccionado, 'descendente': descendente}
        )
    
    def _agrupar_por_campo(self):
        """
        Agrupa y muestra totales por campo.
        """
        campos = self.dataset.obtener_campos()
        
        print("\nCAMPOS DISPONIBLES PARA AGRUPAR:")
        for i, campo in enumerate(campos, 1):
            print(f"  {i}. {campo}")
        
        seleccion = input(f"\nSeleccione campo (1-{len(campos)}): ").strip()
        
        if not Validador.es_entero(seleccion):
            print("❌ Selección inválida")
            return
        
        indice = int(seleccion) - 1
        if indice < 0 or indice >= len(campos):
            print("❌ Número fuera de rango")
            return
        
        campo_agrupar = campos[indice]
        
        print("\nCAMPOS NUMÉRICOS PARA SUMAR:")
        for i, campo in enumerate(campos, 1):
            print(f"  {i}. {campo}")
        
        seleccion2 = input(f"\nSeleccione campo (1-{len(campos)}): ").strip()
        
        if not Validador.es_entero(seleccion2):
            print("❌ Selección inválida")
            return
        
        indice2 = int(seleccion2) - 1
        if indice2 < 0 or indice2 >= len(campos):
            print("❌ Número fuera de rango")
            return
        
        campo_suma = campos[indice2]
        
        totales = self.transformador.calcular_totales_por_grupo(campo_agrupar, campo_suma)
        
        print(f"\nTOTALES DE '{campo_suma}' POR '{campo_agrupar}':")
        print(Formateador.separador(70, "-"))
        for grupo, total in sorted(totales.items(), key=lambda x: x[1], reverse=True):
            print(f"  {grupo}: {Formateador.formatear_moneda(total)}")
    
    def _mostrar_primeros_n(self):
        """
        Muestra los primeros N registros.
        """
        cantidad = input("\n¿Cuántos registros desea ver?: ").strip()
        
        if not Validador.es_entero(cantidad):
            print("❌ Debe ingresar un número entero")
            return
        
        n = int(cantidad)
        dataset_limitado = self.transformador.obtener_primeros_n(n)
        
        self.dataset = dataset_limitado
        self.transformador = Transformador(self.dataset)
        self.limpiador = Limpiador(self.dataset)
    
    def _analizar_estadisticas(self):
        """
        Realiza análisis estadístico del dataset.
        """
        if not self._validar_dataset_cargado():
            return
        
        print(Formateador.titulo("ANÁLISIS ESTADÍSTICO", 70))
        
        analizador = AnalizadorEstadistico(self.dataset)
        resultados = analizador.analizar()
        
        # Registrar operación en BD
        self.registro_bd.registrar_operacion(
            dataset=self.dataset.obtener_nombre(),
            operacion="Análisis Estadístico",
            parametros={'campos_analizados': len(resultados.get('campos', {}))}
        )
        
        # Generar reporte en consola
        generador = GeneradorReporteConsola("Análisis Estadístico")
        generador.establecer_datos(resultados)
        generador.generar()
    
    def _analizar_ventas(self):
        """
        Realiza análisis específico de ventas.
        """
        if not self._validar_dataset_cargado():
            return
        
        print(Formateador.titulo("ANÁLISIS DE VENTAS", 70))
        
        analizador = AnalizadorVentas(self.dataset)
        resultados = analizador.analizar()
        
        # Registrar operación en BD
        self.registro_bd.registrar_operacion(
            dataset=self.dataset.obtener_nombre(),
            operacion="Análisis de Ventas",
            parametros={'ventas_totales': resultados.get('ventas_totales', 0)}
        )
        
        # Generar reporte en consola
        generador = GeneradorReporteConsola("Análisis de Ventas")
        generador.establecer_datos(resultados)
        generador.generar()
    
    def _generar_reportes(self):
        """
        Genera reportes del dataset.
        """
        if not self._validar_dataset_cargado():
            return
        
        print(Formateador.titulo("GENERAR REPORTES", 70))
        
        print("Seleccione el tipo de análisis:\n")
        print("1. Reporte Estadístico")
        print("2. Reporte de Ventas")
        print("3. Reporte Personalizado")
        print("0. Volver")
        
        tipo = input("\nSeleccione opción: ").strip()
        
        if tipo == "0":
            return
        
        print("\nSeleccione el formato de salida:\n")
        print("1. Consola")
        print("2. Archivo TXT")
        print("3. Archivo JSON")
        print("4. Archivo XML")
        
        formato = input("\nSeleccione formato: ").strip()
        
        # Preparar datos según el tipo
        if tipo == "1":
            analizador = AnalizadorEstadistico(self.dataset)
            datos = analizador.analizar()
            titulo = "Reporte Estadístico"
        elif tipo == "2":
            analizador = AnalizadorVentas(self.dataset)
            datos = analizador.analizar()
            titulo = "Reporte de Ventas"
        elif tipo == "3":
            # Reporte con información básica
            datos = {
                'nombre_dataset': self.dataset.obtener_nombre(),
                'total_registros': self.dataset.cantidad_registros(),
                'campos': self.dataset.obtener_campos()
            }
            titulo = "Reporte Personalizado"
        else:
            print("❌ Opción inválida")
            return
        
        # Generar según formato
        if formato == "1":
            generador = GeneradorReporteConsola(titulo)
            generador.establecer_datos(datos)
            generador.generar()
            formato_str = "consola"
        elif formato in ["2", "3", "4"]:
            formato_map = {"2": "txt", "3": "json", "4": "xml"}
            formato_str = formato_map[formato]
            generador = GeneradorReporteArchivo(titulo, formato_str)
            generador.establecer_datos(datos)
            generador.generar()
        else:
            formato_str = "desconocido"
        
        # Registrar operación en BD
        if formato != "" and tipo in ["1", "2", "3"]:
            self.registro_bd.registrar_operacion(
                dataset=self.dataset.obtener_nombre(),
                operacion="Generar Reporte",
                parametros={'tipo_reporte': titulo, 'formato': formato_str}
            )
        
        if formato_str == "desconocido":
            print("❌ Formato inválido")
    
    def _exportar_datos(self):
        """
        Exporta el dataset actual a un archivo.
        """
        if not self._validar_dataset_cargado():
            return
        
        print(Formateador.titulo("EXPORTAR DATOS", 70))
        
        # Por ahora solo exportamos como JSON (CSV requeriría módulo csv)
        nombre = input("Nombre del archivo (sin extensión): ").strip()
        
        if not nombre:
            nombre = f"dataset_exportado"
        
        # Convertir dataset a diccionario
        datos_export = {
            'nombre': self.dataset.obtener_nombre(),
            'total_registros': self.dataset.cantidad_registros(),
            'campos': self.dataset.obtener_campos(),
            'registros': []
        }
        
        for registro in self.dataset.obtener_registros():
            datos_export['registros'].append(registro.obtener_todos_campos())
        
        # Exportar como JSON
        generador = GeneradorReporteArchivo("Dataset Exportado", "json")
        generador.establecer_datos(datos_export)
        ruta = generador.generar(nombre)
        
        # Registrar operación en BD
        self.registro_bd.registrar_operacion(
            dataset=self.dataset.obtener_nombre(),
            operacion="Exportar Datos",
            parametros={'formato': 'JSON', 'archivo': nombre, 'registros': self.dataset.cantidad_registros()}
        )
        
        print(f"\n✅ Dataset exportado exitosamente a: {ruta}")
    
    def _restaurar_dataset_original(self):
        """
        Restaura el dataset a su estado original.
        """
        if self.dataset_original is None:
            print("\n⚠  No hay dataset original para restaurar")
            return
        
        confirmacion = input("\n⚠  ¿Está seguro de restaurar el dataset original? (s/n): ").strip().lower()
        
        if confirmacion == 's':
            # Recargar desde archivo original
            try:
                archivo = self.ruta_data / f"{self.dataset_original.obtener_nombre()}.csv"
                if archivo.exists():
                    cargador = CargadorCSV(str(archivo))
                    self.dataset = cargador.cargar()
                    self.limpiador = Limpiador(self.dataset)
                    self.transformador = Transformador(self.dataset)
                    print("\n✅ Dataset restaurado al estado original")
                else:
                    print("\n❌ No se pudo encontrar el archivo original")
            except Exception as e:
                print(f"\n❌ Error al restaurar: {str(e)}")
    
    def _validar_dataset_cargado(self):
        """
        Valida que haya un dataset cargado.
        
        Returns:
            bool: True si hay dataset, False en caso contrario
        """
        if self.dataset is None or self.dataset.esta_vacio():
            print("\n⚠  No hay dataset cargado. Por favor, cargue un dataset primero.")
            return False
        return True
    
    def _ver_historial_operaciones(self):
        """
        Muestra el historial de operaciones registradas en la BD.
        """
        print(Formateador.titulo("HISTORIAL DE OPERACIONES", 70))
        
        print("Opciones:\n")
        print("1. Ver todas las operaciones")
        print("2. Ver últimas 10 operaciones")
        print("3. Ver estadísticas del historial")
        print("4. Exportar historial a archivo")
        print("5. Limpiar historial")
        print("0. Volver")
        
        opcion = input("\nSeleccione una opción: ").strip()
        
        if opcion == "1":
            operaciones = self.registro_bd.obtener_todas_operaciones()
            if not operaciones:
                print("\n⚠  No hay operaciones registradas")
            else:
                print(f"\nTotal de operaciones: {len(operaciones)}\n")
                print(Formateador.separador(70, "-"))
                for i, op in enumerate(operaciones, 1):
                    print(f"{i}. {op}")
                    if op.resultado:
                        print(f"   Resultado: {op.resultado}")
                    print()
        
        elif opcion == "2":
            operaciones = self.registro_bd.obtener_ultimas_n_operaciones(10)
            if not operaciones:
                print("\n⚠  No hay operaciones registradas")
            else:
                print(f"\nÚltimas {len(operaciones)} operaciones:\n")
                print(Formateador.separador(70, "-"))
                for i, op in enumerate(operaciones, 1):
                    print(f"{i}. {op}")
                    print()
        
        elif opcion == "3":
            stats = self.registro_bd.obtener_estadisticas()
            generador = GeneradorReporteConsola("Estadísticas del Historial")
            generador.establecer_datos(stats)
            generador.generar()
        
        elif opcion == "4":
            ruta = self.registro_bd.exportar_historial_texto()
            print(f"\n✅ Historial exportado a: {ruta}")
        
        elif opcion == "5":
            confirmacion = input("\n⚠  ¿Está seguro de limpiar TODO el historial? (s/n): ").strip().lower()
            if confirmacion == 's':
                if self.registro_bd.limpiar_historial():
                    print("\n✅ Historial limpiado exitosamente")
                else:
                    print("\n❌ Error al limpiar el historial")
        
        elif opcion == "0":
            return
        else:
            print("❌ Opción inválida")
    
    def _salir(self):
        """
        Finaliza la aplicación.
        """
        # Mostrar estadísticas finales de la sesión
        total_ops = self.registro_bd.contar_operaciones()
        print(Formateador.titulo("¡GRACIAS POR USAR EL SISTEMA!", 70))
        print("Desarrollado con Python Standard Library")
        print("Aplicando principios de POO y arquitectura modular")
        print(f"\n📊 Operaciones realizadas en esta sesión: {total_ops}")
        print(f"📁 Base de datos guardada en: {self.registro_bd.obtener_ruta_bd()}\n")


def main():
    """
    Función principal que inicia la aplicación.
    """
    try:
        app = AplicacionProcesadorDatos()
        app.ejecutar()
    except KeyboardInterrupt:
        print("\n\n⚠  Programa interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
