import gc

import numpy as np
import pandas as pd
import datetime as dt
from pathlib import Path

from . import eo
from . import dirs
from . import fechas

from .cl_TablasVC import *

#Ignorar las alertas porque el DataFrame está muy fragmentado. 
#Estorba al logeao en la consola, y además se soluciona al final del procesamiento de cada archivo
import warnings
warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)
warnings.filterwarnings(
    "ignore",
    category=FutureWarning,
    message=(
        ".*will attempt to set the values inplace instead of always setting a new array. "
        "To retain the old behavior, use either.*"),)

warnings.filterwarnings(
    "ignore",
    category=FutureWarning,
    message=(
        ".*elementwise comparison failed; returning scalar instead, but in the future will perform elementwise comparison*"),)
    

__all__ = ['DatosCROM']

class DatosCROM(TablasVC):
    
    def __init__(
        self,
        fecha_i = fechas.ayer(),
        fecha_f = fechas.ayer(),
        periodo = None,
        parques = [],
        dir_salida = dirs.raiz,
        cargar_incidencias = False,
        cargar_datos_basicos = 'offline',
        cargar_datos_segundales = False,
        reprocesar_segundales = False,
        estimar_ens_inc_abiertas = False,
        invalidar_datos_seg_congelados = False,
        consolidar_todo = False,
        reporte_consolidado = False,
        curvas_de_potencia = False,
        explotar_incidencias = False,
        exportar = False,
        mensajes_SQL = True,
        mensajes_procesamiento = 1,
        incidencias_a_editar = None
        ):

        self.__dir_salida = dir_salida
        self.__reprocesar_segundales = reprocesar_segundales
        self.__archivos_necesarios = None
        self.__archivos_encontrados = None
        self.__archivos_faltantes = None
        self.__archivos_disponibles = None
        self._datos_s = None
        self.__incidencias= None
        self.__incidencias_redux = None
        self.__incidencias_explotadas = None
        self.__incidencias_autodetectadas = None
        self.__indisponibilidades_autodetectadas = None
        self.__limitaciones_autodetectadas = None
        self.__rpt_iec61400_minutal = None
        self.__rpt_iec61400_incidencias = None
        self.__rpt_consolidado_status = False
        self.__rpt_consolidado = None
        self.__rpt_consolidado_redux = None
        self.__rpt_curvas_de_potencia = None
        self.__rpt_incidencias_resumen_diario = None
        self.__invalidar_datos_seg_congelados = invalidar_datos_seg_congelados

        if estimar_ens_inc_abiertas:
            cargar_datos_segundales = True
            if cargar_incidencias == False:
                cargar_incidencias = 'offline'
        
        if reporte_consolidado or consolidar_todo or estimar_ens_inc_abiertas:
            consolidar_todo = True
            cargar_datos_segundales = True
            if cargar_incidencias == False:
                cargar_incidencias = 'offline'
        
        if curvas_de_potencia:
            cargar_datos_segundales = True
        
        # Carvar curvas de potencia garantizada por WTG
        self.__curvas_garantizadas = Path(dirs.get_dc_cfg() + '\\' + 'Curvas_de_potencia.xlsx')
        self.__curvas_garantizadas = pd.read_excel(self.__curvas_garantizadas,sheet_name=None)
        
        super().__init__(
            cargar_incidencias = cargar_incidencias,
            cargar_datos_basicos = cargar_datos_basicos,
            parques = parques,
            solo_CROM = False,
            mensajes = mensajes_SQL,
        )
        
        self.__fecha_i = fechas.validar_fecha(fecha_i)
        self.__fecha_f = fechas.validar_fecha(fecha_f)
        self.__periodo = None
        
        if periodo is None: 
            self.fecha_i = self.__fecha_i
            self.fecha_f = self.__fecha_f
        else:
            try:
                self.periodo = periodo
            except:
                print("No se pudo procesar el parámetro periodo correctamente.")
                
                self.fecha_i = self.__fecha_i
                self.fecha_f = self.__fecha_f
                
                print(f"Fecha de inicio {self.fecha_i}")
                print(f"Fecha de fin {self.fecha_f}")
        
        if cargar_incidencias:
            self.__actualizar_incidencias()
        
        if mensajes_procesamiento not in [0,1,2]:
            print(f"Se esperaban valores [0,1,2] para 'mensajes_procesamiento' pero se recibió {mensajes_procesamiento}")
            print(f"Se procederá con mensajes_procesamiento=0 (intermedio)")
            self.__mensajes_procesamiento = 1
        else:
            self.__mensajes_procesamiento = mensajes_procesamiento
        
        if cargar_datos_segundales and len(parques)>0:
            self.cargar_segundales(mensajes_procesamiento=mensajes_procesamiento)
        
        if estimar_ens_inc_abiertas:
            self.estimar_ENS_incidencias_abiertas()
            
        if incidencias_a_editar is not None:
            if not isinstance(incidencias_a_editar,dict):
                raise TypeError(f'El parámetro "incidencias_a_editar" debería ser un diccionario pero es {type(incidencias_a_editar)}')
            
            for id, params in incidencias_a_editar.items():
                self.modificar_incidencia(id,**params)
        

        
        if cargar_incidencias and explotar_incidencias:
            if isinstance(explotar_incidencias,str):
                explotar_incidencias = explotar_incidencias.lower()
                if not explotar_incidencias in ['iec61400','crudas']:
                    raise ValueError(f'El parámetro "explotar_incidencias" debe ser "iec61400" o "crudas", pero no {explotar_incidencias}')
                
                self.explotar_incidencias(  
                    iec61400 = (explotar_incidencias == 'iec61400'),
                    granularidad = '1dia',)
                
            elif isinstance(explotar_incidencias,bool):
                if explotar_incidencias:
                    self.explotar_incidencias(iec61400 = False, granularidad = '1dia')
                    
            else:
                raise TypeError(f'El parámetro "explotar_incidencias" debe ser del tipo string y no {type(explotar_incidencias)}')

           
        if consolidar_todo and len(parques)>0:
            self.consolidar_todo(mensajes=(mensajes_procesamiento>1))
            
        if reporte_consolidado:
            self.elaborar_reporte_consolidado(mensajes=(mensajes_procesamiento>1))
        
        if curvas_de_potencia:
            self.elaborar_curvas_de_potencia()
                
        if exportar == False:
            pass
        elif exportar == True:
            self.exportar(reportes='todos')
        else:
            self.exportar(reportes=exportar)

    #
    # Propiedades. Getters y Setters
    #
    @property
    def fecha_i(self):
        return self.__fecha_i
    
    @fecha_i.setter
    def fecha_i(self,val):
        '''Ingresar una fecha para usar como fecha inicial del rango a analizar/pricesar
        Puede ser un objeto datetime.datetime o texto (string)'''
        fi = fechas.validar_fecha(val)
        self.__fecha_i = fi
        if self.__fecha_i <= self.__fecha_f:
            self.__actualizar_archivos()
            self.__actualizar_incidencias()

    @property
    def fecha_f(self):
        return self.__fecha_f

    @fecha_f.setter
    def fecha_f(self,val):
        '''Ingresar una fecha para usar como fecha final del rango a analizar/pricesar
        Puede ser un objeto datetime.datetime o texto (string)'''
        ff = fechas.validar_fecha(val)
        self.__fecha_f = ff
        if self.__fecha_i <= self.__fecha_f:
            self.__actualizar_archivos()
            self.__actualizar_incidencias()

    @property
    def incidencias(self):
        self.__actualizar_incidencias()
        return self.__incidencias
    
    @incidencias.setter
    def incidencias(self,val):
        raise AttributeError('La propiedad "incidencias" es de sólo lectura.')

    @property
    def incidencias_redux(self):
        self.__actualizar_incidencias()
        return self.__incidencias_redux
    
    @incidencias_redux.setter
    def incidencias_redux(self,val):
        raise AttributeError('La propiedad "incidencias_redux" es de sólo lectura.')

    @property
    def incidencias_explotadas(self):
        return self.__incidencias_explotadas
    
    @incidencias_explotadas.setter
    def incidencias_explotadas(self,val):
        raise AttributeError('La propiedad "incidencias_explotadas" es de sólo lectura.')
       
    @property
    def incidencias_iec61400(self):
        return self.__rpt_iec61400_incidencias
    
    @incidencias_iec61400.setter
    def incidencias_iec61400(self,val):
        raise AttributeError('La propiedad "incidencias_iec61400" es de sólo lectura.') 
       
    @property
    def incidencias_iec61400_minutal(self):
        return self.__rpt_iec61400_minutal
       
    @incidencias_iec61400_minutal.setter
    def incidencias_iec61400_minutal(self,val):
        raise AttributeError('La propiedad "incidencias_iec61400_minutal" es de sólo lectura.')

    @property
    def incidencias_autodetectadas(self):
        return self.__incidencias_autodetectadas
       
    @incidencias_autodetectadas.setter
    def incidencias_autodetectadas(self,val):
        raise AttributeError('La propiedad "incidencias_autodetectadas" es de sólo lectura.')

    @property
    def datos_seg(self):
        return self._datos_s
    
    @datos_seg.setter
    def datos_seg(self,val):
        self._datos_s = val
    
    @property
    def archivos_necesarios(self):
        '''Lista de Strings representando nombres de archivos con extensión
        No incluyen la ruta absoluta hacia su ubicación teórica'''
        return self.__archivos_necesarios

    @property
    def archivos_encontrados(self):
        '''Lista de objetos pathlib.Path con los archivos reales encontrados'''
        return self.__archivos_encontrados

    @property
    def archivos_faltantes(self):
        '''Archivos necesarios pero no encontrados
        Lista de Strings representando nombres de archivos con extensión
        No incluyen la ruta absoluta hacia su ubicación teórica'''
        return self.__archivos_faltantes

    @property
    def archivos_disponibles(self):
        '''Combinación de archivos necesarios y encontrados
        Lista de Strings representando nombres de archivos con extensión
        No incluyen la ruta absoluta hacia su ubicación teórica'''
        return self.__archivos_disponibles
        
    @archivos_necesarios.setter
    def archivos_necesarios(self,val):
        self.__archivos_necesarios = val
    
    @archivos_encontrados.setter
    def archivos_encontrados(self,val):
        self.__archivos_encontrados = val
    
    @archivos_faltantes.setter
    def archivos_faltantes(self,val):
        self.__archivos_faltantes = val
    
    @archivos_disponibles.setter
    def archivos_disponibles(self,val):
        self.__archivos_disponibles = val

    @property
    def dir_salida(self):
        return self.__dir_salida

    @dir_salida.setter
    def dir_salida(self,val):
        '''Toma una ruta a una carpeta en formato string o como objeto pathlib.Path'''
        self.__dir_salida = dirs.check_dir(val)
    
    @property
    def periodo(self):
        return self.__periodo
    
    @periodo.setter
    def periodo(self,val):
        if not (val is None):
            fi,ff = fechas.obtener_periodo(val)
            self.fecha_f = ff
            self.fecha_i = fi
            self.fecha_f = ff
            self.__periodo = val

    @property
    def consolidado(self):
        return self.__rpt_consolidado
    
    @consolidado.setter
    def consolidado(self,val):
        raise AttributeError('La propiedad "consolidado" es de sólo lectura.')

    @property
    def consolidado_redux(self):
        return self.__rpt_consolidado_redux
    
    @consolidado_redux.setter
    def consolidado_redux(self,val):
        raise AttributeError('La propiedad "consolidado_redux" es de sólo lectura.')

    @property
    def curvas_de_potencia(self):
        return self.__rpt_curvas_de_potencia
    
    @curvas_de_potencia.setter
    def curvas_de_potencia(self,val):
        raise AttributeError('La propiedad "curvas_de_potencia" es de sólo lectura.')

    @property
    def incidencias_resumen_diario(self):        
        return self.__rpt_incidencias_resumen_diario
    
    @incidencias_resumen_diario.setter
    def incidencias_resumen_diario(self,val):
        raise AttributeError('La propiedad "incidencias_resumen_diario" es de sólo lectura.')

    @property
    def incidencias_resumen_status(self):
        def agregar_subtotales(df):
            dfs = [(df
                    .loc[stat,:]
                    .sum()
                    .to_frame(name=(stat,'Subtotal'))
                    .T
                ) for stat in df.index.get_level_values(0).unique()
            ]

            return (pd
                .concat([df]+dfs)
                .sort_index()
            )
        
        def agregar_total(df):
            return (pd
                .concat([df, df
                    .reset_index()
                    .query('Nemo != "Subtotal"')
                    .set_index(['Status','Nemo'])
                    .sum(axis=0)
                    .to_frame(name=('','Total'))
                    .T
                    ]
                )
            )
        
        return (self.incidencias_redux
            .pivot_table(
                index=['Status','Nemo',],
                columns='Reason',
                values='Owner',
                aggfunc='count',
                fill_value=0,
            )
            .pipe(lambda adf: adf.join(adf.sum(axis=1).to_frame(name='Parque')))
            .pipe(agregar_subtotales)
            .pipe(agregar_total)
        )
        
    @incidencias_resumen_status.setter
    def incidencias_resumen_status(self,val):
        raise AttributeError('La propiedad "incidencias_resumen_status" es de sólo lectura.')
    
    #
    # Conjunto de funciones destinadas a procesar archivos de datos 10-segundales que se exportan automáticamente
    # desde la base de datos del Vision CROM y quedan en el OneDrive
    #
    def __actualizar_incidencias(self):
        
        if self.__fecha_i > self.fecha_f:
            print(f'Imposible actualizar incidencias. fecha_i {self.fecha_i} es mayor que fecha_f: {self.fecha_f}')
        else:
            if self.incidencias_todas is None:
                self.__incidencias= None
                
            elif not isinstance(self.incidencias_todas,pd.DataFrame):
                raise TypeError('El atributo "incidencias_todas" debe ser del tipo pandas.DataFrame o None')
            else:
                if self.incidencias_todas.empty:
                    self.__incidencias= None
                else:
                    
                    fi = self.fecha_i.replace(hour=0,minute=0,second=0)
                    ff = self.fecha_f.replace(hour=23,minute=59,second=59)
                    
                    flt_activa = self.incidencias_todas.Start.le(ff) & self.incidencias_todas.End.ge(fi) & self.incidencias_todas.Status.str.upper().ne('DESCARTADA')
                    flt_valida = self.incidencias_todas.Hours.ge(0) & self.incidencias_todas.ENS.ge(0) & self.incidencias_todas.Start.le(self.incidencias_todas.End)
                    
                    if self.parques != []:
                        flt_ucs = self.incidencias_todas['UC'].isin(self.parques) 
                        flt_nemos = self.incidencias_todas['Nemo'].isin(self.parques) 
                        flt_pq = flt_ucs | flt_nemos
                        flt = flt_activa & flt_valida & flt_pq
                    else:
                        flt = flt_activa & flt_valida

                    self.__incidencias= (self.incidencias_todas
                        .loc[flt,:]
                        .copy(deep=True)
                        .reset_index(drop=True)
                    )
                    
                    if not self.__incidencias is None:
                        cols_redux = ['ID','Status','Owner','Nemo','Equipo','Pnom','Start','End','Hours','ENS','SolvedBy','Reason','Origin','Code','Pteo','SP_P','BLC_Description']

                        self.__incidencias_redux = self.__incidencias.loc[:, cols_redux]

    def __actualizar_archivos(self):
        if self.__fecha_i > self.fecha_f:
            print(f'Imposible actualizar listados de archivos. fecha_i {self.fecha_i} es mayor que fecha_f: {self.fecha_f}')
        else:
            self.archivos_encontrados = self.__obtener_archivos_encontrados()
            self.archivos_necesarios = self.__obtener_archivos_necesarios()
            
            nombres_encontrados = [archivo.stem for archivo in self.archivos_encontrados]
            existe = lambda x: x.stem in nombres_encontrados
            no_existe = lambda x: not x.exists()

            self.archivos_faltantes = list(filter(no_existe,self.archivos_necesarios))
            self.archivos_disponibles = list(filter(existe,self.archivos_necesarios))
        
    def __obtener_archivos_encontrados(self):

        archivos_totales = self.__buscar_archivos_10s_ct_rango()
        parques_vacio = self.parques == [] or self.parques == None or len(self.parques)==0
        
        pertenece_a_parques_seleccionados = lambda archivo: any(p in archivo.name for p in self.parques)
        
        if parques_vacio:
            return archivos_totales
        else:
            return list(filter(pertenece_a_parques_seleccionados,archivos_totales))

    def __obtener_archivos_necesarios(self):
        
        iterable = fechas.iterar_entre_timestamps_diario(self.fecha_i,self.fecha_f)
        get_carpeta = lambda x : Path(dirs.get_dc_10s_fecha(x))
        
        carpetas = [get_carpeta(fi) for fi,_ in iterable]
        
        parques_vacio = self.parques == [] or self.parques == None or len(self.parques)==0
        parques = self.nemos if parques_vacio else self.parques

        if parques != []:
            archivos_necesarios = []
            for carpeta in carpetas:
                for parque in parques:

                    fecha_archivo = carpeta.stem.replace('-','.')
                    
                    archivo = f'{carpeta}\\{fecha_archivo} {parque}'
                    archivo_pickle = Path(archivo + '.pickle')
                    archivo_xlsx = Path(archivo + '.xlsx')
                    
                    if archivo_pickle.exists() and not self.__reprocesar_segundales:
                        archivos_necesarios.append(archivo_pickle)
                    else:
                        archivos_necesarios.append(archivo_xlsx)
                        
            return archivos_necesarios
        else:
            return []

    def __buscar_archivos_10s_ct_rango(self):
        
        iterable = fechas.iterar_entre_timestamps_diario(self.fecha_i,self.fecha_f)
        
        lista_de_listas = [self.__buscar_archivos10s_diarios(fi) for fi,_ in iterable]
        lista_unificada = [archivo for lista_archivos in lista_de_listas for archivo in lista_archivos]
        return lista_unificada

    def __buscar_archivos10s_diarios(self,fecha):
        '''Para un día determinado, busca los archivos .xlsx de la central elegida.
        Importante: la fecha debe proveerse como objeto datetime'''
        
        dir_tmp = Path(dirs.get_dc_10s_fecha(fecha))
        if dir_tmp.exists():
        
            iterable = dir_tmp.iterdir()
            
            archivos_xlsx = dirs.filtra_archivos(iterable,'.xlsx')
            archivos_pickle = dirs.filtra_archivos(iterable,'.pickle')
            
            nombres_archivos_pickle = (archivo.stem for archivo in archivos_pickle)
            
            archivos_xlsx_no_procesados = [archivo for archivo in archivos_xlsx if not (archivo.stem in nombres_archivos_pickle)]
            
            return archivos_pickle + archivos_xlsx_no_procesados

        else:
            return []

    def __renombrar_lvl0(self,texto,listado_equipos):
        texto = texto.replace('Datos del parque','PLANT')
        
        if 'Unnamed: 0_level_0' in texto:
            texto = ''
        
        if 'Datos del equipo' in texto:
            indice_generador = int(texto.split(' ')[-1])
            texto = listado_equipos[indice_generador-1]

        return texto

    def __renombrar_lvl1(self,texto):
        v = texto
        v = v.replace('Wind Dir','Wind_dir')
        v = v.replace('Wind Speed','Wind')
        v = v.replace('P Disponible','Ppos')
        v = v.replace('FB Consigna P Equipo','SP_P') 
        v = v.replace('Q Equipo','Q')
        v = v.replace('P Equipo','P')
        v = v.replace('Estado','op_state')
        v = v.replace('Consigna P','SP_P')
        v = v.replace('Consigna Q','SP_Q')
        v = v.replace('Consigna V','SP_V')
        v = v.replace('FB ','FB_')
        
        return v

    def __renombrar_cols(self,cols,nemo_parque):
        
        listado_equipos = self.consultar_equipos_no_agrupamientos(nemo_parque=nemo_parque)
        
        nuevas_cols = []
        for col in cols:
            lvl0 = self.__renombrar_lvl0(texto=col[0],listado_equipos=listado_equipos)
            lvl1 = self.__renombrar_lvl1(col[1])
            nuevas_cols.append((nemo_parque,lvl0,lvl1))
        
        nuevas_cols[0] = ('t_stamp','t_stamp','t_stamp')
    
        return pd.MultiIndex.from_tuples(nuevas_cols, names=['Parque','Equipo','Variable'])

    def __preprocesar_un_xlsx(self,archivo,mensajes_shallow=False,mensajes_deep=False):
        
        if archivo.exists():
            self.datos_seg = (pd
                .read_excel(archivo, skiprows=1, header=[0,1])
                #Devuelve una lista de tuples con formato (p,e,v) || p = parque, e = equipo (WTG), v = variable
                .pipe(lambda df_: df_.set_axis(
                    self.__renombrar_cols(
                        cols=df_.columns, 
                        nemo_parque= archivo.stem.split(' ')[-1]), 
                    axis=1)
                #Convierte la fecha en índice
                .pipe(lambda df_: df_.set_index(keys=('t_stamp','t_stamp','t_stamp'),drop=True))
                .rename_axis('t_stamp',axis=0))
            )

            if self.datos_seg.empty:
                print()
                print(f'\t ADVERTENCIA: El archivo {archivo.name} está vacío! Saltando procesamiento.')
                print()
            else:   
                if self.datos_seg.sum(axis=1).sum() == 0:
                    print()
                    print(f'\t ADVERTENCIA: El archivo {archivo.name} contiene todos los valores en 0 (cero)!')
                    print()
                self.__procesar_d10s(mensajes_shallow=mensajes_shallow,mensajes_deep=mensajes_deep)
                nuevo_archivo = str(archivo.parent) + '\\' + archivo.stem + '.pickle'
                if mensajes_shallow: print('\tGuardando archivo .pickle')
                self.datos_seg.to_pickle(nuevo_archivo,compression='bz2')
            
            self.datos_seg = None
            gc.collect()
        else:
            # Esto debería haber quedado solucionado con la lógica de archivos disponibles vs necesarios.
            # ¿Qué pasó?
            print(f'El archivo "{archivo.name}" no existe.')

    def __procesar_d10s(self,mensajes_shallow=True,mensajes_deep=True):
        '''Toma los datos 10 segundales pre-procesados y
        sobre ellos se realiza data cleaning/formating, feauture engineering'''
        
        # Procesamientos generales de aeros y planta
        if mensajes_shallow: print("\tCompletando registros faltantes")
        self.__procesar_d10s_dc(mensajes=mensajes_deep)
        
        # Procesamientos generales de aeros y planta
        if mensajes_shallow: print("\t(In)validación de datos")
        self.__procesar_d10s_dv(mensajes=mensajes_deep,invalidar=self.__invalidar_datos_seg_congelados)

        # Procesamientos generales de aeros
        if mensajes_shallow: print("\tIteración 1")
        self.__procesar_d10s_1i(mensajes=mensajes_deep)

        # Procesamientos específicos por parque 
        # Calcula potencias, energías, vientos promedios, direcciones, etc.
        # Por parque, agrupamiento(s) y agrega potencias nominales de equipos.
        if mensajes_shallow: print("\tIteración 2")
        self.__procesar_d10s_2i(mensajes=mensajes_deep)
        
        # Procesamientos por parque de todos los equipos
        # Magnitudes unitarias, coeficientes (FC, PI)
        if mensajes_shallow: print("\tIteración 3")
        self.__procesar_d10s_3i(mensajes=mensajes_deep)
        
        # Dedicada a procesar la Pposible y sus eventuales huecos
        if mensajes_shallow: print("\tIteración 4")
        self.__procesar_d10s_4i(mensajes=mensajes_deep)

        # Agrega variables booleanas que indican si un equipo está generando, consumiendo y si puede generar
        if mensajes_shallow: print("\tIteración 5")
        self.__procesar_d10s_5i(mensajes=mensajes_deep)     
           
        # Calcular (in)disponibilidad de datos
        if mensajes_shallow: print("\tIteración 6")
        self.__procesar_d10s_6i(mensajes=mensajes_deep)    

        # Calcular (in)disponibilidad de datos
        if mensajes_shallow: print("\tIteración 7")
        self.__procesar_d10s_7i(mensajes=mensajes_deep) 

        #Reordenar las columnas del dataframe
        levels = self.datos_seg.columns.names
        self.datos_seg.sort_index(
            axis=1,
            level=levels,
            ascending=[1 for _ in levels],
            inplace=True
            )
    
    def __procesar_d10s_dc(self,mensajes=True):
        #dc significa "Data Completion" o "Completado de datos"

        #Convertir columnas intxx a float64 porque éste último NO es experimental, y puede manejar los np.nans
        cols_int = self.datos_seg.select_dtypes('int').columns
        self.datos_seg.loc[:,cols_int] = self.datos_seg.loc[:,cols_int].astype('Float32')
        
        # Identificar registros (filas) faltantes, comparando contra un índice teórico 10 segundal
        index_real = self.datos_seg.index
        dia_datos_i = index_real[0].replace(hour=0,minute=0,second=0,microsecond=0)
        dia_datos_f = dia_datos_i.replace(hour=23,minute=59,second=50,microsecond=0)
        index_teorico = pd.date_range(
            start = dia_datos_i,
            end = dia_datos_f,
            freq = '10s',
            name = self.datos_seg.index.name
            )
        faltantes = [i for i in index_teorico if i not in index_real]
        if mensajes: print(f"\tRegistros faltantes: {faltantes}")
        
        if len(faltantes) > 0:
            self.datos_seg = self.datos_seg.reindex(index=index_teorico)
    
    def __procesar_d10s_dv(self,mensajes=True,invalidar=False):
        
        #dv significa "Data Validation" o "(In)Validación de datos"
        get_equipos = lambda x: self.consultar_equipos_no_agrupamientos(nemo_parque=x)
    
        #Identificar parques y aerogeneradores a procesar
        parques_con_datos = set(self.datos_seg.columns.get_level_values(0))
        
        #Validar o invalidar datos por columnas
        for p in parques_con_datos:
            
            equipos = ['PLANT'] + get_equipos(p)
            for e in equipos:
                for v in ['P','Q','Wind','Wind_dir','Ppos']:
                    s = (p,e,v)
        
                    if s not in self.datos_seg.columns:
                        continue
                    
                    g0 = self.datos_seg.loc[:,s] > 0
                    dis_a = self.datos_seg.loc[:,s] == self.datos_seg.loc[:,s].shift(-1)    # Un valor es igual al siguiente
                    dis_b = self.datos_seg.loc[:,s] == self.datos_seg.loc[:,s].shift(1)     # Un valor es igual al anterior
                    
                    if v == 'Ppos':
                        not_max = self.datos_seg.loc[:,s] < self.datos_seg.loc[:,s].max()
                        #Esto invalida todos los valores >0, <max y que haya al menos 2 iguales seguidos.
                        invalidos = g0 & not_max & (dis_a | dis_b) 
                    else:
                        #Esto invalida todos los valores >0 y que haya al menos 2 iguales seguidos.
                        invalidos = g0 & (dis_a | dis_b) 
                    
                    
                    if invalidar:
                        self.datos_seg.loc[invalidos,s] = np.nan
                    
                    if mensajes: 
                        inv = invalidos.sum()
                        print(f"Datos Inválidos para {p} {e} {v} : {inv/len(self.datos_seg.index):.2%}")
        
    def __procesar_d10s_1i(self,mensajes=True):
        #Esta función toma unos pocos segundos ejecutarse
        
        get_equipos = lambda x: self.consultar_equipos_no_agrupamientos(nemo_parque=x)
        get_curva_garantizada = lambda p,e: self.__curvas_garantizadas[p].loc[:,['WS',e]]
        
        #Identificar parques y aerogeneradores a procesar
        parques_con_datos = set(self.datos_seg.columns.get_level_values(0))

        #Procesar sólo algunas variables de los Aerogeneradores
        viento_vel_bins, viento_vel_labels = eo.crear_bins_viento_vel()
        viento_dir_bins, viento_dir_labels = eo.crear_bins_viento_dir()
        for p in parques_con_datos:

            # Cambio de unidades de las variables de planta
            if mensajes: print(f"Cambiando unidades de {p}'PLANT'")
            
            cols_disp = self.datos_seg.loc[:,(p,'PLANT',slice(None))].columns.get_level_values(2)
            vars_a_escalar = ['P','SP_P','Q']
            vars_encontradas = [v for v in vars_a_escalar if v in cols_disp]
            
            seleccion = (p,'PLANT',vars_encontradas)
            self.datos_seg.loc[:,seleccion] = self.datos_seg.loc[:,seleccion] * 1000    # de MW a kW
            
            equipos = get_equipos(p) + ['PLANT']
            k = len(equipos) +1 
            t = slice(None)
            i = 0
            for e in equipos:
                i+=1
                
                #Escalar datos de MW a kW para los parques que no sean de SENVION
                if not p in ['PEHERCUG','CEMALA1G','PEKOSTEG']:
                    if e != 'PLANT':
                        self.datos_seg.loc[:,(p,e,'P')] = self.datos_seg.loc[:,(p,e,'P')] * 1000
                
                if mensajes: print(f"Procesando {i} de {k} {p} {e}: Discriminando entre potencia generada de consumida")
                flt_p_gen = self.datos_seg.loc[:,(p,e,'P')] >= 0
                flt_p_con = self.datos_seg.loc[:,(p,e,'P')] <= 0

                self.datos_seg.loc[:,(p,e,'Pgen')] = self.datos_seg.loc[:,(p,e,'P')] * flt_p_gen
                self.datos_seg.loc[:,(p,e,'Pcon')] = self.datos_seg.loc[:,(p,e,'P')] * flt_p_con

                if e != 'PLANT':
                    if not (p,e,'Ppos') in self.datos_seg.loc[:,(p,e,slice(None))].columns:
                        if mensajes: print(f"Procesando {i} de {k} {p} {e}: Interpolando Potencia Posible Ppos a partir de la curva de potencia")
                        
                        try:
                            df_curva = get_curva_garantizada(p,e)
                            ws_min = df_curva['WS'].min()
                            ws_max = df_curva['WS'].max()
                            
                            viento_bajo = (self.datos_seg.loc[:,(p,e,'Wind')] < ws_min)
                            viento_alto = (self.datos_seg.loc[:,(p,e,'Wind')] > ws_max)
                            
                            fuera_de_rango = viento_bajo | viento_alto
                            viento_en_rango = ~fuera_de_rango
                            
                            self.datos_seg.loc[fuera_de_rango,(p,e,'Ppos')] = 0
                            self.datos_seg.loc[viento_en_rango,(p,e,'Ppos')] = np.interp(
                                                                    x = self.datos_seg.loc[viento_en_rango,(p,e,'Wind')],
                                                                    xp = df_curva['WS'],
                                                                    fp = df_curva.iloc[:,-1],
                                                                    left=0,
                                                                    right=0
                                                                    )
                        except:
                            print(f"No se logró interpolar la variable Ppos de {p} {e}")
                            self.datos_seg.loc[:,(p,e,'Ppos')] = 0
                            
                    self.datos_seg.loc[:,(p,e,'Epos')] = self.datos_seg.loc[:,(p,e,'Ppos')] * (10/3600)
                    if mensajes: print(f"Procesando {i} de {k} {p} {e}: Wind_bin")
                    self.datos_seg.loc[:,(p,e,'Wind_bin')] = pd.cut(
                                                            self.datos_seg.loc[:,(p,e,'Wind')],
                                                            bins=viento_vel_bins,
                                                            labels=viento_vel_labels,
                                                            ordered=True,
                                                            include_lowest=True
                                                            )
                
                    if mensajes: print(f"Procesando {i} de {k} {p} {e}: Wind_dir_r")
                    self.datos_seg.loc[:,(p,e,'Wind_dir_r')] = pd.cut(
                                                            self.datos_seg.loc[:,(p,e,'Wind_dir')],
                                                            bins=viento_dir_bins,
                                                            labels=viento_dir_labels,
                                                            ordered=False,
                                                            include_lowest=True
                                                            )
                
                if mensajes: print(f"Procesando {i} de {k} {p} {e}: Calculando energías")
                self.datos_seg.loc[:,(p,e,'Egen')] = self.datos_seg.loc[:,(p,e,'Pgen')] * (10/3600)
                self.datos_seg.loc[:,(p,e,'Econ')] = self.datos_seg.loc[:,(p,e,'Pcon')] * (10/3600)
            
            self.datos_seg = self.datos_seg.copy(deep=True)
            gc.collect()

    def __procesar_d10s_2i(self,mensajes=True):
        #Esta función toma 1 minuto por mes, aprox
        
        get_agrupamientos = lambda x: self.consultar_agrupamientos(nemo_parque=x)
        get_equipos = lambda x: self.consultar_equipos_no_agrupamientos(nemo_parque=x)
        get_equipos_agr = lambda parque,agrupamiento: self.consultar_equipos_por_agrupamiento(nemo_parque=parque)[agrupamiento]

        parques_con_datos = set(self.datos_seg.columns.get_level_values(0))
        viento_vel_bins, viento_vel_labels = eo.crear_bins_viento_vel()
        viento_dir_bins, viento_dir_labels = eo.crear_bins_viento_dir()
        
        vars_suma = ['Pgen','Pcon','Egen','Econ']
        
        for p in parques_con_datos:
            # Diccionario equipos y su potencia en MW
            ep = self.consultar_equipos(nemo_parque=p,potencia=True) # {'PLANT':80,'CIRCUITO n': 14, 'WTGnn':3.6}
            ep = {k:v*1000 for k,v in ep.items()}                           # Convertir de NW a kW
            
            #Procesar agrupamientos de aerogeneradores
            parque_agrupamientos = get_agrupamientos(p)
            for a in parque_agrupamientos:
                pot_a = ep[a]
                equipos_agrup = get_equipos_agr(p,a)

                cols_equip = self.datos_seg.loc[:,(p,equipos_agrup,slice(None))].columns.get_level_values(2)
                
                vars_suma_circ = [v for v in ['P', 'Q', 'SP_P'] if v in cols_equip]  # Completar columnas faltantes 
                vars_prom = [v for v in ['Wind','Wind_dir',] if v in cols_equip]
                
                vars_suma = vars_suma_circ + ['Pgen','Pcon','Egen','Econ']
                
                for var in vars_suma:
                    if mensajes: print(f"Procesando {p} {a}: {var}")
                    self.datos_seg.loc[:,(p,a,var)] = self.datos_seg.loc[:,(p,equipos_agrup,var)].sum(axis=1)
                
                for var in vars_prom:
                    if mensajes: print(f"Procesando {p} {a}: {var}")
                    self.datos_seg.loc[:,(p,a,var)] = self.datos_seg.loc[:,(p,equipos_agrup,var)].mean(axis=1).fillna(0)
                
                if mensajes: print(f"Procesando {p} {a}: Pnom")
                self.datos_seg.loc[:,(p,a,'Pnom')] = pot_a
                
                if mensajes: print(f"Procesando {p} {a}: Wind_bin")
                self.datos_seg.loc[:,(p,a,'Wind_bin')] = pd.cut(
                                                        self.datos_seg.loc[:,(p,a,'Wind')],
                                                        bins=viento_vel_bins,
                                                        labels=viento_vel_labels,
                                                        ordered=True,
                                                        include_lowest=True
                                                        )
                
                if (p,a,'Wind_dir') in self.datos_seg.loc[:,(p,a,slice(None))].columns:
                    if mensajes: print(f"Procesando {p} {a}: Wind_dir_r")
                    self.datos_seg.loc[:,(p,a,'Wind_dir_r')] = pd.cut(
                                                            self.datos_seg.loc[:,(p,a,'Wind_dir')],
                                                            bins=viento_dir_bins,
                                                            labels=viento_dir_labels,
                                                            ordered=False,
                                                            include_lowest=True
                                                            )

            #Procesar aerogeneradores, individualizados por parque
            parque_equipos = get_equipos(p)
            for e in parque_equipos:
                pot_e = ep[e]
                if mensajes: print(f"Procesando {p} {e}: Pnom")
                self.datos_seg.loc[:,(p,e,'Pnom')] = pot_e

            #Procesar variables de todo el parque ('PLANT')
            cols_equip = self.datos_seg.loc[:,(p,parque_equipos,slice(None))].columns.get_level_values(2)
            cols_pq = self.datos_seg.loc[:,(p,'PLANT',slice(None))].columns.get_level_values(2)
            
            # vars_suma = ['Pgen','Pcon','Egen','Econ']
            # vars_suma_pq = [v for v in vars_suma if (not(v in cols_pq) and (v in cols_equip) )] # Completar columnas faltantes 
            
            pot_p = ep['PLANT']
            if mensajes: print(f"Procesando {p}: Pnom")
            self.datos_seg.loc[:,(p,'PLANT','Pnom')] = pot_p
            
            # for var in vars_suma_pq:
            #     if mensajes: print(f"Procesando {p} 'PLANT': {var}")
            #     try:
            #         self.datos_seg.loc[:,(p,'PLANT',var)] = self.datos_seg.loc[:,(p,parque_agrupamientos,var)].sum(axis=1)
            #     except:
            #         self.datos_seg.loc[:,(p,'PLANT',var)] = self.datos_seg.loc[:,(p,parque_equipos,var)].sum(axis=1)
            
            vars_prom_pq = [v for v in ['Wind','Wind_dir',] if (not(v in cols_pq) and (v in cols_equip) )]
            for var in vars_prom_pq:
                if mensajes: print(f"Procesando {p} 'PLANT': {var}")
                self.datos_seg.loc[:,(p,'PLANT',var)] = self.datos_seg.loc[:,(p,parque_equipos,var)].mean(axis=1)

            if mensajes: print(f"Procesando {p} 'PLANT': Wind_bin")
            self.datos_seg.loc[:,(p,'PLANT','Wind_bin')] = pd.cut(
                                                    self.datos_seg.loc[:,(p,'PLANT','Wind')],
                                                    bins=viento_vel_bins,
                                                    labels=viento_vel_labels,
                                                    ordered=True,
                                                    include_lowest=True
                                                    )
            
            if (p,'PLANT','Wind_dir') in self.datos_seg.loc[:,(p,'PLANT',slice(None))].columns:
                if mensajes: print(f"Procesando {p} 'PLANT': Wind_dir_r")
                self.datos_seg.loc[:,(p,'PLANT','Wind_dir_r')] = pd.cut(
                                                        self.datos_seg.loc[:,(p,'PLANT','Wind_dir')],
                                                        bins=viento_dir_bins,
                                                        labels=viento_dir_labels,
                                                        ordered=False,
                                                        include_lowest=True
                                                        )
            
        self.datos_seg = self.datos_seg.copy(deep=True)
        gc.collect()

    def __procesar_d10s_3i(self,mensajes=True):
        # Esta función toma aprox 9 minutos para un mes, por parque
        parques_con_datos = set(self.datos_seg.columns.get_level_values(0))
    
        for p in parques_con_datos:
            # ep = Equipos del Parque 
            # ['PLANT','CIRCUITO 1',..,'CIRCUITO n','WTG01',...,'WTGnn]
            ep = self.consultar_equipos(nemo_parque=p)

            for e in ep:
                if mensajes: print(f"Procesando {p} {e} FC")
                self.datos_seg.loc[:,(p,e,'FC')] = self.datos_seg.loc[:,(p,e,'Pgen')] / self.datos_seg.loc[:,(p,e,'Pnom')]


        self.datos_seg = self.datos_seg.copy(deep=True)
        gc.collect()

    def __procesar_d10s_4i(self,mensajes=True):
        
        get_agrupamientos = lambda x: self.consultar_agrupamientos(nemo_parque=x)
        get_equipos = lambda x: self.consultar_equipos_no_agrupamientos(nemo_parque=x)
        get_equipos_agr = lambda parque,agrupamiento: self.consultar_equipos_por_agrupamiento(nemo_parque=parque)[agrupamiento]

        parques_con_datos = set(self.datos_seg.columns.get_level_values(0))
        for p in parques_con_datos:
            
            equipos = get_equipos(p)
            for e in equipos:
                eq = e
                ppos = (p,eq,'Ppos') ; pposu = (p,eq,'Ppos_U') ; pnom = (p,eq,'Pnom')
                
                if mensajes: print(f"Procesando {p} {eq}: Ppos_U")
                self.datos_seg.loc[:,pposu] = self.datos_seg.loc[:,ppos].div(self.datos_seg.loc[:,pnom])
                
            #Completar Ppos_U, Ppos y PI a nivel planta
            eq = 'PLANT'
            ppos = (p,eq,'Ppos') ; pposu = (p,eq,'Ppos_U') ; pnom = (p,eq,'Pnom')
            pi = (p,eq,'PI'); pgen = (p,eq,'Pgen'); epos = (p,eq, 'Epos')
            
            if mensajes: print(f"Procesando {p} {eq}: Ppos_U")
            self.datos_seg.loc[:,pposu] = self.datos_seg.loc[:,(p,equipos,'Ppos_U')].mean(axis=1)
            
            if mensajes: print(f"Procesando {p} {eq}: Ppos")
            self.datos_seg.loc[:,ppos] = self.datos_seg.loc[:,pposu] * self.datos_seg.loc[:,pnom]
            
            if mensajes: print(f"Procesando {p} {eq}: PI")
            self.datos_seg.loc[:,pi] = self.datos_seg.loc[:,pgen] / self.datos_seg.loc[:,ppos]

            if mensajes: print(f"Procesando {p} {eq}: Epos")
            self.datos_seg.loc[:,epos] = self.datos_seg.loc[:,ppos] * (10/3600)
            
            
            # Rellenar huecos de Ppos(_U) en generadores
            # Con el promedio de los que sí tienen Ppos(_U)
            for e in equipos:
                eq = e
                ppos = (p,eq,'Ppos') ; pposu = (p,eq,'Ppos_U') ; pnom = (p,eq,'Pnom') 
                pi = (p,eq,'PI') ; pgen = (p,eq,'Pgen'); epos = (p,eq, 'Epos')
                
                #Detectar huecos de Ppos (Es lo mismo que los huecos de Ppos_U)
                hay_hueco = self.datos_seg.loc[:,ppos].isna()
                
                if mensajes: print(f"Procesando {p} {eq}: Ppos_U (rellenando huecos)")
                self.datos_seg.loc[hay_hueco,pposu] =  self.datos_seg.loc[hay_hueco,(p,'PLANT','Ppos_U')]
                
                if mensajes: print(f"Procesando {p} {eq}: Ppos (rellenando huecos)")
                self.datos_seg.loc[hay_hueco,ppos]  = self.datos_seg.loc[hay_hueco,pposu] * self.datos_seg.loc[hay_hueco,pnom] 
                
                if mensajes: print(f"Procesando {p} {eq}: PI")
                self.datos_seg.loc[:,pi] = self.datos_seg.loc[:,pgen] / self.datos_seg.loc[:,ppos]

                if mensajes: print(f"Procesando {p} {eq}: Epos")
                self.datos_seg.loc[:,epos] = self.datos_seg.loc[:,ppos] * (10/3600)
                
            
            # Calcular Ppos_U y Ppos para los agrupamientos
            agrupamientos = get_agrupamientos(p)
            for a in agrupamientos:
                eq = a
                ppos = (p,eq,'Ppos') ; pposu = (p,eq,'Ppos_U') ; pnom = (p,eq,'Pnom')
                pi = (p,eq,'PI') ; pgen = (p,eq,'Pgen'); epos = (p,eq, 'Epos')
                
                equipos_agr = get_equipos_agr(p,a)
                
                if mensajes: print(f"Procesando {p} {eq}: Ppos_U")
                self.datos_seg.loc[:,pposu] = self.datos_seg.loc[:,(p,equipos_agr,'Ppos_U')].mean(axis=1)
                
                if mensajes: print(f"Procesando {p} {eq}: Ppos")
                self.datos_seg.loc[:,ppos] = self.datos_seg.loc[:,pposu] * self.datos_seg.loc[:,pnom] 
                
                if mensajes: print(f"Procesando {p} {eq}: PI")
                self.datos_seg.loc[:,pi] = self.datos_seg.loc[:,pgen] / self.datos_seg.loc[:,ppos] 

                if mensajes: print(f"Procesando {p} {eq}: Epos")
                self.datos_seg.loc[:,epos] = self.datos_seg.loc[:,ppos] * (10/3600)
                

        self.datos_seg = self.datos_seg.copy(deep=True)
        gc.collect()

    def __procesar_d10s_5i(self,mensajes=True):
        # Esta función simplemente agrega variables booleanas, que luego pueden servir para calcular el tiempo
        # de generación, de consumo o de horas posibles de generación, o de medición.

        get_equipos = lambda x: self.consultar_equipos(nemo_parque=x)

        vars = [
            ('Pgen','Gen'),
            ('Pcon','Con'),
            ('Ppos','Pos'),
        ]

        parques_con_datos = set(self.datos_seg.columns.get_level_values(0))
        for p in parques_con_datos:
            equipos = get_equipos(p)
            for e in equipos:
                for v1,v2 in vars:
                    s1 = (p,e,v1)
                    s2 = (p,e,v2)
                    if mensajes: print(f"{p} {e} Creando columnas {v1} y {v2}")
                    self.datos_seg.loc[:,s2] = (self.datos_seg.loc[:,s1].notna()) & (self.datos_seg.loc[:,s1] != 0)
                    self.datos_seg.loc[:,s2] = self.datos_seg.loc[:,s2].astype(pd.BooleanDtype())

    def __procesar_d10s_6i(self,mensajes=True):

        get_equipos = lambda x: self.consultar_equipos(nemo_parque=x)
        t = slice(None)
        k = 10/3600
        
        parques_con_datos = set(self.datos_seg.columns.get_level_values(0)) 
        for p in parques_con_datos:
            for e in get_equipos(p):
                if mensajes: print(f"{p} {e} calculando disponibilidad de datos")
                null = self.datos_seg.loc[:,(p,e,t)].isna().sum(axis=1)
                valid = self.datos_seg.loc[:,(p,e,t)].notna().sum(axis=1)
                total = null + valid
                self.datos_seg.loc[:,(p,e,'Datos_%')] = valid/total
                self.datos_seg.loc[:,(p,e,'RegistrosHs')] = k

    def __procesar_d10s_7i(self,mensajes=True):
        #Mejorar el uso de memoria
        if mensajes: print(f"Comprimiendo datos en la memoria")
        
        convert = {
            'category' : ['op_state'],
            'Float32' : self.datos_seg.select_dtypes('float64').columns.get_level_values(2).unique(),
            }
        
        t = slice(None)
        for dtype,cols in convert.items():
            if dtype == 'category':
                self.datos_seg.loc[:,(t,t,cols)] = self.datos_seg.loc[:,(t,t,cols)].fillna(-1)
            
            self.datos_seg.loc[:,(t,t,cols)] = self.datos_seg.loc[:,(t,t,cols)].astype(dtype)

    def preprocesar_archivos_disponibles(self,mensajes_procesamiento=0):
        
        mensajes_shallow = False if mensajes_procesamiento == 0 else True,
        mensajes_deep = False if mensajes_procesamiento < 2 else True
        
        ahora = dt.datetime.now()
        
        #Lista de objetos Path con la ruta completa hacia los archivos .xlsx o .pickle
        a_pre_procesar = [a for a in self.archivos_disponibles if a.name.lower().endswith('.xlsx')]
                         
        if a_pre_procesar:
            
            n_archivos = len(a_pre_procesar)
            n_elementos = 0
            
            # Calcula la cantidad de elementos (Parques, Circuitos y WTGS) se procesarán en total
            # Por cada día adicional, se repiten los elementos de un mismo parque
            for archivo in a_pre_procesar:
                parque = archivo.stem.split(' ')[-1]
                equipos = self.consultar_equipos(nemo_parque=parque)
                n_elementos += len(equipos)
            
            ritmo_slow = 1.80  # Segundos / Elemento, resulta de un promedio histórico y corridas de prueba
            ritmo_fast = 1.42  # Segundos / Elemento, resulta de un promedio histórico y corridas de prueba
            
            tiempo_slow = ritmo_slow * n_elementos * (1/60)  # Conversión a minutos
            tiempo_fast = ritmo_fast * n_elementos * (1/60)  # Conversión a minutos
            
            min_slow = int(tiempo_slow)
            min_fast = int(tiempo_fast)
            
            # %1 devuelve la parte decimal de un número (con un mínimo error)
            sec_slow = round((tiempo_slow % 1)*60)
            sec_fast = round((tiempo_fast % 1)*60)
            
            if mensajes_shallow: print(f'Se pre-procesarán {n_archivos} archivos Excel. Paciencia...')
            if mensajes_shallow: print(f'Tiempo estimado: entre {min_fast}min {sec_fast}seg y {min_slow}min {sec_slow}seg.')
            
            for archivo in a_pre_procesar:
                if mensajes_shallow: print(f'Pre-procesando: {archivo.name}')
                self.__preprocesar_un_xlsx(archivo,mensajes_shallow=mensajes_shallow,mensajes_deep=mensajes_deep)
                
            # Deshabilitar el fuerce de carga de archivos. 
            # Inevitablemente ya se re-procesó a esta altura.
            self.__reprocesar_segundales = False
            self.__actualizar_archivos()
            
            duracion = (dt.datetime.now() - ahora).total_seconds() 
            ritmo = duracion / len(a_pre_procesar)
            
            if mensajes_shallow: print(f'Pre-procesamiento finalizado. Duración: {round(duracion)}seg a razón de {round(ritmo)} seg/archivo.')

    def cargar_segundales(self,fecha_i=None,fecha_f=None,mensajes_procesamiento=0):
        if not fecha_i is None:
            self.fecha_i = fecha_i
        
        if not fecha_f is None:
            self.fecha_f = fecha_f
        
        self.preprocesar_archivos_disponibles(mensajes_procesamiento=mensajes_procesamiento)
        
        #Crear listas de dataframes con la información 10-segundal
        if len(self.archivos_disponibles) >0:
            if mensajes_procesamiento: print(f'Cargando {len(self.archivos_disponibles)} archivos en la memoria...')
            
            lista_dfs_ancha = []
            for p in self.parques:
                lista_dfs_larga = []
                for archivo in self.__archivos_disponibles:
                    if p in archivo.name:
                        if mensajes_procesamiento: print(f'\tCargando {archivo.name}...')
                        lista_dfs_larga.append(pd.read_pickle(archivo,compression='bz2')) 
                
                lista_dfs_ancha.append(pd.concat(lista_dfs_larga,ignore_index=False))
            
            # Concatenar todo en un único gran dataframe, con los parques a lo ancho y las estampas de tiempo a lo largo
            df_left = None
            for df_right in lista_dfs_ancha:
                
                if df_left is None:
                    df_left = df_right.copy(deep=True)
                else:
                    df_left = df_left.join(df_right,how='outer')
            
            self.datos_seg = df_left.copy(deep=True)
            
            
            # Identificar registros (filas) faltantes, comparando contra un índice teórico 10 segundal            
            dia_datos_i = self.fecha_i.replace(hour=0,minute=0,second=0,microsecond=0)
            dia_datos_f = self.fecha_f.replace(hour=23,minute=59,second=50,microsecond=0)
            
            index_teorico = pd.date_range(
                start = dia_datos_i,
                end = dia_datos_f,
                freq = '10s',
                name = self.datos_seg.index.name
                )
            faltantes = [i for i in index_teorico if i not in self.datos_seg.index]
            
            # En caso de que existan faltantes, completar
            if len(faltantes) > 0:
                if mensajes_procesamiento > 0: print(f"\tRegistros faltantes: {faltantes}")
                self.datos_seg = self.datos_seg.reindex(index=index_teorico)
            else:
                self.datos_seg.sort_index(
                    axis=0,
                    ascending=True,
                    inplace=True
                    )
            
            del df_left, df_right, lista_dfs_ancha, lista_dfs_larga,faltantes,index_teorico
            gc.collect()
        else:
            raise Exception(f'No hay archivos con datos 10 segundales disponibles para cargar de los parques {self.parques}')

    #
    # Conjunto de funciones destinadas a procesar las incidencias "crudas" (según las devuelve TablasVC())
    #
    def __check_jerarquia_equipos_iterable(self,iterable):
        
        valores_posibles = ['WTG','BOP','GRID']
        
        if len(iterable) != 3:
            raise Exception('El iterable con la jerarquía de priorización de incidencias, debe tener exactamente 3 elementos: "WTG","BOP" y "GRID" en algún orden.')
        
        for x in iterable:
            if not isinstance(x,str):
                raise ValueError(f'Error al procesar el valor {x}. El iterable con la jerarquía de priorización de incidencias, debe tener exactamente 3 elementos: "WTG","BOP" y "GRID" en algún orden.')
            
            if not x.upper() in valores_posibles:
                raise ValueError(f'Error al procesar el valor {x}. El iterable con la jerarquía de priorización de incidencias, debe tener exactamente 3 elementos: "WTG","BOP" y "GRID" en algún orden.')

        user_values = [x.upper() for x in iterable]
        k = len(user_values)
        return {v:(k-i) for i,v in enumerate(user_values)}

    def __check_jerarquia_equipos(self,jerarquia_equipos='WTG',mensajes=False):
        defaults = {
            'WTG'  : {'WTG': 3, 'BOP': 2, 'GRID': 1},
            'BOP'  : {'BOP': 3, 'WTG': 2, 'GRID': 1},
            'GRID' : {'GRID': 3, 'BOP': 2, 'WTG': 1}
        }
        
        if isinstance(jerarquia_equipos,str):
            if jerarquia_equipos.upper() in defaults.keys():
                return defaults[jerarquia_equipos]
            else:
                raise ValueError('El parámetro "método" debe ser "WTG", "BOP", "GRID", o una lista/tupla jerarquizando dichos grupos, de más importante a menos importante')
        elif isinstance(jerarquia_equipos,(list,tuple)):
            return self.__check_jerarquia_equipos_iterable(jerarquia_equipos)
        else:
            print(f"El valor recibido de jerarquia_equipos es: {jerarquia_equipos}. Tipo {type(jerarquia_equipos)}")
            raise TypeError('El parámetro "método" debe ser "WTG", "BOP", "GRID", o una lista/tupla jerarquizando dichos grupos, de más importante a menos importante')

    def __iec61400_crear_indice_fechas(self,mensajes=False):
        
        if self.incidencias.empty:
            #No hay incidencias, tomar fecha i y f del objeto
            fi = self.fecha_i
            ff = self.fecha_f
        else:
            #Obtener extremos de fecha del dataframe de incidencias
            fi = self.incidencias.Start.min()
            ff = max(self.incidencias.Start.max(),self.incidencias.End.max())
        
        # Devolver un DateTimeIndex minutal entre (e incluyendo) ambos extremos
        return pd.date_range(start=fi,end=ff,freq='1min',name='t_stamp')

    def __iec61400_crear_columnas_pev(self,index,mensajes=False):
        #pev = (Parque, Equipo, Variable)
        
        get_equipos_parque = lambda x: self.consultar_equipos(nemo_parque=x)
        get_pot_pe = lambda p,e: self.consultar_equipos(nemo_parque=p,potencia=True)[e]*1000

        n = len(index)

        v_str = ['SolverAgent','Reason','Origin'] 
        v_bool = ['FullPerf','Lim','LimExt','LimInt','Ind','IndExt','IndInt']
        v_int = {v:'Int64' for v in ['ID','Priority_IEC']}
        v_f64 = {v:'float64' for v in ['PotDis','ENS','ENS_Lim','ENS_LimExt','ENS_LimInt','ENS_Ind','ENS_IndExt','ENS_IndInt']}
        
        v_num = v_int | v_f64

        columnas = {}
        parques_con_datos = set(self.incidencias.Nemo)
        for p in parques_con_datos:
            for e in get_equipos_parque(p):
                #p = Parque, e = equipo
                
                columnas[(p,e,'Pnom')] = pd.Series(index=index, dtype='float64', data=np.full(n, fill_value = get_pot_pe(p,e)))

                for v in v_str:
                    columnas[(p,e,v)] = pd.Series(index=index, dtype=str, data=np.full(n,fill_value=np.nan))
                
                for v in v_bool:
                    columnas[(p,e,v)] = pd.Series(index=index, dtype=bool, data=np.full(n,fill_value=(v == 'FullPerf')))
                    
                for v,dtype in v_num.items():
                    columnas[(p,e,v)] = pd.Series(index=index, dtype=dtype, data=np.zeros(n))

        return columnas

    def __iec61400_preparar_df_vacio_minutal(self,mensajes=False):
        # A partir del DataFrame de incidencias contenido en el objeto DatosCROM().incidencias
        # se crea un dataframe vacío con índice de fechas minutal, con:
        #   inicio en la fecha Start de la incidencia más antigua
        #   finalización en la fecha End de la incidencia más reciente
        #   Columnas Multi Índice del tipo (Parque, Elemento, Variable). Elementos pueden ser = 'PLANT', 'CIRCUITO 1', 'WTG01', etc.
        
        i = self.__iec61400_crear_indice_fechas()
        c = self.__iec61400_crear_columnas_pev(i)
        
        self.__rpt_iec61400_minutal = pd.DataFrame(c,index=i)

    def __iec61400_explotar_minutalmente_incidencias(self,jerarquia_equipos='WTG',mensajes=False):
        
        # Con este diccionario, se convierte la columna Solver Agent a un número del 1 al 3, representando la
        # prioridad de desempate, en caso de haber incidencias solapadas con igual nivel de prioridad IEC
        rn = {'GENERATOR':'WTG','BOP_CONTRACTOR':'BOP','GRID_OPERATOR':'GRID'}
        rj = self.__check_jerarquia_equipos(jerarquia_equipos=jerarquia_equipos,mensajes=mensajes)
        
        # Crear una versión reducida del dataframe de incidencias del CROM
        df_inc = (self.incidencias
            .loc[:,[
                'ID','Nemo','Start','End','Equipo',
                'Pnom','Hours','ENS','SolverAgent',
                'Reason','Origin','Priority_IEC'
            ]]
            .assign(
                ENS = lambda adf: adf
                    .ENS
                    .mul(1000)
                    .div(adf.Hours * 60),
                    
                Pnom = lambda adf: adf
                    .Pnom
                    .mul(1000),

                SolverAgent = lambda adf: adf
                    .SolverAgent
                    .replace({k:rj[v] for k,v in rn.items()})
                    .astype('Int32')
            )
            .drop(columns=['Hours'])
            .copy(deep=True)
        )

        # DF minutal vacío, con espacio para todas las variables de las incidencias
        df = self.__rpt_iec61400_minutal
        
        #Inicia el ciclo para poblar el df vacío

        for _ , incidencia in df_inc.iterrows(): 
            ini = incidencia['Start']
            fin = incidencia['End'] 
            
            if fin > ini :
                fin -= dt.timedelta(minutes=1) #El minuto final no va incluido
            elif fin == ini:
                pass
            else:
                print(f'No se puede procesar la incidencia ID {incidencia["ID"]} porque la fecha de Finalización es menor que la fecha de inicio')
                
            p = incidencia['Nemo']          #Parque
            e = incidencia['Equipo']        #Equipo


            if mensajes: print(f"Procesando Incidencia {incidencia.ID} {e} {ini} {fin} {incidencia.Reason} {incidencia.Origin}")
            
            # Compartimentación de los tiempos y energía perdidos
            col_tba1 = ('Lim' if incidencia.Reason == 'LIMITATION' else 'Ind')
            col_tba2 = col_tba1 + incidencia.Origin.title()

            #Asignación de valores
            df.loc[ini:fin,(p,e, 'FullPerf')] = False
            df.loc[ini:fin,(p,e, col_tba1)] = True
            df.loc[ini:fin,(p,e, col_tba2)] = True
            
            # Esta forma de sumar energía, es resistente a solapamiento de incidencias para un mismo equipo
            # Realmente no debería suceder, pero si fuera el caso, que por lo menos no se pierda la ENS
            for v in ['ENS', f'ENS_{col_tba1}', f'ENS_{col_tba2}', ]:
                df.loc[ini:fin, (p,e,v)] = df.loc[ini:fin, (p,e,v)].add(incidencia.ENS, fill_value=0)
    
            #Descargar el resto de las variables
            for v in ['ID','Pnom','SolverAgent','Reason','Origin','Priority_IEC',]:
                df.loc[ini:fin,(p,e,v)] = incidencia[v]
        
        self.__rpt_iec61400_minutal = df

    def __iec61400_calcular_pot_dis(self,mensajes=False):
        
        df = self.__rpt_iec61400_minutal
        
        #Calcular la variable "Potencia Disponible" (PotDis) para todos los elementos del parque
        # en base a la Potencia Nominal (Pnom) y el estado del elemento (Indisponible (Ind) : True/False) 
        parques_con_datos = set(self.incidencias.Nemo)
        for p in parques_con_datos:
            
            #Potencia Disponible de Generadores
            equipos = self.consultar_equipos_no_agrupamientos(nemo_parque=p)
            for e in equipos:
                if mensajes: print(f"Calculando PotDis {p} {e} ")
                df.loc[:,(p,e,'PotDis')] = (~df.loc[:,(p,e,'Ind')]).mul(df.loc[:,(p,e,'Pnom')]).astype('float64')
                
            #Potencia Disponible de Agrupamientos
            agrupamientos = self.consultar_equipos_por_agrupamiento(nemo_parque=p)
            for a in agrupamientos.keys():
                if mensajes: print(f"Calculando PotDis {p} {a} ")
                df.loc[:,(p,a,'PotDis')] = (~df.loc[:,(p,a,'Ind')]).mul(df.loc[:,(p,a,'Pnom')]).astype('float64')
                df.loc[:,(p,a,'PotDis_Asociada')] = df.loc[:,(p,agrupamientos[a],'PotDis')].sum(axis=1)

            #Potencia Disponible de la Planta
            pl = 'PLANT'
            if mensajes: print(f"Calculando PotDis {p} {pl} ")
            df.loc[:,(p,pl,'PotDis')] = ((~df.loc[:,(p,pl,'Ind')]) * df.loc[:,(p,pl,'Pnom')]).astype('float64')
            df.loc[:,(p,pl,'PotDis_Asociada')] = df.loc[:,(p,equipos,'PotDis')].sum(axis=1)
            
        self.__rpt_iec61400_minutal = df

    def __iec61400_propagar_ens(self,mensajes=False):
        
        df = self.__rpt_iec61400_minutal
        
        vars_ens = [
            'ENS_Lim','ENS_LimExt','ENS_LimInt',
            'ENS_Ind','ENS_IndExt','ENS_IndInt',
        ]
        # A partir de acá se propone propagar la ENS desde los elementos 'más grandes' (PLANT) hacia los más pequeños (WTG)
        parques_con_datos = set(self.incidencias.Nemo)
        for p in parques_con_datos:
            
            agrupamientos = self.consultar_equipos_por_agrupamiento(nemo_parque=p)
            for a in agrupamientos.keys():
                for v in vars_ens:
                    for e in agrupamientos[a]:
                        if mensajes: print(f"Propagando {p} {a} {e} {v}")
                        proporcion = df.loc[:,(p,e,'PotDis')].div(df.loc[:,(p,a,'PotDis_Asociada')], fill_value=0)
                        ens_rolldown = df.loc[:,(p,a,v)].mul(proporcion, fill_value=0)
                        df.loc[:,(p,e,v)] = df.loc[:,(p,e,v)].add(ens_rolldown, fill_value=0)

            pl = 'PLANT'
            equipos = self.consultar_equipos_no_agrupamientos(nemo_parque=p)
            for v in vars_ens:
                for e in equipos:
                    if mensajes: print(f"Propagando ENS {p} {e} {v}")
                    proporcion =  df.loc[:,(p,e,'PotDis')].div(df.loc[:,(p,pl,'PotDis_Asociada')], fill_value=0)
                    ens_rolldown = df.loc[:,(p,pl,v)].mul(proporcion, fill_value=0)
                    df.loc[:,(p,e,v)] = df.loc[:,(p,e,v)].add(ens_rolldown, fill_value=0)

            for e in equipos:
                #Esto se hace en un ciclo aparte porque no todos los parques tienen agrupamientos
                if mensajes: print(f"Desagrupando ENS según tipo y origen de incidencia {p} {e}")
                df.loc[:,(p,e,'ENS_Lim')] = df.loc[:,(p,e,'ENS_LimExt')].add(df.loc[:,(p,e,'ENS_LimInt')], fill_value=0)
                df.loc[:,(p,e,'ENS_Ind')] = df.loc[:,(p,e,'ENS_IndExt')].add(df.loc[:,(p,e,'ENS_IndInt')], fill_value=0)
                df.loc[:,(p,e,'ENS')] = df.loc[:,(p,e,'ENS_Lim')].add(df.loc[:,(p,e,'ENS_Ind')], fill_value=0)
        
        self.__rpt_iec61400_minutal = df

    def __iec61400_propagar_tba(self,mensajes=False):
        '''Esta función puede tomar el df antes o después de haber sido populado, da igual.
        Por cuestiones de eficiencia, entiendo que sería mejor ejecutarlo luego de propagar la ENS'''
        
        df = self.__rpt_iec61400_minutal
        vars_a_copiar = [
            'ID',
            'SolverAgent','Reason','Origin','Priority_IEC',
            'LimExt','LimInt',
            'IndExt','IndInt',
        ]
        
        pl = 'PLANT'
        parques_con_datos = set(self.incidencias.Nemo)
        for p in parques_con_datos:
            # Para facilitar lectura, se preparan las variables que se utilizarán para seleccionar columnas en el multi índice
            # Formato: (parque, elemento, variable)
            # notar la diferencia entre pl, a, y e para las próximas asignaciones. pl = planta, a = agrupamiento y e = equipo
                          
            # Asumimos que BOP = Agrupamiento, para todos los parques del CROM
            flt_hay_incidencia_pl = df.loc[:,(p,pl,'Priority_IEC')] > 0
            agrupamientos = self.consultar_equipos_por_agrupamiento(nemo_parque=p)
            if agrupamientos != []:
                
                # Si hay agrupamientos, propagar primero PLANT -> CIRCUITO a
                for a in agrupamientos:                    
                    flt_pl_pisa_a_iec = df.loc[:,(p,pl,'Priority_IEC')] > df.loc[:,(p,a,'Priority_IEC')]
                    flt_pl_pisa_a_jer = df.loc[:,(p,pl,'SolverAgent')] > df.loc[:,(p,a,'SolverAgent')]
                    flt_iec_igual = df.loc[:,(p,pl,'Priority_IEC')] == df.loc[:,(p,a,'Priority_IEC')]
                    
                    migra_pl_a = flt_hay_incidencia_pl & (flt_pl_pisa_a_iec | (flt_iec_igual & flt_pl_pisa_a_jer) )
                    
                    # Transferir registros marcardos desde la planta hacia el el agrupamiento
                    for v in vars_a_copiar:
                        if mensajes: print(f"Propagando TBA {p} desde PLANT hacia {a} {v}")
                        df.loc[migra_pl_a,(p,a,v)] = df.loc[migra_pl_a,(p,pl,v)]

                    # Recalcular variables de disponibilidad
                    df.loc[migra_pl_a,(p,a,'Lim')] = df.loc[migra_pl_a,(p,a,'LimExt')] | df.loc[migra_pl_a,(p,a,'LimInt')]
                    df.loc[migra_pl_a,(p,a,'Ind')] = df.loc[migra_pl_a,(p,a,'IndExt')] | df.loc[migra_pl_a,(p,a,'LimInt')]
                    df.loc[migra_pl_a,(p,a,'FullPerf')] = ~(df.loc[migra_pl_a,(p,a,'Lim')] | df.loc[migra_pl_a,(p,a,'Ind')])
                    
                    #Una vez propagadas las incidencias sobre los circuitos, se procede a propagar CIRCUITO a -> WTG e
                    flt_hay_incidencia_a = df.loc[:,(p,a,'Priority_IEC')] > 0
                    equipos = agrupamientos[a]
                    for e in equipos:
                        flt_a_pisa_e_iec = df.loc[:,(p,a,'Priority_IEC')] > df.loc[:,(p,e,'Priority_IEC')]
                        flt_a_pisa_e_jer = df.loc[:,(p,a,'SolverAgent')] > df.loc[:,(p,e,'SolverAgent')]
                        flt_iec_igual = df.loc[:,(p,a,'Priority_IEC')] == df.loc[:,(p,e,'Priority_IEC')]
                        
                        migra_a_wtg = flt_hay_incidencia_a & (flt_a_pisa_e_iec | (flt_iec_igual & flt_a_pisa_e_jer) )

                        # Transferir registros marcardos desde el agrupamiento hacia la WTG
                        for v in vars_a_copiar:
                            if mensajes: print(f"Propagando TBA {p} desde {a} hacia {e} {v}")
                            df.loc[migra_a_wtg,(p,e,v)] = df.loc[migra_a_wtg,(p,a,v)]
                            
                        df.loc[migra_a_wtg,(p,e,'Lim')] = df.loc[migra_a_wtg,(p,e,'LimExt')] | df.loc[migra_a_wtg,(p,e,'LimInt')]
                        df.loc[migra_a_wtg,(p,e,'Ind')] = df.loc[migra_a_wtg,(p,e,'IndExt')] | df.loc[migra_a_wtg,(p,e,'LimInt')]
                        df.loc[migra_a_wtg,(p,e,'FullPerf')] = ~(df.loc[migra_a_wtg,(p,e,'Lim')] | df.loc[migra_a_wtg,(p,e,'Ind')])
                        
                        df.loc[migra_a_wtg,(p,e,'PotDis')] = ((~df.loc[migra_a_wtg,(p,e,'Ind')]) * df.loc[migra_a_wtg,(p,e,'Pnom')]).astype('float64')
                        
                    # El elemento "CIRCUITO a" ya fue procesado, por lo tanto lo podemos descartar.
                    cols = df.loc[:,(p,a,slice(None))].columns
                    df.drop(columns=cols,inplace=True)
                # El elemento PLANT ya fue procesado, por lo tanto lo podemos descartar.
                cols = df.loc[:,(p,pl,slice(None))].columns
                df.drop(columns=cols,inplace=True)
            else:       
                # En caso de que no haya circuitos (que no haya "BOP"), 
                # se procede directamente a propagar las incidencias desde la planta (PLANT) hacia las WTG 
                equipos = self.consultar_equipos_no_agrupamientos(nemo_parque=p)
                for e in equipos:
                    
                    flt_pl_pisa_e_iec = df.loc[:,(p,pl,'Priority_IEC')] > df.loc[:,(p,e,'Priority_IEC')]
                    flt_pl_pisa_e_jer = df.loc[:,(p,pl,'SolverAgent')] > df.loc[:,(p,e,'SolverAgent')]
                    flt_iec_igual = df.loc[:,(p,pl,'Priority_IEC')] == df.loc[:,(p,e,'Priority_IEC')]
                    
                    migra_pl_wtg = flt_hay_incidencia_pl & (flt_pl_pisa_e_iec | (flt_iec_igual & flt_pl_pisa_e_jer) )
                    
                    # Transferir registros marcardos desde la planta hacia la WTG
                    for v in vars_a_copiar:
                        if mensajes: print(f"Propagando TBA {p} desde PLANT hacia {e} {v}")
                        df.loc[migra_pl_wtg,(p,e,v)] = df.loc[migra_pl_wtg,(p,pl,v)]
                    df.loc[migra_pl_wtg,(p,e,'Lim')] = df.loc[migra_pl_wtg,(p,e,'LimExt')] | df.loc[migra_pl_wtg,(p,e,'LimInt')]
                    df.loc[migra_pl_wtg,(p,e,'Ind')] = df.loc[migra_pl_wtg,(p,e,'IndExt')] | df.loc[migra_pl_wtg,(p,e,'LimInt')]
                    df.loc[migra_pl_wtg,(p,e,'FullPerf')] = ~(df.loc[migra_pl_wtg,(p,e,'Lim')] | df.loc[migra_pl_wtg,(p,e,'Ind')])
                    df.loc[migra_pl_wtg,(p,e,'PotDis')] = ((~df.loc[migra_pl_wtg,(p,e,'Ind')]) * df.loc[migra_pl_wtg,(p,e,'Pnom')]).astype('float64')
                    
                # El elemento PLANT ya fue procesado, por lo tanto lo podemos descartar.
                cols = df.loc[:,(p,pl,slice(None))].columns
                df.drop(columns=cols,inplace=True)
                
        self.__rpt_iec61400_minutal = df

    def __iec61400_colapsar_nuevamente_a_incidencias(self,mensajes=False):
        
        get_pot_pe = lambda p,e: self.consultar_equipos(nemo_parque=p,potencia=True)[e]*1000
        
        # Filtrar las incidencias minutales según la fecha inicial del reporte, 
        # básicamente prevenir que haya fechas "antiguas" o "futuras" en las incidencias IEC61400
        # respecto del período seleccionado
        
        fecha_i = self.fecha_i.replace(hour=0,minute=0,second=0)
        fecha_f = self.fecha_f.replace(hour=23,minute=59,second=59)
        
        df = self.__rpt_iec61400_minutal.loc[fecha_i:fecha_f]
        
        lista_dfs = []
        parques_con_datos = set(self.incidencias.Nemo)
        for p in parques_con_datos:
            equipos = self.consultar_equipos_no_agrupamientos(nemo_parque=p)
            for e in equipos:
                if mensajes: print(f"Colapsando incidencias explotadas y desagrupadas según IEC61400 {p} {e}")
                # Identificar principios y fines de las incidencias serializadas
                    # De una serie de elementos, 
                    #   el primero es distinto al elemento anterior, y es igual al siguiente
                    #   el último es igual al anterior y distinto al siguiente
                    #   Son distintos de 0
                    #   No son Null
                # Los elementos únicos (un solo registro)
                    #   es distinto del elemento anterior
                    #   es distinto del elemento siguiente
                    #   es distinto de 0
                    #   No es Null
                v = 'ID'
                distinto_cero = df.loc[:,(p,e,v)] != 0
                distinto_nan = df.loc[:,(p,e,v)].notna()
                es_valido = distinto_cero & distinto_nan

                distinto_anterior = (df.loc[:,(p,e,v)] != df.loc[:,(p,e,v)].shift(1)).fillna(True)
                distinto_siguiente = (df.loc[:,(p,e,v)] != df.loc[:,(p,e,v)].shift(-1)).fillna(True)
                igual_anterior = (df.loc[:,(p,e,v)] == df.loc[:,(p,e,v)].shift(1)).fillna(True)
                igual_siguiente = (df.loc[:,(p,e,v)] == df.loc[:,(p,e,v)].shift(-1)).fillna(True)

                serie_pri = distinto_anterior & igual_siguiente & es_valido
                serie_ult = igual_anterior & distinto_siguiente & es_valido
                unicos = distinto_anterior & distinto_siguiente & es_valido

                #Creamos dos series, una para detectar las fechas de inicio de las nuevas incidencias y otra para las fechas de fin de dichas incidencias
                flt_fechas_ini = serie_pri | unicos
                flt_fechas_fin = serie_ult | unicos

                # Obtener fechas exactas de inicios y fines de incidencia
                fechas_ini = df.index[flt_fechas_ini].array
                fechas_fin = df.index[flt_fechas_fin].array

                # A partir de las fechas obtenidas, rellenar el resto de los valores de las incidencias
                n = len(fechas_ini)
                if n > 0:
                    ids = df.loc[fechas_ini,(p,e,v)].array
                    origenes = df.loc[fechas_ini,(p,e,'Origin')].array
                    razones = df.loc[fechas_ini,(p,e,'Reason')].array
        
                    data = {
                        'Nemo':pd.Series(np.full(n,dtype=object,fill_value=p)),
                        'Equipo':pd.Series(np.full(n,dtype=object,fill_value=e)),
                        'ID':pd.Series(ids),
                        'Start':pd.Series(fechas_ini),
                        'End':pd.Series(fechas_fin),
                        'Hours':pd.Series(np.zeros(n)),
                        'ENS':pd.Series(np.zeros(n)),
                        'Reason':pd.Series(razones),
                        'Origin':pd.Series(origenes),
                        'Pnom':pd.Series(np.full(n,fill_value=get_pot_pe(p,e)))
                    }

                    #Crear un dataframe temporal con los resultados
                    df_tmp = pd.DataFrame(data)
                    df_tmp['Hours'] = (df_tmp['End'] - df_tmp['Start']).dt.total_seconds()/3600
                    lista_dfs.append(df_tmp)
                    
        #la lista de dfs estará vacía, si no hay incidencias registradas
        if not lista_dfs:
            self.__rpt_iec61400_minutal = df
            self.__rpt_iec61400_incidencias = None
            print(f'No hay incidencias para el/los parque(s) {self.parques} en el periodo {self.fecha_i} a {self.fecha_f}')
        else:
            if mensajes: print(f"Concatenando resultados en un único listado de incidencias.")
            df_short = pd.concat(lista_dfs,axis=0,ignore_index=True).copy(deep=True)
            for i,row in df_short.iterrows():
                p = row['Nemo']
                e = row['Equipo']
                v = 'ENS'
                fi = row['Start']
                ff = row['End']
                if mensajes: print(f"Recuperando datos de ENS {row['ID']} {p} {e} {fi} a {ff}.")
                df_short.loc[i,'ENS'] = df.loc[fi:ff,(p,e,v)].sum()/1000
            
            self.__rpt_iec61400_minutal = df
            self.__rpt_iec61400_incidencias = df_short

    def __iec61400_ajustes_finales(self,mensajes=False,guardar_minutal=False):
        
        df_long = self.__rpt_iec61400_minutal
        df_short = self.__rpt_iec61400_incidencias
        
        vars_a_recuperar = [
            'ID',
            'Status', 'UC',  'Owner', 'SolvedBy',
            'ID_PT11', 'Code',
            'BLC_Description', 'BLC_Comments',
            'Owner_Description', 'Owner_AffectedEquipment', 'Owner_ActionsTaken',
            'Owner_Results', 'Owner_NextSteps', 'Owner_Comments', 
            'IEC_lvl1','IEC_lvl2', 'IEC_lvl3', 'IEC_lvl4', 'IEC_Label','Priority_IEC'
        ]

        cols_ordenadas = [
            'Owner', 'Nemo', 'UC', 'Equipo', 'Equipo_Orig', 
            'ID', 'Start', 'End', 'Hours', 'ENS', 'Pnom', 'Reason', 'Origin', 'SolvedBy', 'Status', 'Code','ID_PT11',
            'IEC_lvl1', 'IEC_lvl2', 'IEC_lvl3','IEC_lvl4', 'IEC_Label', 'Priority_IEC',
            'BLC_Description', 'BLC_Comments', 'Owner_Description',
            'Owner_AffectedEquipment', 'Owner_ActionsTaken', 'Owner_Results','Owner_NextSteps', 'Owner_Comments', 
        ]
        
        
        if df_short is None:
            #En caso de que no haya incidencias activas para el período
            df_short = pd.DataFrame(columns=cols_ordenadas)
        else:
            #Recuperar variables que no dependen del equipo o del tipo de equipo
            if mensajes: print(f"Recuperando variables originales que no dependen del equipo o del tiempo")
            df_short = pd.merge(left=df_short,right=self.incidencias.loc[:,vars_a_recuperar],on='ID',how='left')
            
            #Recuperar el equipo original del cual proviene la incidencia
            if mensajes: print(f"Recuperando equipo original del cual proviene la incidencia explotada y desagrupada.")
            get_equipo_original = lambda id: self.incidencias.query(f'ID == {id}').loc[:,'Equipo'].array[0]
            df_short.loc[:,'Equipo_Orig'] = df_short['ID'].apply(get_equipo_original)
            
            # Colocar nuevamente la variable de potencia nominal por fila
            df_short.loc[:,'Pnom'] = 0
            get_pot_equipo = lambda p,e: self.consultar_equipos(nemo_parque=p,potencia=True)[e]
            for p in df_short.Nemo.unique():
                equipos = df_short.loc[df_short.Nemo.eq(p),'Equipo'].unique()
                for e in equipos:
                    if mensajes: print(f"Colocando potencia a las incidencias de {p} {e}")
                    df_short.loc[df_short.Nemo.eq(p) & df_short.Equipo.eq(e),'Pnom'] = get_pot_equipo(p,e)
            
            #Reordenar dataframe
            df_short = df_short.loc[:,cols_ordenadas]

        if guardar_minutal:
            self.__rpt_iec61400_minutal = df_long
        else:
            self.__rpt_iec61400_minutal = None

        gc.collect()
        self.__rpt_iec61400_incidencias = df_short

    def interpretar_incidencias_bajo_iec61400(
        self,
        jerarquia_equipos='WTG',
        mensajes=False,
        guardar_minutal=False,
        exportar=False,
        ruta=None,
        nombre=None,): 
        
        if self.incidencias is None:
            self.consultar(incidencias='offline', mensajes=True)
        
        if not self.incidencias.empty:
            # Crea DF vacío sobre el cual se colocarán los datos de las incidencias
            self.__iec61400_preparar_df_vacio_minutal(mensajes=mensajes)

            #Popular el df vacío minutal, con datos de las incidencias
            self.__iec61400_explotar_minutalmente_incidencias(  
                jerarquia_equipos=jerarquia_equipos,
                mensajes=mensajes)
            
            #Agregar el dato de potencia disponible minutal por equipo, basado en el tipo de incidencia
            self.__iec61400_calcular_pot_dis(mensajes=mensajes) 
            
            # Propagar las proporciones de ENS correspondientes, desde arriba ('PLANT') hacia abajo ('WTG's)
            # pasando por los circuitos en caso de haberlos.
            self.__iec61400_propagar_ens(mensajes=mensajes) 
                                                                                                        
            # Priorización de motivo de incidencias, bajo norma IEC61400, 
            # sólo se tocan las columnas booleanas de disponibilidad//limitación
            # y se trasladan los motivos de incidencias desde arriba ('plant' / 'circuito x') hacia abajo ('wtg's)
            # IMPORTANTE: Aquí se eliminan todas las columnas PLANT y CIRCUITO a, ya que dejan de ser útiles
            self.__iec61400_propagar_tba(mensajes=mensajes)
            
            #Convertir el DataFrame minutal resultante, a un Dataframe con registros que tenga fecha desde-hasta (tipo incidencias)
            self.__iec61400_colapsar_nuevamente_a_incidencias(mensajes=mensajes)
            
            # Incorpora las variables faltantes de las incidencias originales, a partir de las cuales se trabajó
            # ejemplo: Equipo original del cual proviene la incidencia, ordenar columnas, reconvertir unidades, etc.
            self.__iec61400_ajustes_finales(guardar_minutal=guardar_minutal,mensajes=mensajes)

            # #Exportar reporte consolidado
            if exportar:
                #Preparar ruta y nombre de archivo para la exportación
                archivo = self.__exportar_configurar_archivo(
                    encabezado = 'Incidencias IEC61400',
                    ruta=ruta,
                    nombre=nombre
                )
                self.exportar(
                    reportes='incidencias_iec61400',
                    ruta=str(archivo.parent),
                    nombre=archivo.name
                )

    def identificar_solapamientos_incidencias(self,df=None):
        ''' Esta función toma un dataframe de incidencias formateado por el objeto blctools.DatosCROM() o blctools.TablasVC()
        y lo analiza iterativamente, en búsqueda de incidencias que se solapen para un mismo equipo y período en el tiempo.'''
        
        if df is None:
            df = self.incidencias
        
        # #Recorrer todas las incidencias y buscar incidencias solapadas
        conflictos = []
        for _, incidencia in df.iterrows():
            #Un filtro que cumple con todas las condiciones en simultáneo
            flt = (
                df.ID.ne(incidencia['ID']) & 
                df.Nemo.eq(incidencia['Nemo']) & 
                df.Equipo.eq(incidencia['Equipo']) & 
                df.Start.le(incidencia['End']) & 
                df.End.ge(incidencia['Start'])
            )
            
            if 'Status' in incidencia.index:
                flt &= df.Status.ne('DESCARTADA')

            if not df[flt].empty:
                conflictos.append(
                    {incidencia['ID'] : df.loc[flt,'ID'].to_list()}
                )

        from collections import Iterable
        
        # Convertir conflictos a DataFrame largo
        return (pd
            .DataFrame(conflictos)
            .melt(var_name='ID', value_name='IDs_solapados')
            .dropna()

            .applymap(lambda x: set(x) if isinstance(x,Iterable) else set([x]))
            .assign(IDs_con_solapamiento = lambda adf: adf.apply(lambda s: s.ID.union(s.IDs_solapados),axis=1))
            .query('~IDs_con_solapamiento.duplicated()')
            [['IDs_con_solapamiento']]
            .reset_index(drop=True)
        )

    #
    # Conjunto de funciones destinadas a explotar las incidencias.
    # Se puede seleccionar entre incidencias crudas, o IEC61400.
    #
    def __check_granularidad(self,granularidad,intervalos):
        
        if isinstance(granularidad,str):
            granularidad = granularidad.lower()
            if granularidad not in intervalos.keys():
                raise ValueError(f'La granularidad indicada no es un objeto datetime.timedelta ni está entre {list(intervalos.keys())}')
            else:
                return intervalos[granularidad]

        elif not isinstance(granularidad,dt.timedelta):
            raise TypeError('El parámetro "granularidad" debe ser del tipo string o datetime.timedelta.')
        else:
            return granularidad

    def __explotar_incidencia(self,incidencia,col_start='Start',col_end='End',granularidad='1dia'):

        intervalos = {
            '10seg':dt.timedelta(seconds=10),
            '1min':dt.timedelta(minutes=1),
            '5min':dt.timedelta(minutes=5),
            '10min':dt.timedelta(minutes=10),
            '15min':dt.timedelta(minutes=15),
            '1hora':dt.timedelta(hours=1),
            '1dia':dt.timedelta(days=1)
            }
        
        intervalo = self.__check_granularidad(granularidad,intervalos)

        fecha_ini_real = incidencia[col_start]
        fecha_fin_real = incidencia[col_end]
        fecha_ini_iter = fecha_ini_real.replace(hour=0,minute=0,second=0,microsecond=0)
        fecha_fin_iter = fecha_fin_real.replace(hour=23,minute=59,second=59,microsecond=0)

        data = {
            col_start:[],
            col_end:[],
            'Activa':[],
        }

        for fecha_i, fecha_f in fechas.iterar_entre_timestamps(fecha_ini_iter,fecha_fin_iter,intervalo):
            activa = (fecha_ini_real < fecha_f) and (fecha_fin_real >= fecha_i)
            
            data[col_start].append(fecha_i)
            data[col_end].append(fecha_f)
            data['Activa'].append(activa)

        # Sí la incidencia tiene solo un registro luego de ser explotada
        if len(data['Activa']) == 1:
            return pd.DataFrame(
                data=incidencia.to_dict(),
                index=[0]
            )

        #Continuamos con incidencias de duración mayor a un registro
        df = (pd
            .DataFrame(data)
            .query('Activa')
            .drop(columns=['Activa'])
            .reset_index(drop=True)
        )

        try:
            df.iloc[0,0] = fecha_ini_real   #Columna 'Start' y primera fila
            df.iloc[-1,1] = fecha_fin_real  #Columna 'End' y última fila
            
            #Colocando el tiempo y la energía perdidos
            df['Hours'] = (df
                [col_end]
                .sub(df[col_start])
                .dt
                .total_seconds()
                .div(3600)
            )
            
            df['ENS'] = (df.Hours
                .div(incidencia.Hours)
                .mul(incidencia.ENS)
            )

            #Colocando el resto de las columnas
            for c in incidencia.index:
                if c not in df.columns:
                    df[c] = incidencia[c]
            
            return df.loc[:,incidencia.index]
            
        except:
            print(f'Error al procesar la incidencia {incidencia["ID"]}')

    def explotar_incidencias(self,
            df=None,
            iec61400=True,
            col_start='Start',
            col_end='End',
            cols_seleccion=None,
            granularidad='1dia',
            exportar=False,
            ruta=None,
            nombre=None):
        
        #No custom dataframe was passed
        if df is None:
            if iec61400:
                
                self.interpretar_incidencias_bajo_iec61400()
                df = self.incidencias_iec61400
            else:
                df = self.incidencias
        
        #There's a dataframe passed, but it's empty
        if df.empty or df is None:
            self.__incidencias_explotadas = pd.DataFrame(columns=df.columns)
        else:
            if cols_seleccion is None:
                cols_seleccion = df.columns.to_list()
            
            date_start = df[col_start].dt.date
            date_end = df[col_end].dt.date
            
            #Acá ocurre la explosión de incidencias
            self.__incidencias_explotadas = (pd
                .concat(
                    objs= 
                        [df.loc[date_start == date_end, cols_seleccion]] + 
                        [self.__explotar_incidencia(
                            incidencia, 
                            col_start=col_start, 
                            col_end=col_end, 
                            granularidad=granularidad
                        )
                        for _ , incidencia in
                        df.loc[date_start != date_end, cols_seleccion].iterrows()
                    ]
                )
                .sort_values(
                    by=['ID','Equipo','Start'],
                    ignore_index=True
                )
            )
        # Explotar incidencias iec61400
        # interpretar bajo IEC 61400
        if iec61400:
            self.elaborar_resumen_diario_incidencias(explotar_e_interpretar=False)
            
            
        #Exportar reporte consolidado
        if exportar:
            #Preparar ruta y nombre de archivo para la exportación
            archivo = self.__exportar_configurar_archivo(encabezado = 'Incidencias explotadas',ruta=ruta,nombre=nombre)
            self.exportar(reportes='incidencias_explotadas',ruta=str(archivo.parent),nombre=archivo.name)

    #
    # Conjunto de funciones destinadas a detectar incidencias no registradas
    # Las mismas se utilizan para facilitar las funciones del Analista de Producción del CROM
    #
    def __identificar_indisponibilidad(self,parque,equipo,duracion=30,fc=0.00,ws=3,ppos_u=0.01,ws_pl=None,ppos_u_pl=None,mensajes=False):
        
        p = parque
        e = equipo
        
        flt_fc = self.datos_seg.loc[:,(p,e,'FC')].le(fc)
        flt_ppos_u = self.datos_seg.loc[:,(p,e,'Ppos_U')].ge(ppos_u)
        flt_ws = self.datos_seg.loc[:,(p,e,'Wind')].ge(ws)
        distinto_nan = (self.datos_seg
            .loc[:,(p,e,['Pgen','Ppos'])]
            .notna()
            .all(axis=1)
        )
        trigger_start = distinto_nan & flt_fc & flt_ppos_u & flt_ws
        
        if e != 'PLANT':
            if ws_pl: 
                flt_ws_pl = self.datos_seg.loc[:,(p,'PLANT','Wind')].ge(ws_pl)
                trigger_start = trigger_start & flt_ws_pl

            if ppos_u_pl: 
                flt_ppos_u_pl = self.datos_seg.loc[:,(p,'PLANT','Ppos_U')].ge(ppos_u_pl)
                trigger_start = trigger_start & flt_ppos_u_pl

        # Crear una serie "es_indisponibilidad" que:
        #       Si el aero está generando
        #           FALSO
        #       si no
        #           Si la condición de inicio de incidencia (trigger_start) es veradero:
        #               VERDADERO
        #           si no
        #               repite el estado anterior (ffill)
        
        # https://pandas.pydata.org/docs/reference/api/pandas.Series.mask.html
        # https://pandas.pydata.org/docs/reference/api/pandas.Series.ffill.html
        # https://pandas.pydata.org/docs/reference/api/pandas.Series.bfill.html
        
        generando = self.datos_seg.loc[:,(p,e,'Pgen')] > 0
        index = self.datos_seg.index
        arr = np.full(len(index),fill_value=np.nan)
        dtype = pd.BooleanDtype()

        es_indisponibilidad = pd.Series(data=arr,dtype=dtype,index=index,name=(p,e,'es_ind'))\
                                .mask(trigger_start,True)\
                                .mask(generando,False)\
                                .ffill()\
                                .bfill()
                                
        if mensajes: print(f"Buscando indisponibilidades {p} {e}, {es_indisponibilidad.sum()/3600:.2f} hs totales potencialmente detectadas")

        return es_indisponibilidad

    def __contraer_serie(self,serie_ind,serie_gen,mensajes=False):
            distinto_anterior = serie_ind.ne(serie_ind.shift(1)).bfill()
            distinto_siguiente = serie_ind.ne(serie_ind.shift(-1)).ffill()
            igual_anterior = serie_ind.eq(serie_ind.shift(1)).bfill()
            igual_siguiente = serie_ind.eq(serie_ind.shift(-1)).ffill()

            serie_pri = distinto_anterior & igual_siguiente & serie_ind
            serie_ult = igual_anterior & distinto_siguiente & serie_ind
            unicos = distinto_anterior & distinto_siguiente & serie_ind
            
            #Casos especiales cuando la película arranca/termina mal
            if not serie_gen[0] and serie_ind[0]:
                serie_pri[0] = True
                
            if not serie_gen[-1] and serie_ind[-1]:
                serie_ult[-1] = True
                
            # Obtener fechas exactas de inicios y fines de incidencia
            fechas_ini = self.datos_seg.index[serie_pri | unicos].array
            fechas_fin = self.datos_seg.index[serie_ult | unicos].array
            
            # extraer elementoe del tuple de las columnas del dataframe principal, que acá es el nombre de la serie
            p = serie_gen.name[0]   
            e = serie_gen.name[1]
            
            n = len(fechas_ini)
            if n > 0:
                if mensajes: print(f"Indisponibiliades encontradas: {p} {e} : {n} ")
                data = {
                    'Nemo':np.full(n,dtype=object,fill_value=p),
                    'Equipo':np.full(n,dtype=object,fill_value=e),
                    'Start':fechas_ini,
                    'End':fechas_fin,
                    'Hours':np.zeros(n),
                }
                #Crear un dataframe temporal con los resultados
                df_tmp = pd.DataFrame(data)
                df_tmp['Hours'] = (df_tmp['End'] - df_tmp['Start']).dt.total_seconds()
                df_tmp['Reason'] = 'FAILURE'

                return df_tmp
            else:
                return pd.DataFrame()

    def __identificar_indisponibilidades(self,duracion=30,fc=0.00,ws=3,ppos_u=0.01,ws_pl=None,ppos_u_pl=None,mensajes=False):
        
        def mensaje(pnom):
            mensaje = f"Duración >= {duracion}s, Pot <= {pnom*fc:.0f}kW, Ppos >= {ppos_u*pnom:.0f}kW, Wind >= {ws}m/s"
            if ws_pl: 
                mensaje += f"Wind (Plant avg) >= {ws_pl}m/s"
            if ppos_u_pl: 
                mensaje += f"Ppos_U (Plant avg) >= {ppos_u_pl}%"
                
            return mensaje
        
        # Crear series individualizadas indicando si a priori se detectó una incidencia o no
        # Una tira con datos cada 10 segundos, True/False
        dict_series = {}
        for p in self.datos_seg.columns.get_level_values(0).unique():
            for e in self.consultar_equipos(nemo_parque=p):
                es_indisponibilidad = self.__identificar_indisponibilidad(
                    p, e, duracion=duracion,
                    fc=fc, ws=ws, ppos_u=ppos_u,
                    ws_pl=ws_pl,ppos_u_pl=ppos_u_pl,
                    mensajes=mensajes
                )
                dict_series[(p,e)] = es_indisponibilidad
        
        # Ahora procederemos a hacer un roll-down de condiciones PLANT -> Agrupamiento - > WTG
        # Si hay una incidencia para la planta, omitir incidencias por WTG en simultáneo, digamos.
        df_incidencias = pd.DataFrame(data=dict_series)
        lista_dfs = []
        for p in self.datos_seg.columns.get_level_values(0).unique():
            
            agrupamientos = self.consultar_agrupamientos(nemo_parque=p,potencia=True)
            equipos_no_agrupados = self.consultar_equipos_no_agrupamientos(nemo_parque=p,potencia=True)
            
            pnom_planta = self.consultar_equipos(nemo_parque=p,potencia=True)['PLANT']*1000
            
            ind_planta = df_incidencias.loc[:,(p,'PLANT')]
            gen_planta = self.datos_seg.loc[:,(p,'PLANT','Pgen')] > 0
            
            df_tmp = self.__contraer_serie(ind_planta,gen_planta,mensajes=mensajes)
            df_tmp['Parámetros'] = mensaje(pnom_planta)
            
            if mensajes: print(f"Indisponibiliades encontradas: {p} PLANT: {len(df_tmp)}")

            lista_dfs.append(df_tmp)
            
            if agrupamientos:
                equipos_agrupados = self.consultar_equipos_por_agrupamiento(nemo_parque=p)
                
                for a,pnom_agrup in agrupamientos.items():
                    pnom_agrup *= 1000
                    
                    ind_agrup = df_incidencias.loc[:,(p,a)]
                    ind_agrup = (~ind_planta) & ind_agrup
                    gen_agrup = self.datos_seg.loc[:,(p,a,'Pgen')] > 0
                    
                    df_tmp = self.__contraer_serie(ind_agrup,gen_agrup,mensajes=mensajes)
                    df_tmp['Parámetros'] = mensaje(pnom_agrup)
                    
                    if mensajes: print(f"Indisponibiliades encontradas: {p} {a}: {len(df_tmp)}")
                    lista_dfs.append(df_tmp)
                    
                    for e in equipos_agrupados[a]:
                        pnom_equipo = equipos_no_agrupados[e]*1000
                        
                        ind_equipo = df_incidencias.loc[:,(p,e)]
                        ind_equipo = (~ind_planta) & (~ind_agrup) & ind_equipo
                        gen_equipo = self.datos_seg.loc[:,(p,e,'Pgen')] > 0
                        
                        df_tmp = self.__contraer_serie(ind_equipo,gen_equipo,mensajes=mensajes)
                        df_tmp['Parámetros'] = mensaje(pnom_equipo)
                        
                        if mensajes: print(f"Indisponibiliades encontradas: {p} {e}: {len(df_tmp)}")
                        lista_dfs.append(df_tmp)
            else:
                for e,pnom_equipo in equipos_no_agrupados.items():
                    pnom_equipo *= 1000
                    
                    ind_equipo = df_incidencias.loc[:,(p,e)]
                    ind_equipo = (~ind_planta) & ind_equipo
                    gen_equipo = self.datos_seg.loc[:,(p,e,'Pgen')] > 0
                    
                    df_tmp = self.__contraer_serie(ind_equipo,gen_equipo,mensajes=mensajes)
                    df_tmp['Parámetros'] = mensaje(pnom_equipo)
                    
                    if mensajes: print(f"Indisponibiliades encontradas: {p} {e}: {len(df_tmp)}")
                    lista_dfs.append(df_tmp)

        if not lista_dfs:
            self.__indisponibilidades_autodetectadas = None
            
        else:
            self.__indisponibilidades_autodetectadas =  (pd
                .concat(lista_dfs)
                .query(f'Hours >= {duracion}')
                .reset_index(drop=True)
                .assign(Hours = lambda adf: adf.Hours.div(3600))
            )
            
    def __obtener_indisponibilidad_relacionada(self,incidencia):
        p = incidencia['Nemo']
        e = incidencia['Equipo']
        
        if e in self.consultar_agrupamientos(nemo_parque=p):
            a = ''
        elif e == 'PLANT':
            a = ''
        else:
            a = self.consultar_agrupamiento_de_un_equipo(e,nemo_parque=p)
        
        query = f"\
        Nemo == '{p}' & Equipo in ('PLANT','{a}','{e}') & Reason != 'LIMITATION' & \
        Start <= '{incidencia['End']}' & End >= '{incidencia['Start']}'\
        "
        arr = self.incidencias_redux.query(query)['ID'].array
        
        if len(arr) > 1:
            return arr.tolist() 
        elif len(arr) == 1:
            return arr[0]
        else:
            return pd.NA
            
    def __obtener_indisponibilidades_relacionadas(self,mensajes=False):
        if mensajes: print(f"Intentando relacionar incidencias detectadas con incidencias crudas")
        
        if not self.__indisponibilidades_autodetectadas is None:
            self.__indisponibilidades_autodetectadas = (
                self.__indisponibilidades_autodetectadas
                    .assign(Relacionadas = lambda adf: 
                        adf.apply(self.__obtener_indisponibilidad_relacionada, axis = 1)
                    )
            )
            
    def __identificar_limitaciones(self,duracion=30,limitaciones_planta=True,limitaciones_equipos=False,mensajes=False):

        if not (limitaciones_planta or limitaciones_equipos):
            print(f"Parámetros limitaciones_planta y limitaciones_equipos son {limitaciones_planta} y {limitaciones_equipos} respectivamente. Imposible buscar limitaciones.")
            return

        dict_series = {}
        for p in self.datos_seg.columns.get_level_values(0).unique():
            if limitaciones_planta:
                if mensajes: print(f"Buscando limitaciones para {p} PLANT")
                dict_series[(p,'PLANT')] = (self.datos_seg
                    .loc[:,(p,'PLANT','SP_P')]
                    .lt(self.consultar_equipos(nemo_parque=p,potencia=True)['PLANT']*1000)
                )

            if limitaciones_equipos:
                equipos = self.consultar_equipos_no_agrupamientos(nemo_parque=p,potencia=True)

                for e,pnom in equipos.items():
                    if mensajes: print(f"Buscando limitaciones para {p} {e}")
                    limitacion = (self.datos_seg
                        .loc[:,(p,e,'SP_P')]
                        .lt(pnom*1000)
                    )
                    
                    if limitaciones_planta:
                        limitacion = limitacion & ~dict_series[(p,'PLANT')]
                        
                    dict_series[(p,e)] = limitacion
        

        #Una vez obtenidas todas las series para el parque p, comenzar a contraer las series
        lista_dfs = []
        for (p,e), limitacion in dict_series.items():
        
            distinto_anterior = limitacion.ne(limitacion.shift(1)).bfill()
            distinto_siguiente = limitacion.ne(limitacion.shift(-1)).ffill()
            igual_anterior = limitacion.eq(limitacion.shift(1)).bfill()
            igual_siguiente = limitacion.eq(limitacion.shift(-1)).ffill()

            serie_pri = distinto_anterior & igual_siguiente & limitacion 
            serie_ult = igual_anterior & distinto_siguiente & limitacion
            unicos = distinto_anterior & distinto_siguiente & limitacion

            #Casos especiales cuando la película arranca/termina mal
            if limitacion[0]:
                serie_pri[0] = True
                
            if limitacion[-1]:
                serie_ult[-1] = True
            
            # Obtener fechas exactas de inicios y fines de incidencia
            fechas_ini = limitacion.index[serie_pri | unicos].array
            fechas_fin = limitacion.index[serie_ult | unicos].array
            
            n = len(fechas_ini)
            if n > 0:
                #Crear un dataframe temporal con los resultados
                lista_dfs.append(pd
                    .DataFrame({
                        'Nemo':np.full(n,dtype=object, fill_value = p),
                        'Equipo':np.full(n,dtype=object, fill_value = e),
                        'Start':fechas_ini,
                        'End':fechas_fin,
                        'Hours':np.zeros(n),
                    })
                    .assign(Hours = lambda adf: 
                        adf.End
                        .sub(adf.Start)
                        .dt
                        .total_seconds()
                        .div(3600)
                    )
                )
                
        if not lista_dfs:
            self.__limitaciones_autodetectadas = None
        else:
            self.__limitaciones_autodetectadas = (pd
                .concat(lista_dfs)
                .query(f'Hours >= {duracion/3600}')
                .reset_index(drop=True)
                .assign(
                    Reason = 'LIMITATION',
                    Parámetros = f"Duración >= {duracion}s planta {limitaciones_planta}, equipos {limitaciones_equipos} "
                )
            )

    def __obtener_limitacion_relacionada(self,incidencia):
        p = incidencia['Nemo']
        e = incidencia['Equipo']

        query = f"\
        Nemo == '{p}' & Equipo == '{e}' & Reason == 'LIMITATION' & \
        Start <= '{incidencia['End']}' &  End >= '{incidencia['Start']}'\
        "
        arr = self.incidencias_redux.query(query)['ID'].array
        
        if len(arr) > 1:
            return arr.tolist() 
        elif len(arr) == 1:
            return arr[0]
        else:
            return pd.NA
    
    def __obtener_limitaciones_relacionadas(self,mensajes=False):
        if mensajes: print(f"Intentando relacionar limitaciones detectadas con incidencias crudas")

        if not self.__limitaciones_autodetectadas is None:
            self.__limitaciones_autodetectadas = (
                self.__limitaciones_autodetectadas
                .assign(
                    Relacionadas = lambda adf: adf.apply(self.__obtener_limitacion_relacionada, axis = 1)
                )
            )

    def buscar_indisponibilidades(self,
                                  duracion=30,
                                  factor_capacidad=0.00,
                                  wind_speed=3.75,
                                  ppos_u=0.03,
                                  wind_speed_planta=None,
                                  ppos_u_planta=None,
                                  mensajes=False,
                                  exportar=False,
                                  ruta=None,
                                  nombre=None):

        self.__indisponibilidades_autodetectadas = None
        
        self.__identificar_indisponibilidades(
            duracion=duracion,
            fc=factor_capacidad,
            ws=wind_speed,
            ppos_u=ppos_u,
            ws_pl=wind_speed_planta,
            ppos_u_pl=ppos_u_planta,
            mensajes=mensajes
            )

        self.__obtener_indisponibilidades_relacionadas(mensajes=mensajes)
        
        #Ojo, no confundir "incidencias (todo)" con "indisponibilidades" (eventos con equipos 100% fuera de servicio)
        self.__incidencias_autodetectadas = self.__indisponibilidades_autodetectadas
        if exportar:
            #Preparar ruta y nombre de archivo para la exportación
            archivo = self.__exportar_configurar_archivo(encabezado = 'Indisponibilidades autodetectadas', ruta=ruta, nombre=nombre)
            self.exportar(reportes='incidencias_autodetectadas', ruta=str(archivo.parent), nombre=archivo.name)

    def buscar_limitaciones(self,
                            duracion=30,
                            limitaciones_planta=True,
                            limitaciones_equipos=False,
                            mensajes=False,
                            exportar=False,
                            ruta=None,
                            nombre=None):
        
        self.__limitaciones_autodetectadas = None
        
        self.__identificar_limitaciones(
            duracion=duracion,
            limitaciones_planta=limitaciones_planta,
            limitaciones_equipos=limitaciones_equipos,
            mensajes=mensajes
        )
        self.__obtener_limitaciones_relacionadas(mensajes=mensajes)
        self.__incidencias_autodetectadas = self.__limitaciones_autodetectadas

        if exportar:
            #Preparar ruta y nombre de archivo para la exportación
            archivo = self.__exportar_configurar_archivo(encabezado = 'Limitaciones autodetectadas',ruta=ruta,nombre=nombre)
            self.exportar(reportes='incidencias_autodetectadas',ruta=str(archivo.parent),nombre=archivo.name)

    def buscar_incidencias(self,
                           duracion_lim=30,
                           duracion_ind=30,
                           limitaciones_planta=True,
                           limitaciones_equipos=False,
                           factor_capacidad=0.00,
                           wind_speed=3.75,
                           ppos_u=0.03,
                           wind_speed_planta=None,
                           ppos_u_planta=None,
                           mensajes=False,
                           exportar=False,
                           ruta=None,
                           nombre=None):

        self.__indisponibilidades_autodetectadas = None
        self.__limitaciones_autodetectadas = None
        
        self.__identificar_indisponibilidades(
            duracion = duracion_ind,
            fc = factor_capacidad,
            ws = wind_speed,
            ppos_u = ppos_u,
            ws_pl = wind_speed_planta,
            ppos_u_pl = ppos_u_planta,
            mensajes = mensajes
            )
        self.__obtener_indisponibilidades_relacionadas(mensajes=mensajes)
        
        self.__identificar_limitaciones(
            duracion = duracion_lim,
            limitaciones_planta = limitaciones_planta,
            limitaciones_equipos = limitaciones_equipos,
            mensajes = mensajes
            )
        self.__obtener_limitaciones_relacionadas(mensajes=mensajes)
        
        
        df_ind = self.__indisponibilidades_autodetectadas
        df_lim = self.__limitaciones_autodetectadas
        
        if df_ind is None and df_lim is None:
            self.__incidencias_autodetectadas = None
            
        elif isinstance(df_ind, pd.DataFrame) and df_lim is None:
            self.__incidencias_autodetectadas = self.__indisponibilidades_autodetectadas
            
        elif isinstance(df_lim, pd.DataFrame) and df_ind is None:
            self.__incidencias_autodetectadas = self.__limitaciones_autodetectadas
            
        elif isinstance(df_ind, pd.DataFrame) and isinstance(df_lim, pd.DataFrame):
            self.__incidencias_autodetectadas = (pd
                .concat([df_ind,df_lim])
                .sort_values(
                    by=['Nemo','Equipo','Start','End','Hours'],
                    ascending=[1,1,1,1,0],
                    ignore_index=True
                )
            )
        else:
            pass

        if exportar:
            #Preparar ruta y nombre de archivo para la exportación
            archivo = self.__exportar_configurar_archivo(encabezado = 'Incidencias autodetectadas',ruta=ruta,nombre=nombre)
            self.exportar(reportes='incidencias_autodetectadas',ruta=str(archivo.parent),nombre=archivo.name)

    #
    # Conjunto de funciones destinadas a facilitar el cálculo de ENS para incidencias
    #
    def __check_id(self, id_inc):
        try:
            return int(id_inc)
        except:
            raise Exception(f'No se pudo convertir el ID {id_inc} a el tipo de datos int')
    
    def __check_ids(self,ids_inc):
        tipos_iterables = (list,tuple,set,np.ndarray,pd.Series)
        
        if isinstance(ids_inc,str):
            return [self.__check_id(ids_inc)]
        
        elif isinstance(ids_inc,tipos_iterables):
            return [self.__check_id(id_inc) for id_inc in ids_inc]
        
        else:
            raise TypeError(f'El parámetro "ids" es {type(ids_inc)}, pero se esperaba alguno de {[str,int] + tipos_iterables} o cualquier otro numérico')
    
    def __check_datos_10s(self, id_inc, nemo, equipo, fi, ff):
        
        if self.datos_seg is None:
            raise Exception('No hay datos diez segundales cargados')
        
        parques_con_datos = self.datos_seg.columns.get_level_values(0).unique().tolist()
        if nemo not in parques_con_datos:
            raise ValueError(f'El parque {nemo} no se encuentra entre los datos diez segundales cargados, para {parques_con_datos}')
        
        equipos_parque = self.datos_seg.loc[:,(nemo,slice(None),slice(None))].columns.get_level_values(1).unique().tolist()
        if equipo not in equipos_parque:
            raise ValueError(f'El parque {nemo} no se encuentra entre los datos diez segundales cargados, para {parques_con_datos}')
        
        if self.datos_seg.index.min() > fi:
            raise ValueError(f'Los datos diez segundales no contienen el período requerido para analizar la incidencia deseada ID = {id_inc}\n' +
                             f'La fecha de inicio de los datos diez segundales es {self.datos_seg.index.min()} y la de la incidencia es {fi}')

        if self.datos_seg.index.max() < ff:
            raise ValueError(f'Los datos diez segundales no contienen el período requerido para analizar la incidencia deseada ID = {id_inc}\n' +
                             f'La fecha de inicio de los datos diez segundales es {self.datos_seg.index.max()} y la de la incidencia es {ff}')
    
    def __check_string(self,var,var_name,valores_posibles):
        if not isinstance(var,str):
            raise TypeError(f'El parámetro {var_name} debe ser del tipo string, y no {type(var)}')
        else:
            var = var.lower()
            if var not in valores_posibles:
                raise ValueError(f'El parámetro {var_name} debe ser uno de {valores_posibles} y no {var}.')
        
        return var
    
    def estimar_ENS_una_incidencia(self,
        id_inc, 
        muestra=.33,
        metodo='promedio',
        fuente='crudas',
        devolver_diccionario=False
        ):
        
        if muestra <=0 or muestra >1:
            raise ValueError(f'El parámetro muestra debe ser un valor entre (0 , 1]')
        
        metodo = self.__check_string(
            var=metodo,
            var_name='metodo',
            valores_posibles=['cuantil','promedio']
        )
        
        fuente = self.__check_string(
            var=fuente,
            var_name='fuente',
            valores_posibles=['crudas','explotadas','iec61400']
        )

        if fuente == 'crudas':
            df = self.incidencias
        elif fuente == 'explotadas':
            df = self.incidencias_explotadas
        else:
            df = self.incidencias_iec61400
            
        if df.query(f'ID == {self.__check_id(id_inc)}').empty:
            raise ValueError(f'No se encontró la incidencia con ID {id_inc}')
        else:
            df = df.query(f'ID == {id_inc}')
        
        resultados = {}
        for i, incidencia in df.iterrows():
            p = incidencia.Nemo
            e = incidencia.Equipo
            fi = incidencia.Start
            ff = incidencia.End
            equipos_no_agr = self.consultar_equipos_no_agrupamientos(nemo_parque=p)
            equipos_muestra = max([1,round(len(equipos_no_agr)*muestra)])
            
            iidd = incidencia.ID if (fuente =='crudas') else i
            
            # Validar que haya datos 10 segundales para dicha incidencia
            self.__check_datos_10s(id_inc,p,e,fi,ff)
            print(f'Estimando ENS: Incidencia {iidd} {p} {e} desde {fi} hasta {ff}')
            

            #Calcula el promedio de los n mejores factores de capacidad
            if metodo == 'promedio':
                fc_mejores = pd.Series(
                    name = 'Promedio',
                    index = self.datos_seg.loc[fi:ff,(p, equipos_no_agr, 'FC')].index,
                    data = (np.sort(self.datos_seg
                        .loc[fi:ff,(p, equipos_no_agr, 'FC')]
                        .fillna(0)
                        .to_numpy(dtype='float32')
                        )
                        [:,-equipos_muestra:]
                        .mean(axis=1)
                    )
                )
            else:
                #Calcula el quantil (1-muestra) de los factores de capacidad
                fc_mejores = pd.Series(
                    name = 'Cuantil',
                    index = self.datos_seg.loc[fi:ff,(p, equipos_no_agr, 'FC')].index,
                    data = np.quantile(
                        axis = 1,
                        q = 1 - muestra,
                        method='higher',
                        a = np.sort(
                            self.datos_seg
                                .loc[fi:ff,(p, equipos_no_agr, 'FC')]
                                .fillna(0)
                                .to_numpy(dtype='float32')
                        ),  
                    )
                )
                
            # Calcular ENS
            resultados[iidd] = {'ENS':self.datos_seg
                .loc[fi:ff,(p, e, 'Pnom')]                          # Aislar Potencia Nominal del equipo
                .mul(fc_mejores)                                    # Multiplicar Pnom por los factores de capacidad calculados
                .sub(self.datos_seg.loc[fi:ff,(p, e, 'Pgen')])      # Restar potencia activa efectivamente entregada
                .pipe(lambda s: s.mask(s.lt(0),0))                  # Filtrar eventuales valores negativos donde Pgen > Pteo
                .sum()                                              # Sumar todos los valores de la serie en un valor total
                .__mul__(10/3600)                                   # Convertir de potencia a energía
                .__truediv__(1000)                                  # Convertir de kWh a MWh
            }
        
        if devolver_diccionario:
            return resultados
        else:
            
            df = df.assign(ENS_Calculada = 0)
            if fuente == 'crudas':
                for i, params in resultados.items():
                    for _, v in params.items():
                        df.loc[df.ID.eq(i), 'ENS_Calculada'] = v
                        
            else:
                for i, params in resultados.items():
                    for _, v in params.items():
                        df.loc[i,'ENS_Calculada'] = v
            
            return df.copy(deep=True)
  
    def estimar_ENS_varias_incidencias(self,
        ids_inc,
        muestra=.33,
        metodo = 'promedio',
        fuente='crudas',
        devolver_diccionario=False):

        if muestra <=0 or muestra >1:
            raise ValueError(f'El parámetro muestra debe ser un valor entre (0 , 1]')
        
        metodo = self.__check_string(
            var=metodo,
            var_name='metodo',
            valores_posibles=['cuantil','promedio']
        )
        
        fuente = self.__check_string(
            var=fuente,
            var_name='fuente',
            valores_posibles=['crudas','explotadas','iec61400']
        )

        if fuente == 'crudas':
            df = self.incidencias
        elif fuente == 'explotadas':
            df = self.incidencias_explotadas
        else:
            df = self.incidencias_iec61400
        
        df_inc_selec = df[df.ID.isin(self.__check_ids(ids_inc))]
        
        resultados = {}
        for p in df_inc_selec.Nemo.unique():
            df_pq = df_inc_selec.query(f'Nemo == "{p}"')
            fi_pq = df_pq.Start.min()
            ff_pq = df_pq.End.max()
            
            equipos_no_agr = self.consultar_equipos_no_agrupamientos(nemo_parque=p)
            equipos_muestra = max([1, round(len(equipos_no_agr)*muestra)])
            
            #Calcula el promedio de los n mejores factores de capacidad
            if metodo == 'promedio':
                mejor_fc_pq = pd.Series(
                    name = 'Promedio',
                    index = self.datos_seg.loc[fi_pq:ff_pq,(p, equipos_no_agr, 'FC')].index,
                    data = (np.sort(self.datos_seg
                        .loc[fi_pq:ff_pq,(p, equipos_no_agr, 'FC')]
                        .fillna(0)
                        .to_numpy(dtype='float32')
                        )
                        [:,-equipos_muestra:]
                        .mean(axis=1)
                    )
                )
            else:
                #Calcula el quantil (1-muestra) de los factores de capacidad
                mejor_fc_pq = pd.Series(
                    name = 'Cuantil',
                    index = self.datos_seg.loc[fi_pq:ff_pq,(p, equipos_no_agr, 'FC')].index,
                    data = np.quantile(
                        axis = 1,
                        q = 1 - muestra,
                        method='higher',
                        a = np.sort(
                            self.datos_seg
                                .loc[fi_pq:ff_pq,(p, equipos_no_agr, 'FC')]
                                .fillna(0)
                                .to_numpy(dtype='float32')
                        ),  
                    )
                )
            
            # Comienzaz el cálculo por cada incidencia de cada parque
            for i, incidencia in df_pq.iterrows():
                e = incidencia.Equipo
                fi = incidencia.Start
                ff = incidencia.End
                
                iidd = incidencia.ID if (fuente =='crudas') else i
                # Validar que haya datos 10 segundales para dicha incidencia
                self.__check_datos_10s(incidencia.ID,p,e,fi,ff)
                
                resultados[iidd] = {'ENS':self.datos_seg
                    .loc[fi:ff,(p, e, 'Pnom')]
                    .mul(mejor_fc_pq.loc[fi:ff])
                    .sub(self.datos_seg.loc[fi:ff,(p, e, 'Pgen')])
                    .pipe(lambda ser_: ser_.mask(ser_.lt(0),0)) # No permitir ENS negativa
                    .sum()
                    .__mul__(10/3600)
                    .__truediv__(1000)
                }
        
        if devolver_diccionario:
            return resultados
        else:
            
            df_inc_selec = df_inc_selec.assign(ENS_Calculada = 0)
            if fuente == 'crudas':
                for i, params in resultados.items():
                    for _, v in params.items():
                        df_inc_selec.loc[df_inc_selec.ID.eq(i), 'ENS_Calculada'] = v
                        
            else:
                for i, params in resultados.items():
                    for _, v in params.items():
                        df_inc_selec.loc[i,'ENS_Calculada'] = v
            
            return df_inc_selec.copy(deep=True)
    
    def estimar_ENS_todas_las_incidencias(self,
        muestra=.33,
        metodo='promedio',
        fuente='crudas',
        incluir_limitaciones_ext=False):
        
        if muestra <=0 or muestra >1:
            raise ValueError(f'El parámetro muestra debe ser un valor entre (0 , 1]')
        
        metodo = self.__check_string(
            var=metodo,
            var_name='metodo',
            valores_posibles=['cuantil','promedio']
        )
        
        fuente = self.__check_string(
            var=fuente,
            var_name='fuente',
            valores_posibles=['crudas','explotadas','iec61400']
        )

        if fuente == 'crudas':
            df = self.incidencias
        elif fuente == 'explotadas':
            df = self.incidencias_explotadas
        else:
            df = self.incidencias_iec61400
        
        if not incluir_limitaciones_ext:
            df = df.query('Reason != "LIMITATION" or (Reason == "LIMITATION" & Origin == "INT")')
        
        resultados = {}
        for p in df.Nemo.unique():
            df_pq = df.query(f'Nemo == "{p}"')
            fi_pq = df_pq.Start.min()
            ff_pq = df_pq.End.max()
            
            equipos_no_agr = self.consultar_equipos_no_agrupamientos(nemo_parque=p)
            equipos_muestra = max([1, round(len(equipos_no_agr) * muestra)])
            
            #Calcula el promedio de los n mejores factores de capacidad
            if metodo == 'promedio':
                mejor_fc_pq =  pd.Series(
                    name = 'Promedio',
                    index = self.datos_seg.loc[fi_pq:ff_pq,(p, equipos_no_agr, 'FC')].index,
                    data = (np.sort(self.datos_seg
                        .loc[fi_pq:ff_pq,(p, equipos_no_agr, 'FC')]
                        .fillna(0)
                        .to_numpy(dtype='float32')
                        )
                        [:,-equipos_muestra:]
                        .mean(axis=1)
                    )
                )
            else:
                #Calcula el quantil (1-muestra) de los factores de capacidad
                mejor_fc_pq = pd.Series(
                    name = 'Cuantil',
                    index = self.datos_seg.loc[fi_pq:ff_pq,(p, equipos_no_agr, 'FC')].index,
                    data = np.quantile(
                        axis = 1,
                        q = 1 - muestra,
                        method='higher',
                        a = np.sort(
                            self.datos_seg
                                .loc[fi_pq:ff_pq,(p, equipos_no_agr, 'FC')]
                                .fillna(0)
                                .to_numpy(dtype='float32')
                        ),  
                    )
                )
            
            # Comienzaz el cálculo por cada incidencia de cada parque
            for i, incidencia in df_pq.iterrows():
                e = incidencia.Equipo
                fi = incidencia.Start
                ff = incidencia.End
                
                iidd = incidencia.ID if (fuente =='crudas') else i
                # Validar que haya datos 10 segundales para dicha incidencia
                self.__check_datos_10s(incidencia.ID,p,e,fi,ff)
                
                resultados[iidd] = {'ENS':self.datos_seg
                    .loc[fi:ff,(p, e, 'Pnom')]
                    .mul(mejor_fc_pq.loc[fi:ff])
                    .sub(self.datos_seg.loc[fi:ff,(p, e, 'Pgen')])
                    .pipe(lambda ser_: ser_.mask(ser_.lt(0),0)) # No permitir ENS negativa
                    .sum()
                    .__mul__(10/3600)
                    .__truediv__(1000)
                }
        

        df = df.assign(ENS_Calculada = 0)
        if fuente == 'crudas':
            for i, params in resultados.items():
                for _, v in params.items():
                    df.loc[df.ID.eq(i), 'ENS_Calculada'] = v
                    
        else:
            for i, params in resultados.items():
                for _, v in params.items():
                    df.loc[i,'ENS_Calculada'] = v
            
        return df.copy(deep=True)
    
    def estimar_ENS_incidencias_abiertas(self,
            muestra=.33,
            metodo='promedio',
            fuente='crudas'):
        
        if not self.incidencias.query('Status == "ABIERTA"').empty:
            
            r = self.estimar_ENS_varias_incidencias(
                ids_inc = self.incidencias.query('Status == "ABIERTA"').ID,
                muestra=muestra,
                metodo=metodo,
                fuente=fuente,
                devolver_diccionario=True
            )
            
            for id_inc, params in r.items():
                self.modificar_incidencia(id_inc,**params)
        else:
            print('No hay incidencias abiertas que requieran estimación de ENS')
    
    #
    # Conjunto de funciones destinadas a consolidar en los datos 10segundales
    # junto con el resultado de procesar las incidencias bajo IEC61400
    #
    def __consolidar_todo_preparar_df_10s(self,mensajes=False):
        # Preparar las columnas necesarias para poder descargar la info de las incidencias IEC61400, al DF de mediciones 10 segundales.

        i = self.datos_seg.index
        n = len(i)
        data = {}
        for p in self.datos_seg.columns.get_level_values(0).unique():
            for e in self.consultar_equipos(nemo_parque=p):
                
                if mensajes: print(f"Preparando {p} {e} para descargar datos de incidencias")

                data |= {
                            (p,e,'PBA'): pd.Series(np.ones(n), name=(p,e,'PBA'), index=i, dtype='Float32'),
                            (p,e,'TBA'): pd.Series(np.ones(n), name=(p,e,'TBA'), index=i, dtype='Float32'),
                            (p,e,'FullPerf'): pd.Series(np.full(n,fill_value=True), name=(p,e,'FullPerf'), index=i)           
                        }
                
                data |= {(p,e,v):
                            pd.Series(np.full(n,fill_value=False), name=(p,e,v), index=i)
                            for v in ['Ind','IndExt','IndInt','Lim','LimExt','LimInt',]
                        }
                
                data |= {(p,e,v):
                            pd.Series(np.zeros(n),name=(p,e,v), index=i, dtype='Float32')
                            for v in ['Pteo','Pteo_U','Eteo','Eteo_U','ENS','ENS_U',
                            'ENS_Ind','ENS_IndExt','ENS_IndInt','ENS_Lim','ENS_LimExt','ENS_LimInt']
                        }
    

        self.datos_seg = pd.concat([self.datos_seg,pd.DataFrame(data)],axis=1)

    def __consolidar_todo_descargar_incidencias(self,mensajes=False):
        
        #  Va leyendo las incidencias que correspondan, y las descargue en el df 10 segundal consolidado
        for _ , incidencia in self.incidencias_iec61400.iterrows():
        
            fi = incidencia['Start']
            ff = incidencia['End']
            p = incidencia['Nemo']
            e = incidencia['Equipo']

            if mensajes: print(f"Procesando incidencia {p} {e} {incidencia.ID}")
            
            ens_10 = 0
            ens_u = 0
            
            if incidencia.Hours:
                ens_10 = incidencia.ENS * 1000 * (10/3600) / incidencia.Hours  # Convertir MWh a kWh, y de valor promedio (horario) a diez segundal
                ens_u = ens_10 / incidencia.Pnom           # Convertir a un valor unitario, sirve para reponer datos en caso de faltantes
            
            self.datos_seg.loc[fi:ff,(p,e,'FullPerf')] = False
            self.datos_seg.loc[fi:ff,(p,e,'ENS')] = ens_10
            self.datos_seg.loc[fi:ff,(p,e,'ENS_U')] = ens_u
            
            # Categorizar indisponibilidad y su ENS
            orig = incidencia.Origin.title()
            tipo = 'Lim' if (incidencia.Reason == 'LIMITATION') else 'Ind'
            
            self.datos_seg.loc[fi:ff,(p,e,tipo)] = True
            self.datos_seg.loc[fi:ff,(p,e,tipo + orig)] = True
            self.datos_seg.loc[fi:ff,(p,e,f'ENS_{tipo}')] = ens_10
            self.datos_seg.loc[fi:ff,(p,e,f'ENS_{tipo + orig}')] = ens_10

    def __consolidar_todo_roll_up(self,mensajes=False):
        
        # Hacer un roll up de los estados lógicos FullPerf, Ind y Lim, desde las WTG hacia el parque y los circuitos
        for p in self.datos_seg.columns.get_level_values(0).unique():
            for a,equipos in self.consultar_equipos_por_agrupamiento(nemo_parque=p).items():
                if mensajes: print(f"Haciendo Roll-up de FullPerf/Ind-/Lim- y ENS_- de {p} {a}")
                
                for v in ['FullPerf','Ind','IndExt','IndInt','Lim','LimExt','LimInt']:
                    
                    #Variables de disponibilidad
                    if v == 'FulPerf':
                        self.datos_seg.loc[:,(p,a,v)] = self.datos_seg.loc[:,(p,equipos,v)].all(axis=1)
                    else:
                        self.datos_seg.loc[:,(p,a,v)] = self.datos_seg.loc[:,(p,equipos,v)].mean(axis=1)
                        
                    # Cálculo de ENS
                    if v != 'FullPerf': 
                        self.datos_seg.loc[:,(p,a,f'ENS_{v}')] = self.datos_seg.loc[:,(p,equipos,f'ENS_{v}')].sum(axis=1)
                        
                self.datos_seg.loc[:,(p,a,'ENS')] = self.datos_seg.loc[:,(p,equipos,'ENS')].sum(axis=1)
                self.datos_seg.loc[:,(p,a,'ENS_U')] = self.datos_seg.loc[:,(p,equipos,'ENS_U')].sum(axis=1)


            equipos = self.consultar_equipos_no_agrupamientos(nemo_parque=p)
            if mensajes: print(f"Haciendo Roll-up de FullPerf/Ind-/Lim- y ENS_- de {p} 'PLANT'")
            for v in ['FullPerf','Ind','IndExt','IndInt','Lim','LimExt','LimInt']:
                #Variables de disponibilidad
                if v == 'FulPerf':
                    self.datos_seg.loc[:,(p,'PLANT',v)] = self.datos_seg.loc[:,(p,equipos,v)].all(axis=1)
                else:
                    self.datos_seg.loc[:,(p,'PLANT',v)] = self.datos_seg.loc[:,(p,equipos,v)].mean(axis=1)
                
                # Cálculo de ENS
                if v != 'FullPerf': 
                    self.datos_seg.loc[:,(p,'PLANT',f'ENS_{v}')] = self.datos_seg.loc[:,(p,equipos,f'ENS_{v}')].sum(axis=1)
            
            self.datos_seg.loc[:,(p,'PLANT','ENS')] = self.datos_seg.loc[:,(p,equipos,'ENS')].sum(axis=1)
            self.datos_seg.loc[:,(p,'PLANT','ENS_U')] = self.datos_seg.loc[:,(p,equipos,'ENS_U')].sum(axis=1)
            
            # Calcular variables dependientes de las variables recientemente calculadas, para todos los equipos del parque
            for e in self.consultar_equipos(nemo_parque=p):
                if mensajes: print(f"Haciendo Roll-Up de TBA/PBA/Pteo {p} {e}")
                self.datos_seg.loc[:,(p,e,'TBA')] = 1 - self.datos_seg.loc[:,(p,e,'Ind')]
                self.datos_seg.loc[:,(p,e,'Eteo')] = self.datos_seg.loc[:,(p,e,'Egen')] + self.datos_seg.loc[:,(p,e,'ENS')]
                self.datos_seg.loc[:,(p,e,'Pteo')] = self.datos_seg.loc[:,(p,e,'Eteo')] / (10/3600)
                self.datos_seg.loc[:,(p,e,'Eteo_U')] = self.datos_seg.loc[:,(p,e,'Eteo')].div(self.datos_seg.loc[:,(p,e,'Pnom')])
                self.datos_seg.loc[:,(p,e,'Pteo_U')] = self.datos_seg.loc[:,(p,e,'Pteo')].div(self.datos_seg.loc[:,(p,e,'Pnom')])
                
                flt = self.datos_seg.loc[:,(p,e,'Pteo')] != 0
                self.datos_seg.loc[flt,(p,e,'PBA')] = self.datos_seg.loc[:,(p,e,'P')].div(self.datos_seg.loc[:,(p,e,'Pteo')])

    def __ordenar_columnas(self,df=None,mensajes=False):
        
        ret = True
        if df is None:
            ret = False
            df = self.datos_seg
        
        #Forzar un reordenamiento de todas las columnas
        columnas_ordenadas = []
        parques_con_datos = df.columns.get_level_values(0).unique()
        for p in parques_con_datos:

            columnas_ordenadas += sorted(df
                .loc[:,(p,'PLANT',slice(None))]
                .columns
                .to_list()
            )

            for a in self.consultar_agrupamientos(nemo_parque=p):
                columnas_ordenadas += sorted(df
                    .loc[:,(p,a,slice(None))]
                    .columns
                    .to_list()
                )
            
            for e in self.consultar_equipos_no_agrupamientos(nemo_parque=p):
                columnas_ordenadas += sorted(df
                    .loc[:,(p,e,slice(None))]
                    .columns
                    .to_list()
                )
        
        if ret:
            return df.loc[:,columnas_ordenadas]
        else:
            self.datos_seg = df.loc[:,columnas_ordenadas]

    def consolidar_todo(self,mensajes=False):
        
        if self.datos_seg is None:
            raise Exception('Imposible consolidar incidencias con datos segundales, si no se cargaron los datos segundales.')
        else:
            if self.__rpt_iec61400_incidencias is None:
                self.interpretar_incidencias_bajo_iec61400()
            self.__consolidar_todo_preparar_df_10s(mensajes=mensajes)       # Crear columnas vacías con datatype booleano, para luego manipular sus datos (FullPerf, Ind y Lim)  

        if self.incidencias_iec61400 is not None:
            #Descargar datos de las incidencias IEC61400 sobre las columnas booleanas
            self.__consolidar_todo_descargar_incidencias(mensajes=mensajes) 
            self.__consolidar_todo_roll_up(mensajes=mensajes)               # Afectar los circuitos y la planta toda, con operaciones lógicas
            self.__ordenar_columnas(mensajes=mensajes)                      # Ajustes finales, ordenar columnas, básicamente
            self.__rpt_consolidado_status = True                            # Indicar que ya se consolidó la información

    def __elaborar_un_rpt_consolidado(self,granularidad='1D',mensajes=False):
     
        # Estas se suman y nada más
        vars_ener = [
            'Econ','Egen','Epos','Eteo','ENS', 
            'ENS_Ind','ENS_IndExt','ENS_IndInt', 
            'ENS_Lim','ENS_LimExt','ENS_LimInt'
        ]

        # Esto son todos promedios
        vars_pot = ['P','Q','Pcon', 'Pgen','Ppos','Pteo',]

        # Estas se pueden sumar o promediar. 
        #   Al sumar hay que multiplicar por (10/3600) para convertir a hs decimales
        #   Al promediar indica el % de tiempo que dicho estado estuvo presente
        vars_tiempo = [
            'Con','Gen','Pos','FullPerf', 
            'Ind','IndExt','IndInt', 
            'Lim','LimExt','LimInt', 
        ]

        # Estas variables hay que explotarlas en categorías booleanas
        # Una vez explotadas en categorías booleanas, sucede lo mismo que con las vars_tiempo
        # Realmente no vale la pela, preferible que el usuario lo aprenda a hacer y lo haga por su cuenta
        vars_cat = ['Wind_dir_r','op_state']

        vars_met = ['Wind','Wind_dir',]
        
        vars_suma = vars_ener + vars_tiempo + ['RegistrosHs']
        vars_prom = vars_met + vars_pot + ['TBA','Datos_%']

        #Filtrar columnas según datos cargados
        t = slice(None)
        cols_prom = self.datos_seg.loc[:,(t,t,vars_prom)].columns.to_list() 
        cols_suma = self.datos_seg.loc[:,(t,t,vars_suma)].columns.to_list()

        df_cons = (self.datos_seg
            .loc[:,cols_prom]
            .resample(granularidad)
            .mean()
            .join(self.datos_seg
                .loc[:,cols_suma]
                .resample(granularidad)
                .sum()
            )
        )

        for v in vars_tiempo:
            df_cons.loc[:,(t,t,v)] = df_cons.loc[:,(t,t,v)] * (10/3600)
        
        # A continuación, se reprocesan variables que sólo se pueden recalcular una vez alcanzado el nuevo nivel de consolidación        
        viento_vel_bins, viento_vel_labels = eo.crear_bins_viento_vel()

        #Devuelve un diccionario con equipo:potencia (en MW)
        for p in self.datos_seg.columns.get_level_values(0).unique():
            dict_equipos = self.consultar_equipos(nemo_parque=p,potencia=True)
            for e in dict_equipos.keys():

                df_cons.loc[:,(p,e,'Pnom')] = dict_equipos[e]*1000
                try:
                    df_cons.loc[:,(p,e,'FC')] = df_cons.loc[:,(p,e,'Egen')] / (df_cons.loc[:,(p,e,'Gen')] * df_cons.loc[:,(p,e,'Pnom')])
                except:
                    pass
                
                try:
                    df_cons.loc[:,(p,e,'PBA')] = df_cons.loc[:,(p,e,'Egen')] / df_cons.loc[:,(p,e,'Eteo')]
                except:
                    pass
                
                try:
                    df_cons.loc[:,(p,e,'PI')] = df_cons.loc[:,(p,e,'Egen')] / df_cons.loc[:,(p,e,'Epos')]
                except:
                    pass

                try:
                    df_cons.loc[:,(p,e,'Wind_bin')] = pd.cut(
                        df_cons.loc[:,(p,e,'Wind')],
                        bins=viento_vel_bins,
                        labels=viento_vel_labels,
                        ordered=True,
                        include_lowest=True
                    )
                except:
                    pass

        return self.__ordenar_columnas(df=df_cons,mensajes=mensajes)

    def __elaborar_un_rpt_consolidado_redux(self,df_cons=None,vars=None,mensajes=False):
        
        if mensajes: print("Creando reducción del reporte consolidado")
        
        # Esto tiene que ser básicamente una selección del rpt consolidado, melteado y listo
        ret = True
        if df_cons is None:
            ret = False
            df_cons = self.__rpt_consolidado
        
        if vars is None:
            vars_ordenadas = [
                'Wind','Wind_dir',
                'TBA','PBA','PI',
                'Egen','Econ','Epos','Eteo','ENS',
                'Gen','Con','Pos','Ind','IndExt','Lim','LimExt',
                'RegistrosHs','Datos_%'
            ]
        else:
            vars_ordenadas = vars

        cols_selec = [c for c in df_cons.columns if c[2] in vars_ordenadas]
        
        df_redux = (df_cons
            .loc[:,cols_selec]
            .melt(ignore_index=False)
            .reset_index()
            .pivot(
                index=['Parque','Equipo','t_stamp'],
                columns=['Variable'],
                values='value'
            )
            .loc[:,vars_ordenadas]
            .reset_index()
            .rename_axis(None,axis=1)
            .rename(columns={'t_stamp':'Fecha'})
        )
        
        df_redux['DispDatosFinal'] = df_redux['RegistrosHs'] * df_redux['Datos_%']
        
        #Agregar campo con Año Operativo
        df_redux['AñoOp'] = 0
        for _, row in df_redux.iterrows():
            df_redux['AñoOp'] = self.consultar_año_op(
                fecha=row['Fecha'],
                nemo_parque=row['Parque']
            )
        
        
        if ret:
            return df_redux.copy(deep=True)
        else:
            self.__rpt_consolidado_redux = df_redux.copy(deep=True)

    def elaborar_reporte_consolidado(self,
                            granularidad='1D',
                            vars=None,
                            mensajes=False,
                            exportar=False,
                            ruta=None,
                            nombre=None
                            ):
        
        if not self.__rpt_consolidado_status:
            self.consolidar_todo(mensajes=mensajes)
        
        get_rpt = lambda g: self.__elaborar_un_rpt_consolidado(granularidad=g,mensajes=mensajes)
        get_rpt_redux = lambda df : self.__elaborar_un_rpt_consolidado_redux(df_cons=df,vars=vars,mensajes=mensajes)
        
        if isinstance(granularidad,str):
            self.__rpt_consolidado = get_rpt(granularidad)
            self.__elaborar_un_rpt_consolidado_redux(vars=vars,mensajes=mensajes)
        elif isinstance(granularidad,(list,tuple)):
            self.__rpt_consolidado = {g:get_rpt(g) for g in granularidad}
            self.__rpt_consolidado_redux = {g:get_rpt_redux(df) for g,df in self.__rpt_consolidado.items()}
        
        #Exportar reporte consolidado
        if exportar:
            #Preparar ruta y nombre de archivo para la exportación
            archivo = self.__exportar_configurar_archivo(encabezado = 'Rpt Consolidado',ruta=ruta,nombre=nombre)
            self.exportar(reportes='consolidado',ruta=str(archivo.parent),nombre=archivo.name)

    #
    # Conjunto de funciones destinadas a crear las curvas de potencia
    # a partir de los reportes consolidados entre 
    # datos 10segundales e incidencias IEC61400
    #
    def __fp(self,p,e,vf):
        # Esta función toma tres parámetros, p, e y v
        # p = parque (str), e = equipo (str) y vf = variable para filtrar (Nombre de columna o serie booleana de pandas) 

        t = slice(None) #Atajo para seleccionar todo en un MultiIndex de pandas
        
        #Varuables de medición encontradas para un parque y elemento dado
        vms_in_df = self.datos_seg.loc[:,(p,e,t)].columns.get_level_values(2)
          
        indice = self.datos_seg.index   # Copia del índice del df por si hay que crear una serie booleana
        n = len(indice)                 #Obtiene la cantidad de filas del df
        
        if vf is None:
            # Si no se ingresó filtro, devuelve una serie con todos valores "True"
            return pd.Series(np.full(n,fill_value=True),index=indice).copy(deep=True)
        
        elif isinstance(vf,pd.Series):
            # Si se ingresó una serie booleana, se devuelve la misma serie
            return vf
        
        elif not vf in vms_in_df:
            print(f"Advertencia: La variable de filtro {vf} no se encontró en las columnas del dataframe datos_seg para {p} {e}. Procediendo sin filtrar")
            return pd.Series(np.full(n,fill_value=True),index=indice).copy(deep=True)
        
        else: 
            return self.datos_seg.loc[:,(p,e,vf)]

    def __vms(self,p,e,vms,vc,mensajes=False):
        # Ingresar a esta función con un parque, un elemento dado y un conjunto de variables de medición deseadas
        # devuelve un tuple: Status, Tuple de filtrado
            # Failed: True si no se encontró ninguna medición. False si se enctró al menos una variable de medición. 
            # Tuple de filtrado, en formato (p,e,vms)
        
        t = slice(None)
        vms_in_df = self.datos_seg.loc[:,(p,e,t)].columns.get_level_values(2).to_list()
        
        if not vc in vms_in_df:
            print(f'{p} {e}  No se encontró la variable categórica {vc} en el dataframe datos_seg. Salteando este equipo.')
            return False , (p,e,[])
        
        # Filtrar variables encontradas (vms_on) y no encontradas (vms_off)
        vms_off = []
        vms_on = []
        for v in vms:
            if v in vms_in_df:
                vms_on.append(v)
            else:
                vms_off.append(v)
        

        if vms_off and vms_on:
            if mensajes: print(f'{p} {e} No se encontraron las siguientes variables: {vms_off}, se descartarán de la elaboración de las curvas de potencia.')
            return False, (p,e,vms_on)
        
        elif not vms_off and vms_on:
            return False, (p,e,vms_on)
        
        elif vms_off and not vms_on:
            if mensajes: print(f'{p} {e} No se encontró ninguna variable para elaborar las curvas de potencia.')
            return True, None
        
        else:
            return True, None

    def _curvas_de_potencia(self,
                df,
                variables_medicion=['Pgen',],
                variable_categorica='Wind_bin',
                variable_filtro='FullPerf',
                aggfunc=np.mean,
                margenes=False,
                mensajes=False,
                ):
        
        # self.__curvas_de_potencia(df,vm,v,vf,'count')
        # Cambio de nombre de variables para reducir el código
        vf = variable_filtro
        vm = variables_medicion
        vc = variable_categorica
        f = aggfunc
        
        lista_dfs = []  # Dataframes con las curvas ya procesadas para parque p, elemento e y variables vm y vc
        
        for p in df.columns.get_level_values(0).unique():
            equipos = self.consultar_equipos_no_agrupamientos(nemo_parque=p)
            for e in equipos:                                                                
                
                failed_status, vms = self.__vms(p,e,vm,vc,mensajes=mensajes) # Verificación de columnas deseadas (vm y vc)
                if failed_status: 
                    continue    #saltearse el equipo actual y continuar con el siguiente equipo posible
                
                vms_vc = (vms[0],vms[1],vms[2] + [vc])          # vls[0] = Parque, vms[1] = Equipo, vms[2] = Variable
                fp = self.__fp(p,e,vf)    # la función __fp devuelve una serie booleana
                                        # fp viene originalmente de 'Full Performance' ya que es el filtro estándar (y más adecuado)
                                        
                # Crear la curva de potencia para el parque p, elemento e, conjunto de variables vms según variable categórica vc
                lista_dfs.append(df
                    .loc[fp,vms_vc]
                    .melt(id_vars=[(p,e,vc)],value_vars=[(p,e,v) for v in vms[2]],ignore_index=False)
                    .reset_index(drop=True)
                    .rename(columns={(p,e,vc):vc})
                    .pivot_table(columns=['Parque','Equipo','Variable'],index=vc,aggfunc=f)
                    .droplevel(level=0,axis='columns')
                )
        
        if not lista_dfs:
            print(f'No se pudo realizar ninguna curva de potencia para {vc} y {vm}')
            return None
        else:
            # Concatenar todos los dataframes de izquierda a derecha, basado en el nuevo índice categórico
            dfm = lista_dfs[0]
            for df in lista_dfs[1:]:
                dfm = pd.merge(
                    left=dfm,
                    right=df,
                    left_index=True,
                    right_index=True,
                    how='outer'
                )
            
            if margenes:
                for p in df.columns.get_level_values(0).unique():
                    for v in vm:
                        dfm.loc[:,(p,'Conteo',v)] = (dfm
                            .loc[:,(p,slice(None),v)]
                            .sum(axis=1)
                        )
                        dfm.loc[:,(p,'Histograma',v)] = (dfm
                            .loc[:,(p,'Conteo',v)]
                            .div(dfm
                                 .loc[:,(p,'Conteo',v)]
                                 .sum()
                            )
                        )
            
            # Reordenar niveles del DataFrame para que queden las variables agrupadas.   
            dfm = (dfm
                .reorder_levels(
                    axis='columns',
                    order=['Parque','Variable','Equipo']
                )
                .sort_index(axis='columns')
            )
                
            if vc == 'Wind_dir_r':
                index_new = pd.Index(eo.rosa_de_los_vientos(bins=16),name='Wind_dir_r')
                dfm = dfm.reindex(index=index_new)
            
            return dfm.copy(deep=True)

    def elaborar_curvas_de_potencia(self,
                            df = None,
                            variables_medicion= ['Pgen','Pteo','Wind','PI'],
                            variables_categoricas= ['Wind_bin','Wind_dir_r'],
                            variable_filtro='FullPerf',
                            filtra_n=0,
                            aggfunc=np.mean,
                            ruta=None,
                            nombre=None,
                            exportar=False,
                            ):
        
        proceder =True
        
        if df is None:
            df = self.datos_seg
        
        if df.empty:
            print(f"Imposible realizar curvas de potencia sin datos")
            proceder = False
            
        if not self.__rpt_consolidado_status:
            print(f"Advertencia: intentando realizar curvas de potencia sin haber consolidado las incidencias y los datos segundales.")
            variable_filtro = None

        if proceder:
            vm = variables_medicion         # Conjunto de variables de medición, las cuales se quiere categorizar
            vc = variables_categoricas      # Vcs = Variables categóricas. Por cada variable categórica, se creará un dataframe con todas las variables de medición
            vf = variable_filtro            # Variable (Serie booleana) por la cual se filtrarán los datos crudos, previo a categorizar
            n = filtra_n                    # Sólo considera registros con un conteo >= n
            f = aggfunc                     # Variable de agregación, sobre las varaibles de medicion (suma, promedio, etc.)
            

            # Crea un diccionario del tipo 'VariableCategórica':df_curvas_de_potencia
            dict_dfs_val = {v:self._curvas_de_potencia(df,vm,v,vf,f,False) for v in vc}          
            dict_dfs_count = {v:self._curvas_de_potencia(df,vm,v,vf,'count',True) for v in vc}
            
            # En caso de que haya algún resultado sin curvas de potencia, descartar
            dict_dfs_val = {k:v for k,v in dict_dfs_val.items() if not v is None}           
            dict_dfs_count = {k:v for k,v in dict_dfs_count.items() if not v is None}

            dict_dfs = {}
            
            for k in dict_dfs_val.keys():
                dfv = dict_dfs_val[k]
                dfc = dict_dfs_count[k]
                flt = dfc >= n
                dict_dfs[k] = dfv[flt]
                dict_dfs[k+'_count'] = dfc
            

            if len(dict_dfs) > 1:
                self.__rpt_curvas_de_potencia = dict_dfs
            else:
                self.__rpt_curvas_de_potencia = None
            
            if exportar:
                #Preparar ruta y nombre de archivo para la exportación
                archivo = self.__exportar_configurar_archivo(encabezado = 'Curvas de Potencia',ruta=ruta,nombre=nombre)
                self.exportar(reportes='curvas',ruta=str(archivo.parent),nombre=archivo.name)

    #
    # Conjunto de reportes de resumen, en base a las incidencias
    #
    def elaborar_resumen_diario_incidencias(self,explotar_e_interpretar=False,):
        
        if explotar_e_interpretar or (self.incidencias_iec61400 is None):
            self.explotar_incidencias(iec6100=True)
            
        df = self.incidencias_explotadas

        cols_group = [
            'Nemo','Equipo',
            self.incidencias_iec61400.Start.dt.date,
            'Origin','Reason']
        
        cols_orig = [
            'Nemo','Equipo_Orig',
            self.incidencias_iec61400.Start.dt.date,
            'Origin','Reason']
        
        df_ENS = pd.merge(
            left= df
                .groupby(cols_group)
                ['ENS']
                .sum()
                .rename_axis(['Nemo','Equipo','Fecha','Origin','Reason',])
                .rename('ENS_IEC61400'),
            right = df
                .groupby(cols_orig)
                ['ENS']
                .sum()
                .rename_axis(['Nemo','Equipo','Fecha','Origin','Reason',])
                .rename('ENS_Equipo_Orig'),
            left_index=True,
            right_index=True,
            how='outer')

        df_Hours = pd.merge(
            left= df
                .loc[~df
                     .duplicated(
                            subset=['Equipo_Orig','Start','End'],
                            keep='first'
                    )
                    ,:]
                .groupby(cols_orig)
                ['Hours']
                .sum()
                .rename_axis(['Nemo','Equipo','Fecha','Origin','Reason',])
                .rename('Hours_Equipo_Orig'),
            right = df
                .groupby(cols_group)
                ['Hours']
                .sum()
                .rename_axis(['Nemo','Equipo','Fecha','Origin','Reason',])
                .rename('Hours_IEC61400'),
            left_index=True,
            right_index=True,
            how='outer')

        self.__rpt_incidencias_resumen_diario = (pd
            .merge(
                left=df_ENS,
                right=df_Hours,
                left_index=True,
                right_index=True,
                how='outer',)
            .reset_index()
        )

    #
    # Conjunto de funciones destinadas a exportar datos 
    # 
    def __exportar_configurar_archivo(self,encabezado=None,ruta=None,nombre=None):
        #Configurar nombre del archivo
        if nombre is None:
            fecha_str = dt.datetime.now().strftime("%Y-%m-%d %H.%M.%S")
            fecha_i_str = self.fecha_i.strftime("%Y-%m-%d")
            fecha_f_str = self.fecha_f.strftime("%Y-%m-%d")
            fechas = f'{fecha_i_str} a {fecha_f_str} {fecha_str}'
            
            if len(self.parques) > 1 or not self.parques:
                nombre_rpt = f'{encabezado} {fechas}.xlsx'
            else:
                nombre_rpt = f'{encabezado} {fechas} {self.parques[0]}.xlsx'
        else:
            if not nombre.lower().endswith('.xlsx'):
                nombre_rpt = nombre + '.xlsx'
            else:
                nombre_rpt = nombre
        
        #Configurar ruta de salida
        if not ruta:
            ruta = self.dir_salida
        else:
            ruta = dirs.check_dir(ruta)
        
        return Path(ruta + '\\' + nombre_rpt)

    def __exportar_check_texto_reportes(self,reporte):
       
        valores_posibles = [
            'todos',
            'incidencias',
            'incidencias_crudas',
            'incidencias_redux',
            'incidencias_iec61400',
            'incidencias_explotadas',
            'incidencias_autodetectadas',
            'incidencias_resumen_diario',
            'consolidado',
            'curvas'
        ]
        
        # Chequear que
        if isinstance(reporte,str):
            reporte = reporte.lower()
            if reporte in valores_posibles:
                return reporte
            else:
                raise ValueError(f'El parámetro reportes es <{reporte}> y se esperaba alguno entre {valores_posibles}')

    def __exportar_check_reportes_seleccionados(self,reportes):
        
        #Chequear DataType del parámetro ingresado
        if not isinstance(reportes,(str,list,tuple)):
            raise TypeError('El parámetro "reportes" debe ser del tipo str, lista o tuple')
        
        #Ya sabemos que reportes es str,list o tuple
        if isinstance(reportes,str):
            return [self.__exportar_check_texto_reportes(reportes)]
        else:
            return [self.__exportar_check_texto_reportes(r) for r in reportes]

    def exportar(self,reportes='todos',ruta=None,nombre=None):
        
        # Validación del parámetro de entrada
        # Convierte a lista la variable, incluso si la entrada fue un string, queda como ['todos'] (por ejemplo)
        reportes = self.__exportar_check_reportes_seleccionados(reportes)
        
        # Chequeo de que las palabras claves se encuentre contenidas en la lista 'Reportes'
        todos = 'todos' in reportes
        consolidado = todos or ('consolidado' in reportes)
        curvas = todos or 'curvas' in reportes
        incidencias_todas = todos or ('incidencias' in reportes)
        incidencias_crudas = todos or incidencias_todas or ('incidencias_crudas' in reportes)
        incidencias_redux = todos or incidencias_todas or ('incidencias_redux' in reportes)
        incidencias_explotadas = todos or incidencias_todas or ('incidencias_explotadas' in reportes)
        incidencias_iec61400 = todos or incidencias_todas or ('incidencias_iec61400' in reportes)
        incidencias_autodetectadas = todos or incidencias_todas or ('incidencias_autodetectadas' in reportes)
        incidencias_resumen_diario = todos or incidencias_todas or ('incidencias_resumen_diario' in reportes)
        
        # Flags para chequear que cada uno de los reportes tiene datos efectivamente
        # Si alguno está sin datos, simplemente se lo va a saltear
        tiene_datos_consolidado = self.consolidado is not None
        tiene_datos_curvas = self.curvas_de_potencia is not None
        tiene_datos_inc_cru = self.incidencias is not None
        tiene_datos_inc_red = self.incidencias_redux is not None
        tiene_datos_inc_exp = self.incidencias_explotadas is not None
        tiene_datos_inc_iec = self.incidencias_iec61400 is not None
        tiene_datos_inc_aut = self.incidencias_autodetectadas is not None
        tiene_datos_resumen = self.incidencias_resumen_diario is not None
        
        # Flags que se utilizan al momento de decidir si un reporte se exporta a excel o no.
        exp_rpt_consolidado =  consolidado and tiene_datos_consolidado
        exp_rpt_curvas_de_potencia = curvas and tiene_datos_curvas
        exp_incidencias_crudas = incidencias_crudas and tiene_datos_inc_cru
        exp_incidencias_redux = incidencias_redux and tiene_datos_inc_red
        exp_incidencias_explotadas = incidencias_explotadas and tiene_datos_inc_exp
        exp_incidencias_iec61400 = incidencias_iec61400 and tiene_datos_inc_iec
        exp_incidencias_autodetectadas = incidencias_autodetectadas and tiene_datos_inc_aut
        exp_incidencias_resumen_diario = incidencias_resumen_diario and tiene_datos_resumen
        
        # Hay casos donde puede haber dataframes vacíos
        # Segunda iteración sobre dichas flags
        try:
            if exp_rpt_consolidado: exp_rpt_consolidado = not self.consolidado.empty
        except:
            pass
        try:
            if exp_rpt_curvas_de_potencia: exp_rpt_curvas_de_potencia = not self.curvas_de_potencia.empty
        except:
            pass
        try:
            if exp_incidencias_crudas: exp_incidencias_crudas = not self.incidencias.empty
        except:
            pass
        try:
            if exp_incidencias_redux: exp_incidencias_redux = not self.incidencias_redux.empty
        except:
            pass
        try:
            if exp_incidencias_explotadas: exp_incidencias_explotadas = not self.incidencias_explotadas.empty
        except:
            pass
        try:
            if exp_incidencias_iec61400: exp_incidencias_iec61400 = not self.incidencias_iec61400.empty
        except:
            pass
        try:
            if exp_incidencias_autodetectadas: exp_incidencias_autodetectadas = not self.incidencias_autodetectadas.empty
        except:
            pass
        try:
            if exp_incidencias_resumen_diario: exp_incidencias_resumen_diario = not self.incidencias_autodetectadas.empty
        except:
            pass
            
        # Preparar ruta y nombre de archivo para la exportación
        archivo = self.__exportar_configurar_archivo(encabezado = 'Reportes blctools', ruta=ruta, nombre=nombre)
        
        # Rutina de exportación
        with pd.ExcelWriter(archivo) as w:
            if exp_incidencias_crudas: 
                self.incidencias.to_excel(
                    w,
                    sheet_name='Inc_Crudas',
                    index=False,
                    freeze_panes=(1,0),
                    inf_rep='')
                
            if exp_incidencias_redux: 
                self.incidencias_redux.to_excel(
                    w,
                    sheet_name='Inc_Redux',
                    index=False,
                    freeze_panes=(1,0),
                    inf_rep='')
                
            if exp_incidencias_explotadas: 
                self.incidencias_explotadas.to_excel(
                    w,
                    sheet_name='Inc_Expl',
                    index=False,
                    freeze_panes=(1,0),
                    inf_rep='')
                
            if exp_incidencias_iec61400: 
                self.incidencias_iec61400.to_excel(
                    w,
                    sheet_name='Inc_IEC61400',
                    index=False,
                    freeze_panes=(1,0),
                    inf_rep='')
            
            if exp_incidencias_autodetectadas:
                self.incidencias_autodetectadas.to_excel(
                    w,
                    sheet_name='Inc_Autodetectadas',
                    index=False,
                    freeze_panes=(1,0),
                    inf_rep='')
                
            if exp_incidencias_resumen_diario:
                self.incidencias_resumen_diario.to_excel(
                    w,
                    sheet_name='Inc_Resumen_Diario',
                    index=False,
                    freeze_panes=(1,3),)
                
            if exp_rpt_consolidado: 
                #RPT consolidado completo
                if isinstance(self.consolidado,pd.DataFrame):
                    self.consolidado.to_excel(
                        w,
                        sheet_name='Consolidado',
                        merge_cells=False,
                        freeze_panes=(1,1),
                        inf_rep='')
                else:
                    for g,df in self.consolidado.items():
                        df.to_excel(
                            w,
                            sheet_name=f'Consolidado_{g}',
                            merge_cells=False,
                            freeze_panes=(1,1),
                            inf_rep='')
                        
                #RPT consolidado reducido
                if isinstance(self.consolidado_redux,pd.DataFrame):
                    self.consolidado_redux.to_excel(
                        w,
                        sheet_name='Consolidado_Redux',
                        index=False,
                        merge_cells=False,
                        freeze_panes=(1,3),
                        inf_rep='')
                else:
                    for g,df in self.consolidado_redux.items():
                        df.to_excel(
                            w,
                            sheet_name=f'Consolidado_Redux_{g}',
                            index=False,
                            merge_cells=False,
                            freeze_panes=(1,3),
                            inf_rep='')
            
            if exp_rpt_curvas_de_potencia: 
                if isinstance(self.curvas_de_potencia,pd.DataFrame):
                    self.__rpt_curvas_de_potencia.to_excel(
                        w,
                        sheet_name='Curvas',
                        merge_cells=False,
                        freeze_panes=(1,1),
                        inf_rep='')
                else:
                    for vc,df in self.curvas_de_potencia.items():
                        df.to_excel(
                            w,
                            sheet_name=f'Curvas_{vc}',
                            merge_cells=False,
                            freeze_panes=(1,1),
                            inf_rep='')
