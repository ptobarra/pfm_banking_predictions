from database import queries
from manager import pandas_manager

# Gets the information of all accounts of a login of the application
def get_accounts_information_by_holder_id(connection, holder_id):
    query = queries.GET_HOLDER_ACCOUNT_MOVEMENTS.replace("#login_id#", holder_id)
    return pandas_manager.get_data_frame_from_database_query(query, connection)

# Gets a data frame with the information of the balance of an account.
def get_account_balance_information(connection, account_id):
    query = queries.GET_CURRENT_BALANCE.replace("#account_id#", account_id)
    return pandas_manager.get_data_frame_from_database_query(query, connection)

# Gets the information of the transactions of an account.
def get_account_transactions(connection, account_id):
    query = queries.GET_ACCOUNT_TRANSACTIONS.replace("#account_id#", account_id)
    return pandas_manager.get_data_frame_from_database_query(query, connection)