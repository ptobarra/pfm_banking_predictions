import GIT_INTEGRACION_forecast_3_months_20210318
import GIT_INTEGRACION_gas_natural_219_ide
import GIT_INTEGRACION_impago_nomina_pension_desempleo_20210607
import GIT_INTEGRACION_liquidacion_tarjeta_126_20210621
import GIT_INTEGRACION_restaurantes_salidas_116
import GIT_INTEGRACION_seguro_medico_prophet_ide_20210616
import GIT_INTEGRACION_seguro_vehiculo_78_20210630
import GIT_INTEGRACION_supermercados_70
from database import database_connection
from manager import json_manager, database_queries_manager


# Checks if the salary is unpaid.
def is_unpaid_salary(account_id):
    connection = database_connection.get_database_connection()
    data_frame = database_queries_manager.get_account_transactions(connection, account_id)
    connection.close()
    notify, message = \
        GIT_INTEGRACION_impago_nomina_pension_desempleo_20210607.impago_nomina_pension_desempleo(data_frame)
    return json_manager.create_unpaid_salary_response(notify, message)


# Gets the information about the medical insurance.
def get_medical_insurance_info(account_id):
    connection = database_connection.get_database_connection()
    data_frame = database_queries_manager.get_account_transactions(connection, account_id)
    connection.close()
    alert, prediction_receipt, stat_mode_str, message1, message2 = \
        GIT_INTEGRACION_seguro_medico_prophet_ide_20210616.seguro_medico(data_frame)
    return json_manager.create_medical_insurance_response(alert, prediction_receipt, stat_mode_str, message1, message2)


# forecast next liquidacion_tarjeta_126 bill amount and date
def liquidacion_tarjeta_forecast(account_id):
    connection = database_connection.get_database_connection()
    data_frame = database_queries_manager.get_account_transactions(connection, account_id)
    mensaje1, mensaje2, mensaje3, importe_recibo, dia_factura, aviso = \
        GIT_INTEGRACION_liquidacion_tarjeta_126_20210621.liquidacion_tarjeta_126(data_frame)
    return json_manager.create_liquidacion_tarjeta_response(aviso, mensaje1, mensaje2, mensaje3, dia_factura,
                                                            importe_recibo)


# forecast next gas_natural_219 bill amount and date
def natural_gas(account_id):
    connection = database_connection.get_database_connection()
    data_frame = database_queries_manager.get_account_transactions(connection, account_id)
    aviso, mensaje1, mensaje2, dia_factura, importe_recibo = \
        GIT_INTEGRACION_gas_natural_219_ide.gas_natural_219(data_frame)
    return json_manager.create_natural_gas_response(aviso, mensaje1, mensaje2, dia_factura, importe_recibo)


# forecast total next month amount of expenses in restaurantes_salidas_216
def restaurantes_salidas_216(account_id):
    connection = database_connection.get_database_connection()
    data_frame = database_queries_manager.get_account_transactions(connection, account_id)
    balance_data_frame = database_queries_manager.get_account_balance_information(connection, account_id)
    mensaje1, mensaje2, valid_prediction_orig, final_amount, final_year_orig, final_month_orig, final_month_orig_str = \
        GIT_INTEGRACION_restaurantes_salidas_116.restaurantes_salidas_116(data_frame, balance_data_frame)
    return json_manager.create_restaurantes_salidas_216_response(mensaje1, mensaje2, valid_prediction_orig,
                                                                 final_amount, final_year_orig, final_month_orig,
                                                                 final_month_orig_str)


# forecast total next month amount of expenses in supermercados_70
def supermercados_70(account_id):
    connection = database_connection.get_database_connection()
    data_frame = database_queries_manager.get_account_transactions(connection, account_id)
    balance_data_frame = database_queries_manager.get_account_balance_information(connection, account_id)
    mensaje1, mensaje2, valid_prediction, final_amount, final_year, final_month, final_month_str = \
        GIT_INTEGRACION_supermercados_70.supermercados_70(data_frame, balance_data_frame)
    return json_manager.create_supermercados_70_response(mensaje1,
                                                         mensaje2,
                                                         valid_prediction,
                                                         final_amount,
                                                         final_year,
                                                         final_month,
                                                         final_month_str)


def seguro_vehiculo_78(account_id):
    connection = database_connection.get_database_connection()
    data_frame = database_queries_manager.get_account_transactions(connection, account_id)
    balance_data_frame = database_queries_manager.get_account_balance_information(connection, account_id)
    system_date, mensaje1, next_bill_date, mensaje2, last_bill_date, mensaje3, next_bill_amount_float, mensaje4, \
        last_year_b, mensaje5, next_month_b, mensaje6, next_month_def_b, mensaje7 = \
        GIT_INTEGRACION_seguro_vehiculo_78_20210630.seguro_vehiculo_78(data_frame, balance_data_frame)
    return json_manager.create_seguro_vehiculo_78(system_date,
                                                  mensaje1,
                                                  next_bill_date,
                                                  mensaje2,
                                                  last_bill_date,
                                                  mensaje3,
                                                  next_bill_amount_float,
                                                  mensaje4,
                                                  last_year_b,
                                                  mensaje5,
                                                  next_month_b,
                                                  mensaje6,
                                                  next_month_def_b,
                                                  mensaje7)


# def forecast_3_months(login_id):
def forecast_3_months(account_id):
    connection = database_connection.get_database_connection()
    data_frame = database_queries_manager.get_account_transactions(connection, account_id)
    balance_data_frame = database_queries_manager.get_account_balance_information(connection, account_id)
    forecast_per_week_final_df = GIT_INTEGRACION_forecast_3_months_20210318.forecast_3_months(data_frame,
                                                                                              balance_data_frame)
    return json_manager.create_forecast_3_months(forecast_per_week_final_df)
