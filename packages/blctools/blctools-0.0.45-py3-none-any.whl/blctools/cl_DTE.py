from . import dirs
from . import fechas

from .cl_ReporteBase import *
from .cl_BCRA import *

__all__ = ['DTE',]

class DTE(ReporteBase,BCRA):

    def __init__(
        self,
        fecha_i = fechas.ayer(),
        fecha_f = fechas.ayer(),
        cargar = False,
        descargar = False,
        cols_usd = None,
        periodo = None,
        filtro = 'ultimos',
        parques = [],
        tabla_datos = 'Q_RepItems',
        col_filtro = 'NEMO',
        dir_salida = dirs.raiz,
        ):

        dir_descarga, dir_extraccion = self.__elegir_dirs(filtro=None)

        ReporteBase.__init__(self,
            fecha_i = fecha_i,
            fecha_f = fecha_f,
            periodo=periodo,
            nemo_rpt = 'DTE_UNIF',
            nombre = 'DTE',
            formato_nombre_archivo = 'DTE%y%m',
            parques = parques,
            extension = 'mdb',
            tabla_datos = tabla_datos,
            tabla_fecha = 'VALORES_PERIODO',
            col_filtro = col_filtro,
            dir_salida = dir_salida,
            dir_descarga = dir_descarga,
            dir_extraccion = dir_extraccion,
            funcion_archivos_necesarios = fechas.iterar_mensual,
            valores_custom_filtro= {'finales':self.__filtrar_dtes_finales}
            )
        
        BCRA.__init__(self,
            cargar_tc = False,
            cargar_rem = False 
            )
        
        self.filtro = filtro
        self.cols_usd = cols_usd        

        if cargar:
            self.cargar(descargar=descargar, filtro=filtro, exportar_consulta=False)
            
        if not cargar and descargar:
            self.descargar(filtro=filtro)
        
    #--------------------------
    #
    #Fin de la función __init__
    #
    #--------------------------
    def __filtrar_dtes_finales(self,df):
        #Toma un dataframe resultante de la funcion cl_ApiCammesa.ApiCammesa.consultar()
        flt = df['titulo'].str.upper().str.startswith('DTE EMISIÓN 08/')
        return df[~flt]
    
    def __get_dirs(self,funcion):
        try:
            dir_descarga = funcion() + '\\00 ZIP'
        except: 
            dir_descarga = dirs.raiz + '\\00 ZIP'

        try:
            dir_extraccion = funcion() + '\\01 MDB'
        except:
            dir_extraccion = dirs.raiz + '\\01 MDB'
            
        return dir_descarga, dir_extraccion
    
    def __elegir_dirs(self,filtro=None):
        
        if filtro is None or filtro =='ultimos':
            dir_descarga, dir_extraccion = self.__get_dirs(dirs.get_dc_dte)
                    
        elif filtro == 'iniciales':
            dir_descarga, dir_extraccion = self.__get_dirs(dirs.get_dc_dtei)
                    
        elif filtro == 'finales':
            dir_descarga, dir_extraccion = self.__get_dirs(dirs.get_dc_dtef)
        else:
            dir_descarga    = dirs.raiz + '\\00 ZIP'
            dir_extraccion  = dirs.raiz + '\\01 MDB'
            
        return  dir_descarga, dir_extraccion
    
    @property
    def filtro(self):
        return self._filtro
    
    @filtro.setter
    def filtro(self,val):
        if val != False:
            self._filtro = self.check_filtro(val)
            self.dir_descarga, self.dir_extraccion = self.__elegir_dirs(self.filtro)
            self._actualizar_archivos()

    @property
    def cols_usd(self):
        return self._cols_usd
    
    @cols_usd.setter
    def cols_usd(self,val):
        
        if isinstance(val,str):
            self._cols_usd = [val,]
        elif isinstance(val,(list,tuple,set)):
            if all(map(lambda x: isinstance(x,str),val)):
                self._cols_usd = val
            else:
                raise TypeError('Todos los elementos del iterable "dolarizar" deben ser del tipo string.')
        elif val is None:
            self._cols_usd = None
        else:
            raise TypeError('dolarizar debe ser string (para una columna) o lista, tuple o set de strings, para un conjunto de columnas')

    # Agregado de funcionalidades a funciones de la clase superior
    def consultar(self,exportar_consulta=False,dir_consulta=None,filtro=None):
        
        if filtro is not None:
            self.filtro = filtro
        
        ReporteBase.consultar(self,
            exportar_consulta=exportar_consulta,
            dir_consulta=dir_consulta,
            filtro=self.filtro
            ) 
    
    def descargar(self,exportar_consulta=False,dir_consulta=None,filtro=None):
        
        if filtro is not None:
            self.filtro = filtro
        
        ReporteBase.descargar(self,
            exportar_consulta=exportar_consulta,
            dir_consulta=dir_consulta,
            filtro=self.filtro
            ) 
        
    def cargar(self,descargar=False,filtro=None,exportar_consulta=False):
        
        if filtro is not None:
            self.filtro = filtro
        
        ReporteBase.cargar(self,
            descargar=descargar,
            filtro=self.filtro,
            exportar_consulta=exportar_consulta
            )
        
        if self.cols_usd is not None:
            self.dolarizar()

    def dolarizar(self):

        #Chequeo de columnas
        cols_na = list(filter(
                lambda x: x not in self.datos.columns,
                self.cols_usd
                )
            )
        if cols_na:
            raise ValueError(f'No se encontró/encontraron la(s) columna(s) {cols_na} entre {self.datos.columns.to_list()}')

        # Obtener tipo de cambio BCRA
        self.cargar_tc_ultimo_dia_habil()

        #Chequeo de que se pudo cargar el tipo de cambio
        if self.tc_udh.empty:
            print('Se procederá a la carga del DTE sin dolarizar, por falta del dato del Tipo de Cambio.')
        else:
            self.datos = (self.datos
                .rename(columns={'TC':'Tecnologia'})   #Hay algunas tablas de CAMMESA que dicen "TC" por "Tipo de Tecnología"
                .merge(
                    right=self.tc_udh, 
                    left_on='Fecha', 
                    right_index=True, 
                    how='left')
                .assign(**{f'{c}_USD':lambda df_, c=c: df_[c].div(df_.TC) for c in self.cols_usd})
                .rename(columns={c:f'{c}_ARS' for c in self.cols_usd})
            )
    
    def a_excel(self,descargar=False,filtro=None,exportar_consulta=False):
        
        if filtro is not None:
            self.filtro = filtro
        
        ReporteBase.a_excel(self,
            descargar=descargar,
            filtro=self.filtro,
            exportar_consulta=exportar_consulta
            )