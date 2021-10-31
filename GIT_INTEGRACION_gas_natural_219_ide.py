import calendar
import statistics
from datetime import datetime, timedelta

import dateutil.relativedelta
import pandas
from prophet import Prophet
from pandas import date_range, DatetimeIndex, DataFrame, to_numeric, to_datetime
# from pandas import read_excel
from pandas.tseries.offsets import DateOffset

"""
Pedro Tobarra 20210816:
Modificación del notebook '20210624 gas_natural_219.ipynb' para meter el código en una función de python que luego pueda
ser implementada en un fichero '.py' para su integración con el backend del PFM
"""


def gas_natural_219(transacciones_df):
    # nos quedamos con categoría desde 'Fecha transacción' hasta 'Nombre Categoría'
    transacciones_df = transacciones_df.iloc[:, 0:4]

    # nos quedamos con las transacciones de la categoría 'gas_natural_129'
    transacciones_219_df = transacciones_df[transacciones_df['ID Categoría'] == 219.0]
    del transacciones_df

    # quitamos las columnas de 'ID Categoría' y 'Nombre Categoría' que ya no nos aportan nada
    transacciones_219_df = transacciones_219_df.drop(columns=['ID Categoría', 'Nombre de categoría'], inplace=False)

    # renombramos columnas
    transacciones_219_df = transacciones_219_df.rename(columns={'Fecha transacción': 'FECHA', 'Importe': 'IMPORTE'},
                                                       inplace=False)

    # ordenamos las fechas por orden ascendente
    transacciones_219_df = transacciones_219_df.sort_values(by=['FECHA'], ascending=True, inplace=False,
                                                            ignore_index=True)

    # vamos a agrupar los valores y sumarlos por fecha para agrupar cargos distintos realizados el mismo dia
    transacciones_219_df = transacciones_219_df.groupby(['FECHA']).sum()

    # Al igual que hicimos en el caso de la serie temporal del seguro medico y de la liquidación de la tarjeta,
    # vamos a rellenar las missing dates con el ultimo valor válido y comprobar si esa serie temporal es modelable y
    # predecible
    transacciones_219_importe_df = transacciones_219_df.copy()
    transacciones_219_importe_df['FECHA'] = transacciones_219_importe_df.index

    idx = date_range(start=transacciones_219_importe_df.FECHA.min(), end=transacciones_219_importe_df.FECHA.max())

    transacciones_219_importe_df.index = DatetimeIndex(transacciones_219_importe_df.index)
    transacciones_219_importe_df = transacciones_219_importe_df.reindex(idx, fill_value='NaN')
    transacciones_219_importe_df.drop(columns='FECHA', inplace=True)

    transacciones_219_importe_ser = transacciones_219_importe_df.T.squeeze()
    transacciones_219_importe_ser = to_numeric(transacciones_219_importe_ser, errors='coerce')
    transacciones_219_importe_df = DataFrame(transacciones_219_importe_ser)
    del transacciones_219_importe_ser

    # rellenamos los NaN con el ultimo valor numérico anterior
    transacciones_219_importe_df['IMPORTE'].fillna(method='ffill', inplace=True)

    # para que los datos sean más fáciles de interpretar vamos a hacerlos todos positivos multiplicándolos por '-1'
    transacciones_219_importe_df['IMPORTE'] = -transacciones_219_importe_df['IMPORTE']

    # HACEMOS EL DATAFRAME DEL DIA DE PAGO DEL SEGURO MEDICO
    transacciones_219_df_dia = transacciones_219_df.copy()

    # hacemos una columna con la fecha a partir del índice
    transacciones_219_df_dia['FECHA'] = transacciones_219_df_dia.index
    transacciones_219_df_dia['FECHA'] = pandas.to_datetime(transacciones_219_df_dia['FECHA'])

    # hacemos una columna con el dia a partir de la columna de la fecha
    transacciones_219_df_dia['DIA'] = transacciones_219_df_dia['FECHA'].dt.day

    # calculamos la moda - tomaremos la moda como el dia de cobro mas habitual
    stat_mode_dist = statistics.mode(transacciones_219_df_dia['DIA'])

    # extraemos el 1er cuartil
    quartil1_dist = int(transacciones_219_df_dia.describe().loc['25%']['DIA'])

    # extraemos el 3er cuartil
    quartil3_dist = int(transacciones_219_df_dia.describe().loc['75%']['DIA'])

    # calculamos el rango intercuartílico
    iqr_dist = quartil3_dist - quartil1_dist

    # calculo de iqr: si NO pasan recibo a FIN DE MES
    if stat_mode_dist < 28:
        iqr = iqr_dist
    # calculo de iqr: si SÍ pasan recibo a FIN DE MES
    else:
        # si quartil3_dist - quartil1_dist es mayor a 4 dias
        if iqr_dist > 4:
            iqr = 4
        else:
            iqr = iqr_dist

    # pedimos al usuario la fecha (en producción tomamos la fecha del sistema)
    #     year = input('year: ')
    #     month = input('month: ')
    #     day = input('day: ')
    year = str(2019)
    month = str(6)
    day = str(20)

    # pasamos la fecha a string
    current_date_str = year + '-' + month + '-' + day

    # pasamos la fecha al formato datetime
    current_date_obj = datetime.strptime(current_date_str, '%Y-%m-%d')

    # pasamos iqr a formato datetime
    iqr_obj = timedelta(days=iqr)

    # sumamos 1 mes a current_date_obj ya que vamos a calcular fecha e importe del recibo al mes siguiente al que se lo
    # pedimos
    target_date_obj = current_date_obj + DateOffset(months=1)

    # calculamos quartil3_obj en función de current_date_obj, quartil3_dist y si pasan el recibo a FIN de MES o NO
    # si SÍ pasan recibo a FIN de MES
    if stat_mode_dist >= 28:
        # quartil3_obj sera el ultimo dia del mes de target_date_obj
        quartil3 = calendar.monthrange(target_date_obj.year, target_date_obj.month)[1]
        quartil3_str = str(target_date_obj.year) + '-' + str(target_date_obj.month) + '-' + str(quartil3)
    # si NO pasan recibo a FIN de MES
    else:
        quartil3_str = str(target_date_obj.year) + '-' + str(target_date_obj.month) + '-' + str(quartil3_dist)

    q3_obj = datetime.strptime(quartil3_str, '%Y-%m-%d')
    q1_obj = q3_obj - iqr_obj

    # para que el pycharm no de problemas
    stat_mode_str = ''

    # calculamos la moda con año, mes y dia
    if (quartil3_dist - stat_mode_dist) >= 0:
        # print('la moda esta en el mismo mes y año q quartil3_dist')
        stat_mode_str = str(q3_obj.year) + '-' + str(q3_obj.month) + '-' + str(stat_mode_dist)
    elif (stat_mode_dist - quartil1_dist) >= 0:
        # print('la moda esta en el mismo mes y año q quartil1_dist')
        stat_mode_str = str(q1_obj.year) + '-' + str(q1_obj.month) + '-' + str(stat_mode_dist)
    else:
        print('hay un fallo con el calculo de la moda')

    # pasamos la moda a formato obj
    stat_mode_obj = datetime.strptime(stat_mode_str, '%Y-%m-%d')

    lim_inf_recibo_obj = stat_mode_obj - dateutil.relativedelta.relativedelta(months=3)

    num_recibos = 0

    transacciones_219_df_dia.index = pandas.to_datetime(transacciones_219_df_dia.index)

    # barro desde 2 meses antes que la moda hasta el dia antes de la moda
    for d in range(int((stat_mode_obj - lim_inf_recibo_obj).days)):
        # ESTA LINEA NO SE EJECUTA EN PRODUCCIÓN
        #         fecha_str = str((lim_inf_recibo_obj + timedelta(days=d)).year) + \
        #                     '-' + str((lim_inf_recibo_obj + timedelta(days=d)).month) + \
        #                     '-' + str((lim_inf_recibo_obj + timedelta(days=d)).day)
        # ESTA LINEA NO SE EJECUTA EN PRODUCCIÓN
        #         print(fecha_str)
        if (lim_inf_recibo_obj + timedelta(days=d)) in transacciones_219_df_dia.index:
            # ESTA LINEA NO SE EJECUTA EN PRODUCCIÓN
            #             print(fecha_str + ": se pasa un recibo")
            num_recibos += 1

        #     print('num_recibos: ' + str(num_recibos))

    # procedemos a estimar la predicción de la serie temporal

    # Time Series Forecasting With Prophet in Python
    # https://machinelearningmastery.com/time-series-forecasting-with-prophet-in-python/

    # Forecast IMPORTE With Prophet

    # Fit Prophet Model

    df = transacciones_219_importe_df.copy()
    df['FECHA'] = df.index
    df = df[['FECHA', 'IMPORTE']]
    df.reset_index(drop=True, inplace=True)

    # prepare expected column names
    df.columns = ['ds', 'y']
    df['ds'] = to_datetime(df['ds'])

    # A continuación vamos a obtener un dataframe de train desde el 1er dia en que tenemos datos hasta el dia
    # anterior a 'current_date_str' y un dataframe de test desde 'current_date_str' hasta el ultimo dia en que
    # tenemos datos. (en producción no hacemos test)

    limite_superior_train, = (df.index[df['ds'] == current_date_str])
    prophet_train_df = df.iloc[:limite_superior_train, :]

    # define the model
    model = Prophet()
    # fit the model
    model.fit(prophet_train_df)

    # Make an In-Sample Forecast

    # Make an In-Sample Forecast Vamos a hacer una predicción desde el 1er dia en que tenemos datos hasta el ultimo dia
    # del mes siguiente a current_date_str

    lim_sup_pred_obj = current_date_obj + dateutil.relativedelta.relativedelta(months=1)

    # calculo el ultimo dia del mes obj para hacer la predicción del mes entero posterior a la fecha de petición
    lim_sup_pred_str = str(lim_sup_pred_obj.year) + '-' + str(lim_sup_pred_obj.month) + '-' + str(calendar.monthrange(
        lim_sup_pred_obj.year, lim_sup_pred_obj.month)[1])

    lim_sup_pred_obj = datetime.strptime(lim_sup_pred_str, '%Y-%m-%d')

    idx = date_range(start=transacciones_219_importe_df.index.min(), end=lim_sup_pred_obj)

    prophet_pred_df = DataFrame(idx)
    prophet_pred_df.columns = ['ds']

    # use the model to make a forecast
    forecast_df = model.predict(prophet_pred_df)

    prediccion_recibo, = forecast_df.loc[forecast_df['ds'] == stat_mode_obj]['yhat']

    # if para decidir si genero aviso utilizando la predicción de prophet

    if num_recibos > 0:
        #         print("Te van a pasar el próximo recibo del gas natural aproximadamente el: " + stat_mode_str)
        mensaje1_str = "Te van a pasar el próximo recibo del gas natural aproximadamente el: " + stat_mode_str
        #         print("El valor estimado del importe del recibo es de: " + str(5*round(prediccion_recibo/5)) + ' eur')
        mensaje2_str = "El valor estimado del importe del recibo es de: " + str(
            5 * round(prediccion_recibo / 5)) + ' eur'
        aviso = True
    else:
        mensaje1_str = "No te van a pasar recibo del gas natural próximamente."
        mensaje2_str = "El valor estimado del importe del recibo es de: " + str(0) + ' eur'
        aviso = False

    #     print('Aviso: ' + str(aviso))

    return aviso, mensaje1_str, mensaje2_str, stat_mode_str, prediccion_recibo


# Load data using read_excel
# transacciones_orig_df = read_excel('./scripts_jupyter/20210513 mmelero (249236).xlsx', sheet_name='Hoja1')
#
# aviso_orig, mensaje1_orig, mensaje2_orig, dia_factura_orig, importe_recibo_orig = gas_natural_219(
# transacciones_orig_df)
#
# print()
# print(mensaje1_orig)
# print(mensaje2_orig)
# print(aviso_orig)
# print(dia_factura_orig)
# print(importe_recibo_orig)
# print()
# print('Aviso: ' + str(aviso_orig))
# print()
