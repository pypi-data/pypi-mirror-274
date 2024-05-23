import snowflake.connector
import os
import json


def get_project_settings(import_filepath="settings.json"):
    """
    Function to import settings from settings.json
    :param import_filepath: path to settings.json
    :return: settings as a dictionary object
    """
    if os.path.exists(import_filepath):
        try:
            with open(import_filepath, "r") as f:
                project_settings = json.load(f)
            return project_settings
        except Exception as e:
            raise ImportError(f"Error reading settings.json: {e}")
    else:
        raise ImportError("settings.json does not exist at provided location")


def snowflake_connection(project_settings=get_project_settings(), AUTO_COMMIT=True):
    conn = snowflake.connector.connect(
        user=project_settings["snowflake"]["user"],
        password=project_settings["snowflake"]["password"],
        account=project_settings["snowflake"]["account"],
        authenticator=project_settings["snowflake"]["authenticator"],
        database=project_settings["snowflake"]["database"],
        autocommit=True if AUTO_COMMIT == True else False
    )
    return conn


# Function to disconnect the database connection and clear cache
def disconnect_and_clear_cache(conn):
    cur = conn.cursor()
    cur.close()
    # Disconnect the database connection
    conn.close()
