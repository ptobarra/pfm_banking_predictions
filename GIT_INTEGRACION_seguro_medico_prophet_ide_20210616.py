from pandas import date_range, DataFrame, to_numeric, to_datetime
# from pandas import read_excel
from pandas.tseries.offsets import DateOffset
import pandas
import statistics
import dateutil.relativedelta

from prophet import Prophet

import calendar

from datetime import datetime, timedelta


def seguro_medico(transacciones_nomina_df):
    # nos quedamos con las transacciones de la categoría 'seguro_salud_90'
    transacciones_nomina_df = transacciones_nomina_df.iloc[:, 0:3]

    # 20210812 modificación
    transacciones_90_df = transacciones_nomina_df[transacciones_nomina_df['ID Categoría'] == 90.0]

    # nos quedamos con categoría desde 'Fecha transacción' hasta 'Importe'
    transacciones_90_df = transacciones_90_df.iloc[:, 0:2]

    # renombramos columnas
    transacciones_90_df = transacciones_90_df.rename(columns={'Fecha transacción': 'FECHA',
                                                              'Importe': 'IMPORTE'}, inplace=False)

    # ordenamos las fechas por orden ascendente
    transacciones_90_df = transacciones_90_df.sort_values(by=['FECHA'], ascending=True, inplace=False,
                                                          ignore_index=True)

    # vamos a agrupar los valores y sumarlos por fecha para agrupar cargos distintos realizados el mismo dia
    transacciones_90_df = transacciones_90_df.groupby(['FECHA']).sum()

    # para que los datos sean más fáciles de interpretar vamos a hacerlos todos positivos multiplicándolos por '-1'
    transacciones_90_df['IMPORTE'] = -transacciones_90_df['IMPORTE']

    # hacemos el dataframe del dia de pago del seguro medico
    transacciones_90_dia_df = transacciones_90_df.copy()

    # hacemos una columna con la fecha a partir del índice
    transacciones_90_dia_df['FECHA'] = transacciones_90_dia_df.index

    transacciones_90_dia_df['FECHA'] = pandas.to_datetime(transacciones_90_dia_df['FECHA'])

    # hacemos una columna con el dia a partir de la columna de la fecha
    transacciones_90_dia_df['DIA'] = transacciones_90_dia_df['FECHA'].dt.day

    # calculamos la moda - tomaremos la moda como el dia de cobro mas habitual
    stat_mode_dist = statistics.mode(transacciones_90_dia_df['DIA'])

    # extraemos el 1er cuartil
    quartil1_dist = int(transacciones_90_dia_df.describe().loc['25%']['DIA'])

    # extraemos el 3er cuartil
    quartil3_dist = int(transacciones_90_dia_df.describe().loc['75%']['DIA'])

    # calculamos el rango intercuartílico
    iqr_dist = quartil3_dist - quartil1_dist

    # si NO pasan recibo a FIN DE MES
    if stat_mode_dist < 28:
        iqr = iqr_dist
    # si SÍ pasan recibo a FIN DE MES
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
    month = str(1)
    day = str(20)

    # pasamos la fecha a string
    current_date_str = year + '-' + month + '-' + day

    # pasamos la fecha al formato datetime
    current_date_obj = datetime.strptime(current_date_str, '%Y-%m-%d')

    # pasamos iqr a formato datetime
    iqr_obj = timedelta(days=iqr)

    # sumamos 1 mes a current_date_obj ya que vamos a calcular fecha e importe del recibo
    # al mes siguiente al que se lo pedimos
    target_date_obj = current_date_obj + DateOffset(months=1)

    # calculamos quartil3_obj en función de current_date_obj, quartil3_dist y si pasan el recibo a FIN de MES o NO

    # si SÍ pasan recibo a FIN de MES
    if stat_mode_dist >= 28:
        # quartil3_obj sera el ultimo dia del mes de current_date_obj
        quartil3 = calendar.monthrange(target_date_obj.year, target_date_obj.month)[1]
        quartil3_str = str(target_date_obj.year) + '-' + str(target_date_obj.month) + '-' + str(quartil3)
    # si NO pasan recibo a FIN de MES
    else:
        quartil3_str = str(target_date_obj.year) + '-' + str(target_date_obj.month) + '-' + str(quartil3_dist)

    del target_date_obj

    q3_obj = datetime.strptime(quartil3_str, '%Y-%m-%d')

    q1_obj = q3_obj - iqr_obj

    stat_mode_str = ""

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

    # miraremos tres meses más atrás del mes objetivo para ver si hubo recibos en esos dos meses y no nos hemos
    # dado de baja del servicio (estamos mirando desde 2 meses más atrás del mes que pedimos la predicción)
    liminfrecibo_obj = stat_mode_obj - dateutil.relativedelta.relativedelta(months=3)

    num_recibos = 0

    # barro desde 3 meses antes que la moda hasta el dia antes de la moda

    transacciones_90_dia_df.index = pandas.to_datetime(transacciones_90_dia_df.index)

    for d in range(int((stat_mode_obj - liminfrecibo_obj).days)):
        # estas lineas no se ejecutan en producción
        ####
        # fecha_str = str((liminfrecibo_obj + timedelta(days=d)).year) + '-' + str((liminfrecibo_obj +
        #                                                                           timedelta(days=d)).month) +'-'+ str(
        #     (liminfrecibo_obj + timedelta(days=d)).day)
        # print(fecha_str)
        ####
        if (liminfrecibo_obj + timedelta(days=d)) in transacciones_90_dia_df.index:
            num_recibos += 1
            # print(fecha_str + ": se pasa un recibo")

    # hacemos el dataframe de la serie temporal del importe de los recibos y estimados el valor del recibo
    # para el mes siguiente a la fecha en la que pedimos la predicción

    transacciones_90_importe_df = transacciones_90_df.copy()
    del transacciones_90_df

    transacciones_90_importe_df['FECHA'] = transacciones_90_importe_df.index

    idx = date_range(start=transacciones_90_importe_df.FECHA.min(), end=transacciones_90_importe_df.FECHA.max())

    # rellenamos las missing dates con NaN
    transacciones_90_importe_df = transacciones_90_importe_df.reindex(idx, fill_value='NaN')

    transacciones_90_importe_df.drop(columns='FECHA', inplace=True)

    # vamos a cambiar el tipo de 'IMPORTE' de 'object' a 'float64'
    transacciones_90_importe_ser = transacciones_90_importe_df.T.squeeze()
    transacciones_90_importe_ser = to_numeric(transacciones_90_importe_ser, errors='coerce')
    transacciones_90_importe_df = DataFrame(transacciones_90_importe_ser)
    del transacciones_90_importe_ser

    # rellenamos los NaN con el valor numérico de la primera fecha anterior
    transacciones_90_importe_df['IMPORTE'].fillna(method='ffill', inplace=True)

    # Forecast IMPORTE With Prophet
    # Fit Prophet Model
    df = transacciones_90_importe_df.copy()
    df['FECHA'] = df.index
    df = df[['FECHA', 'IMPORTE']]
    df.reset_index(drop=True, inplace=True)

    # prepare expected column names
    df.columns = ['ds', 'y']
    df['ds'] = to_datetime(df['ds'])

    # A continuación vamos a obtener un dataframe de train desde el 1er dia en que tenemos datos hasta el dia
    # anterior a 'current_date_str'
    limite_superior_train, = (df.index[df['ds'] == current_date_str])
    prophet_train_df = df.iloc[:limite_superior_train, :]

    # define the model
    model = Prophet()
    # fit the model
    model.fit(prophet_train_df)

    # Make an In-Sample Forecast
    # Vamos a hacer una predicción desde el 1er dia en que tenemos datos hasta el ultimo dia del mes siguiente
    # a current_date_str
    lim_sup_pred_obj = current_date_obj + dateutil.relativedelta.relativedelta(months=1)

    # calculo el ultimo dia del mes obj para hacer la predicción del mes entero posterior a la fecha de petición
    lim_sup_pred_str = str(lim_sup_pred_obj.year) + '-' + str(lim_sup_pred_obj.month) + '-' + str(calendar.monthrange(
        lim_sup_pred_obj.year, lim_sup_pred_obj.month)[1])

    lim_sup_pred_obj = datetime.strptime(lim_sup_pred_str, '%Y-%m-%d')

    idx = date_range(start=transacciones_90_importe_df.index.min(), end=lim_sup_pred_obj)

    prophet_pred_df = DataFrame(idx)
    prophet_pred_df.columns = ['ds']

    # use the model to make a forecast
    forecast_df = model.predict(prophet_pred_df)

    # esto no ira en producción
    # plot forecast
    #     model.plot(forecast_df)
    #     pyplot.show()

    prediccion_recibo, = forecast_df.loc[forecast_df['ds'] == stat_mode_obj]['yhat']

    # if para decidir si genero aviso utilizando la predicción de prophet

    mensaje1 = ""
    mensaje2 = ""

    if num_recibos > 0:
        mensaje1 = "Te van a pasar el próximo recibo aproximadamente el: " + stat_mode_str
        mensaje2 = "El importe aproximado del recibo será de: " + str(5 * round(prediccion_recibo / 5)) + ' eur'
        #         print("Te van a pasar el próximo recibo aproximadamente el: " + stat_mode_str)
        #         print("El importe aproximado del recibo será de: " + str(5*round(prediccion_recibo/5)) + ' eur')
        aviso = True
    else:
        aviso = False

    return aviso, prediccion_recibo, stat_mode_str, mensaje1, mensaje2

# Load data using read_excel
# transacciones_nomina_orig_df = read_excel('./scripts_jupyter/20210513 mmelero (249236).xlsx', sheet_name='Hoja1')

# print()
# print(transacciones_nomina_orig_df)
# print()

# aviso_orig, prediccion_recibo_orig, stat_mode_str_orig, mensaje1_orig, mensaje2_orig = seguro_medico(
#    transacciones_nomina_orig_df)

# print()
# print(stat_mode_str_orig)
# print(prediccion_recibo_orig)
# print(aviso_orig)
# print(mensaje1_orig)
# print(mensaje2_orig)
# print('Aviso: ' + str(aviso_orig))
# print()
