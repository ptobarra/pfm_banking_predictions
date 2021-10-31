from datetime import datetime

import pandas
from pandas import date_range, DatetimeIndex, DataFrame, to_numeric

# from pandas import read_excel

"""
Pedro Tobarra 20210907:
Modificación del notebook '20210630 seguro_vehiculo_78_v01_def.ipynb' para meter el código en una función 
de python que luego pueda ser implementada en un fichero '.py' para su integración con el backend del PFM
"""


def seguro_vehiculo_78(transacciones_df, balance_df):
    # nos quedamos con la fecha en que nos dan los datos de las transacciones
    balance_date_str = str(balance_df.iloc[0]['BALANCE_DATE'])
    last_date_tstamp = pandas.to_datetime(balance_date_str, yearfirst=True)

    # nos quedamos con las transacciones de la categoría 'seguro_vehiculo_78'
    transacciones_78_df = transacciones_df[transacciones_df['ID Categoría'] == 78.0]
    del transacciones_df

    # nos quedamos con categoría desde 'Fecha transacción' hasta 'Importe'
    transacciones_78_df = transacciones_78_df.iloc[:, 0:2]

    # renombramos columnas
    transacciones_78_df.rename(columns={'Fecha transacción': 'FECHA', 'Importe': 'IMPORTE'}, inplace=True)

    # ordenamos las fechas por orden ascendente
    transacciones_78_df.sort_values(by=['FECHA'], ascending=True, inplace=True, ignore_index=True)

    # vamos a agrupar los valores y sumarlos por fecha para agrupar cargos distintos realizados el mismo dia
    # (por si acaso)
    transacciones_78_df = transacciones_78_df.groupby(['FECHA']).sum()

    # para que los datos sean más fáciles de interpretar vamos a hacerlos todos positivos multiplicándolos por '-1'
    transacciones_78_df['IMPORTE'] = -transacciones_78_df['IMPORTE']

    # EMPEZAMOS POR HACER EL DATAFRAME DE LOS IMPORTES
    # vamos a rellenar las missing dates con el ultimo valor válido
    transacciones_78_importe_df = transacciones_78_df.copy()

    # hacemos una columna con la fecha del indice
    transacciones_78_importe_df['FECHA'] = transacciones_78_importe_df.index

    idx = date_range(start=transacciones_78_importe_df.FECHA.min(), end=transacciones_78_importe_df.FECHA.max())

    # pasamos el indice de transacciones_78_importe_df a formato DatetimeIndex
    transacciones_78_importe_df.index = DatetimeIndex(transacciones_78_importe_df.index)

    # rellenamos las missing dates en el indice
    transacciones_78_importe_df = transacciones_78_importe_df.reindex(idx, fill_value='NaN')

    # hacemos drop de la columna FECHA
    transacciones_78_importe_df.drop(columns='FECHA', inplace=True)

    # pasamos IMPORTE a formato 'numeric'
    transacciones_78_importe_ser = transacciones_78_importe_df.T.squeeze()
    transacciones_78_importe_ser = to_numeric(transacciones_78_importe_ser, errors='coerce')
    transacciones_78_importe_df = DataFrame(transacciones_78_importe_ser)
    del transacciones_78_importe_ser

    # rellenamos los NaN con el ultimo valor numérico anterior
    transacciones_78_importe_df['IMPORTE'].fillna(method='ffill', inplace=True)

    # HACEMOS EL DATAFRAME DEL DIA DE PAGO DEL SEGURO DEL COCHE HASTA EL AÑO SIGUIENTE AL DE LAST_DATE_TSTAMP

    # extendemos dataframe del dia de pago del seguro hasta 1 año después de la fecha de la ultima transacción en
    # cuenta
    target_year = 1 + last_date_tstamp.year

    # hacemos la diferencia entre target_year y transacciones_78_importe_past_df.iloc[-1]['FECHA'].year para saber
    # cuantos años tenemos q extender el dataframe anterior
    numberOf_future_years = target_year - transacciones_78_df.index[-1].year

    # transacciones_78_forecast_df sera el dataframe donde guardaremos las futuras fechas de cobro (y las pasadas
    # reales)
    transacciones_78_forecast_df = transacciones_78_df.copy()

    while numberOf_future_years > 0:
        # calculo el 1er y ultimo dia del ultimo año
        start_date_dtime = datetime(transacciones_78_forecast_df.index[-1].year, 1, 1)
        end_date_dtime = datetime(transacciones_78_forecast_df.index[-1].year, 12, 31)

        # convertimos de date a datetime la columna index de transacciones_78_forecast_df
        transacciones_78_forecast_df.index = pandas.to_datetime(transacciones_78_forecast_df.index)

        # construyo la condición para seleccionar las fechas entre el 1er y ultimo dia del ultimo año
        after_start_date = transacciones_78_forecast_df.index >= start_date_dtime
        before_end_date = transacciones_78_forecast_df.index <= end_date_dtime
        between_two_dates = after_start_date & before_end_date

        # construyo un dataframe solo con las fechas del ultimo año
        transacciones_78_nextYear_df = transacciones_78_forecast_df.loc[between_two_dates]

        # añadimos 1 año al indice
        transacciones_78_nextYear_df.index += pandas.offsets.DateOffset(years=1)

        # añadimos las filas de transacciones_78_nextYear_df a las de transacciones_78_forecast_df
        transacciones_78_forecast_df = transacciones_78_forecast_df.append(transacciones_78_nextYear_df)

        # decrementamos el contador de años futuros
        numberOf_future_years -= 1

        # borramos el dataframe q tiene solo las transacciones del ultimo año
        del transacciones_78_nextYear_df

    # con el dataframe 'transacciones_78_forecast_df' ya tenemos estimados el importe y las fechas de cobro
    # mediante la 'cuenta de la vieja'

    # A CONTINUACIÓN CON LOS DATOS ANTERIORES VAMOS A HACER LA PARTE DEL ALGORITMO QUE HACE LAS PREDICCIONES
    # pedimos la fecha al usuario --> en producción se tomará la fecha del sistema
    """
    year = 2020
    month = 7    
    day = 28
    
    # pasamos la fecha a string
    system_date_str = str(year) + '-' + str(month) + '-' + str(day)     

    # pasamos la fecha al formato datetime
    system_date_obj = datetime.strptime(system_date_str, '%Y-%m-%d')
    """

    # tomamos la fecha del sistema del excel que nos han dado --> --> en producción se tomará la fecha del sistema
    system_date_obj = last_date_tstamp
    system_date_str = system_date_obj.strftime('%Y-%m-%d')

    # en transacciones_78_forecast_df tenemos la fecha de los próximos recibos y su importe (proyectados del
    # pasado) hasta 1 año después de la fecha del sistema

    # hacemos un bucle desde la fecha del sistema; incrementándola hasta que encontremos la fecha del próximo
    # recibo en el indice transacciones_78_forecast_df

    # calculamos el rango de fechas del bucle for para buscar las fechas de los próximos recibos
    idx = date_range(start=system_date_obj, end=transacciones_78_forecast_df.index.max())

    # inicializamos la variable de la fecha del próximo recibo
    next_bill_date_obj = system_date_obj

    # buscamos la fecha del próximo recibo
    for date_obj in idx:
        if date_obj in transacciones_78_forecast_df.index:
            next_bill_date_obj = date_obj
            break

    # obtenemos el importe del recibo del dataframe transacciones_78_forecast_df para next_bill_date_obj
    next_bill_amount = float(transacciones_78_forecast_df.loc[next_bill_date_obj, 'IMPORTE'])

    # chequeamos si la fecha del próximo recibo está en el mes siguiente al de la petición para dar aviso
    next_month_bool = False
    if next_bill_date_obj.month - system_date_obj.month == 1:
        next_month_bool = True

    # chequeamos si hay un recibo el mismo dia (+/- 3 dias) y cantidad next_bill_date_obj en transacciones_78_df
    # y si la diferencia entre next_bill_date_obj y esta fecha encontrada es igual o menor a 1 año para dar la
    # predicción como real
    last_year_bool = False
    last_bill_date_obj = None

    if next_bill_amount in transacciones_78_df['IMPORTE'].tolist():
        last_bill_date_obj = max(transacciones_78_df.index[transacciones_78_df['IMPORTE'] ==
                                                           next_bill_amount].tolist())
        if abs(next_bill_date_obj.day - last_bill_date_obj.day) <= 3 & \
                next_bill_date_obj.year - last_bill_date_obj.year <= 1:
            last_year_bool = True

    mensaje1_str = 'Fecha sistema:\t\t\t\t\t\t\t\t ' + system_date_str
    next_bill_date_str = next_bill_date_obj.strftime('%Y-%m-%d')
    mensaje2_str = 'Fecha próximo recibo:\t\t\t\t\t\t ' + next_bill_date_str
    last_bill_date_str = last_bill_date_obj.strftime('%Y-%m-%d')
    # convertimos last_bill_date_obj de 'date' a 'datetime'
    last_bill_date_obj = pandas.to_datetime(last_bill_date_obj)
    mensaje3_str = 'Fecha último recibo equivalente (mismo importe): ' + last_bill_date_str
    mensaje4_str = 'Importe próximo recibo (proyectado):\t\t ' + str(int(next_bill_amount)) + ' eur'
    mensaje5_str = 'Aviso recibo real (anterior en último año):\t ' + str(last_year_bool)
    mensaje6_str = 'Aviso recibo mes siguiente:\t\t\t\t\t ' + str(next_month_bool)
    next_month_def_bool = last_year_bool & next_month_bool
    mensaje7_str = 'Aviso definitivo recibo mes siguiente\t\t ' + str(last_year_bool & next_month_bool)

    return system_date_obj, mensaje1_str, next_bill_date_obj, mensaje2_str, last_bill_date_obj, mensaje3_str, \
        next_bill_amount, mensaje4_str, last_year_bool, mensaje5_str, next_month_bool, mensaje6_str, \
        next_month_def_bool, mensaje7_str


"""
# Load data using read_excel
transacciones_orig_df = read_excel('./scripts_jupyter/20210513 mmelero (249236).xlsx', sheet_name='Hoja1')

system_date, mensaje1, next_bill_date, mensaje2, last_bill_date, mensaje3, next_bill_amount_float, mensaje4, \
    last_year_b, mensaje5, next_month_b, mensaje6, next_month_def_b, mensaje7 = \
    seguro_vehiculo_78(transacciones_orig_df)

# print()
print(system_date)
print(mensaje1)
print(next_bill_date)
print(mensaje2)
print(last_bill_date)
print(mensaje3)
print(next_bill_amount_float)
print(mensaje4)
print(last_year_b)
print(mensaje5)
print(next_month_b)
print(mensaje6)
print(next_month_def_b)
print(mensaje7)
"""
