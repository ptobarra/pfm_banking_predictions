import pyodbc
from manager import properties_manager
import constants
import cx_Oracle
import mysql.connector
import psycopg2

# Gets a database connection using the parameters indicated in the properties file.
def get_database_connection():
    properties = properties_manager.load_properties(constants.PROPERTIES_FILE_PATH)
    # print(properties)

    type = properties.get("database_type")
    server = properties.get("server")
    database = properties.get("database")
    username = properties.get("username")
    password = properties.get("password")
    driver = properties.get("driver")

    if type == constants.SQL_SERVER_DATABASE:
        connection = pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    elif type == constants.MYSQL_DATABASE:
        connection = mysql.connector.connect(host=server, user=username, password=password, database=database)
    elif type == constants.POSTGRESQL_DATABASE:
        connection = psycopg2.connect(host=server, database=database, user=username, password=password)
    elif type == constants.ORACLE_DATABASE:
        connection = get_connection_to_oracle_database(properties)
        #connection = cx_Oracle.connect(user=username, password=password, dsn= '"' + server + '"')
    #cursor = connection.cursor()

    #cursor.execute('SELECT * FROM t_alert_types')
    #columns = [column[0] for column in cursor.description]
    #print(columns)
    #for row in cursor:
    #    print(row)
    return connection

# Gets the connection to an Oracle database.
def get_connection_to_oracle_database(properties):
    sid = properties.get("oracle_sid")
    port = properties.get("oracle_port")
    server = properties.get("server")
    username = properties.get("username")
    password = properties.get("password")
    driver = properties.get("driver")
    # The connections is obtained differently if the SID is provided.
    if not sid:
        connection = cx_Oracle.connect(user=username, password=password, dsn=server)
    else:
        dsnStr = cx_Oracle.makedsn(server, port, sid)
        connection = cx_Oracle.connect(user=username, password=password, dsn=dsnStr)
    return connection