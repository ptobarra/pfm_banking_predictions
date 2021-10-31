from fastapi import FastAPI
from database import queries, database_connection
from manager import pandas_manager
from controllers.data_insight_controller import data_insight_controller

# Main controller for the proyect.
# It is mandatory to launch the project to execute the command "uvicorn controllers.main_controller:main --reload"
# in a terminal from the root folder of the project.

main = FastAPI()
main.include_router(data_insight_controller)

# Endpoint to check if the service is alive
@main.get('/', status_code=200)
def alive():
    return "{'status': 'alive'}"

#def test():
#    connection = database_connection.get_database_connection()
#    query = queries.GET_ACCOUNT_MOVEMENTS.replace("#account_id#", "347710")
#    data_frame = pandas_manager.transforma_cursor_to_pandas(query, connection)
#    return data_frame
