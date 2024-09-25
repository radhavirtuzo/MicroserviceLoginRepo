from flask import current_app
import pyodbc
from databaseconfig.Database import connection_string
from .encryption import Encryption
from .utils import response
def authenticate_user(user_name, user_password):
    try:
        encrypted_password = Encryption.encrypt(user_password)
        with pyodbc.connect(connection_string) as connection:
            with connection.cursor() as cursor:
                result = cursor.execute("EXEC sp_authenticate_user ?, ?", (user_name, encrypted_password))
                auth_result = result.fetchone()
                if auth_result:
                    user_id = auth_result[0]
                    return response("200", "Login successful", user_id)
                else:
                    return response("103", "Incorrect username or password", None)
    except Exception as e:
        current_app.logger.error(f"Error during authentication for user {user_name}: {e}")
        return response("500", "Error during authentication", None)

def get_user_details(user_name):
    try:
        with pyodbc.connect(connection_string) as connection:
            with connection.cursor() as cursor:
                result = cursor.execute("EXEC GetUserInventorydetails ?", (user_name,))
                columns = [column[0] for column in cursor.description]
                user_details = result.fetchall()
                user_details_list = [dict(zip(columns, row)) for row in user_details]
                if user_details_list:
                    return response("200", "User details retrieved successfully", None ,details=user_details_list)
                else:
                    return response("103", "No details found for the given username",None,None)
    except Exception as e:
        current_app.logger.error(f"Error fetching user details for username {user_name}: {e}")
        return response("500", "Error fetching user details", None)