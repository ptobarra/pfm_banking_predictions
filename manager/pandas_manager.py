import pandas
from pandas import DataFrame

# Uses Pandas library to obtain a data frame from a query to a database.
def get_data_frame_from_database_query(query_string, database_connection):
    # pandas.set_option('display.max_rows', 12)
    # pandas.set_option('display.max_rows', None)
    pandas.set_option('display.max_columns', None)
    pandas.set_option('display.width', None)
    pandas.set_option('display.max_colwidth', None)
    data_frame = pandas.read_sql(query_string, database_connection)
    # print(data_frame)
    return data_frame
