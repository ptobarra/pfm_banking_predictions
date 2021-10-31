from fastapi import APIRouter
from manager import data_insight_manager
from pydantic import BaseModel


class LoginId(BaseModel):
    loginId: int


data_insight_controller = APIRouter()


@data_insight_controller.post('/unpaid_salary/{accountId}', status_code=200)
def isUnpaidSalary(accountId: str):
    json_response = data_insight_manager.is_unpaid_salary(accountId)
    return json_response


@data_insight_controller.post('/medical_insurance/{accountId}', status_code=200)
def get_medical_insurance(accountId: str):
    json_response = data_insight_manager.get_medical_insurance_info(accountId)
    return json_response


@data_insight_controller.post('/card_forecast/{accountId}', status_code=200)
def liquidacion_tarjeta_forecast(accountId: str):
    json_response = data_insight_manager.liquidacion_tarjeta_forecast(accountId)
    return json_response


@data_insight_controller.post('/natural_gas/{accountId}', status_code=200)
def natural_gas_forecast(accountId: str):
    json_response = data_insight_manager.natural_gas(accountId)
    return json_response


@data_insight_controller.post('/restaurantes_salidas/{accountId}', status_code=200)
def restaurantes_salidas_forecast(accountId: str):
    json_response = data_insight_manager.restaurantes_salidas_216(accountId)
    return json_response


@data_insight_controller.post('/supermercados/{accountId}', status_code=200)
def supermercados_forecast(accountId: str):
    json_response = data_insight_manager.supermercados_70(accountId)
    return json_response


@data_insight_controller.post('/seguro_vehiculo/{accountId}', status_code=200)
def seguro_forecast(accountId: str):
    json_response = data_insight_manager.seguro_vehiculo_78(accountId)
    return json_response


@data_insight_controller.post('/forecast_3_months/{accountId}', status_code=200)
def seguro_forecast(accountId: str):
    json_response = data_insight_manager.forecast_3_months(accountId)
    return json_response
