import pandas as pd
from dbconn import *
from fetch_data import *
from wfm_functions import *

import pandas as pd
from dbconn import snowflake_connection
from fetch_data import fetch_orders_data

def read_and_sort_orders(date_range=None, file_path=None):
    """
    Read and sort orders data either from a database using a specified date range or from a parquet file.

    Args:
    - date_range (str, optional): A string representing the date range in "YYYY-MM-DD,YYYY-MM-DD" format.
    - file_path (str, optional): Path to the parquet file containing orders data.

    Returns:
    - pd.DataFrame: A DataFrame containing the sorted orders data.

    Raises:
    - ValueError: If neither date_range nor file_path is provided.
    """
    if date_range is not None:
        # If date_range is provided, fetch data from the database
        conn = snowflake_connection()
        df = fetch_orders_data(conn, date_range=date_range, gmv=True, interval=True)
    elif file_path is not None:
        # If file_path is provided, read data from the parquet file
        df = pd.read_parquet(file_path)
    else:
        # If neither date_range nor file_path is provided, raise an error
        raise ValueError("Either date_range or file_path must be provided")

    # Sort the DataFrame by date, interval, and country
    df_ordered = df.sort_values(by=["FECHA", "INTERVALO", "COUNTRY"])
    return df_ordered

import pandas as pd

def preprocess_special_dates(csv_path):
    """
    Read a CSV file containing special dates and preprocess the dates.

    Args:
    - csv_path (str): Path to the CSV file.

    Returns:
    - list: A list of special dates.
    """
    special = pd.read_csv(csv_path)
    special['Fecha'] = pd.to_datetime(special['Fecha'], format='%d/%m/%Y').dt.date
    special_days = special["Fecha"].to_list()
    return special_days

def filter_special_dates(df, special_days):
    """
    Filter out special dates from a DataFrame.

    Args:
    - df (pd.DataFrame): Input DataFrame containing orders data.
    - special_days (list): List of special dates to be filtered out.

    Returns:
    - pd.DataFrame: Filtered DataFrame.
    """
    df_filtered = df[~df['FECHA'].isin(special_days)]
    df_filtered.reset_index(drop=True, inplace=True)
    return df_filtered


def pivot_orders(df):
    """
    Pivot orders data to get total orders per country per date.

    Args:
    - df (pd.DataFrame): Input DataFrame containing orders data.

    Returns:
    - pd.DataFrame: Pivot table with total orders per country per date.
    """
    ordersxregion = pd.pivot_table(df, values='ORDERS', index=['FECHA', 'INTERVALO'], columns=['COUNTRY'], aggfunc='sum')
    ordersxregion = ordersxregion.fillna(0)
    ordersxregion['SS'] = ordersxregion.drop(columns=['BR']).sum(axis=1)
    ordersxregion['BR'] = ordersxregion['BR']
    ordersxregion = ordersxregion.filter(['CO', 'MX', 'EC', 'PE', 'CL', 'AR', 'UY', 'CR', 'BR', 'SS'])
    orders = ordersxregion[["SS", "BR"]].reset_index()
    orders = orders[["FECHA", "SS", "BR"]].groupby(["FECHA"]).sum()
    orders.reset_index(inplace=True)
    return orders


def create_features(df):
    """
    Create time series features based on the DataFrame index.

    Args:
    - df (pd.DataFrame): Input DataFrame containing orders data.

    Returns:
    - pd.DataFrame: DataFrame with additional time series features.
    """
    df = df.copy()
    df['dayofweek'] = df.index.dayofweek
    df['quarter'] = df.index.quarter
    df['month'] = df.index.month
    df['year'] = df.index.year
    df['dayofyear'] = df.index.dayofyear
    df['dayofmonth'] = df.index.day
    df['weekofyear'] = df.index.isocalendar().week
    return df

def split_train_test_data(data, startdate):
    """
    Split data into train and test sets based on a start date.

    Args:
    - data (pd.DataFrame): Input DataFrame containing orders data.
    - startdate (str): Start date for the test set in "YYYY-MM-DD" format.

    Returns:
    - tuple: A tuple containing the train and test DataFrames.
    """
    data.index = pd.to_datetime(data.index)
    train = data.loc[data.index < startdate]
    test = data.loc[data.index >= startdate]
    return train, test