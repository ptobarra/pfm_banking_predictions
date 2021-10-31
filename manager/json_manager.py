def create_unpaid_salary_response(notify, message):
    json = {"notify": notify, "message": message}
    return json


def create_medical_insurance_response(alert, prediction_receipt, stat_mode_str, message1, message2):
    json = {"alert": alert, "prediction_receipt": prediction_receipt, "stat_mode": stat_mode_str,
            "message1": message1, "message2": message2}
    return json


def create_liquidacion_tarjeta_response(aviso, mensaje1, mensaje2, mensaje3, dia_factura, importe_recibo):
    json = {"aviso": aviso, "mensaje1": mensaje1, "mensaje2": mensaje2, "mensaje3": mensaje3,
            "dia_factura": dia_factura, "importe_recibo": importe_recibo}
    return json


def create_natural_gas_response(aviso, mensaje1, mensaje2, dia_factura, importe_recibo):
    json = {"aviso": aviso, "mensaje1": mensaje1, "mensaje2": mensaje2, "dia_factura": dia_factura,
            "importe_recibo": importe_recibo}
    return json


def create_restaurantes_salidas_216_response(mensaje1, mensaje2, valid_prediction_orig, final_amount, final_year_orig,
                                             final_month_orig, final_month_orig_str):
    json = {"mensaje1": mensaje1, "mensaje2": mensaje2, "valid_prediction_orig": valid_prediction_orig,
            "final_amount": final_amount, "final_year_orig": final_year_orig, "final_month_orig": final_month_orig,
            "final_month_orig_str": final_month_orig_str}
    return json


def create_supermercados_70_response(mensaje1,
                                     mensaje2,
                                     valid_prediction,
                                     final_amount,
                                     final_year,
                                     final_month,
                                     final_month_str):
    json = {"mensaje1": mensaje1, "mensaje2": mensaje2, "valid_prediction": valid_prediction,
            "final_amount": final_amount, "final_year": final_year, "final_month": final_month,
            "final_month_str": final_month_str}
    return json


def create_seguro_vehiculo_78(system_date,
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
                              mensaje7):
    json = {"system_date": system_date,
            "mensaje1": mensaje1,
            "next_bill_date": next_bill_date,
            "mensaje2": mensaje2,
            "last_bill_date": last_bill_date,
            "mensaje3": mensaje3,
            "next_bill_amount_float": next_bill_amount_float,
            "mensaje4": mensaje4,
            "last_year_b": last_year_b,
            "mensaje5": mensaje5,
            "next_month_b": next_month_b,
            "mensaje6": mensaje6,
            "next_month_def_b": next_month_def_b,
            "mensaje7": mensaje7}
    return json


def create_forecast_3_months(forecast_per_week_final_df):
    json = {"forecast_per_week_final_df": forecast_per_week_final_df}
    return json
