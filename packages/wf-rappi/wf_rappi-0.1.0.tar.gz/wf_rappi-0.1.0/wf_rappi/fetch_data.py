from dataclasses import dataclass, field
from typing import List
from functools import lru_cache
import pandas as pd


@dataclass(frozen=True, order=True) # Instances of this class will be immutable and orderable based on their fields
class Orders:
    service_user_types: List[str] = field(
        default_factory=lambda: ['User', 'RT', 'Rest'])
    segment_types: List[str] = field(
        default_factory=lambda: ['Inhouse - Rappi'])


@lru_cache(maxsize=None)  # This decorator enables caching with unlimited size
def fetch_test(conn, service_user_types: tuple = None, segment_types: tuple = None) -> pd.DataFrame:
    # Convert single strings to tuples
    if isinstance(service_user_types, str):
        service_user_types = (service_user_types,)
    if isinstance(segment_types, str):
        segment_types = (segment_types,)

    # Convert lists to tuples to make them hashable
    if service_user_types is not None:
        service_user_types = tuple(service_user_types)
    else:
        service_user_types = tuple(Orders().service_user_types)
    if segment_types is not None:
        segment_types = tuple(segment_types)
    else:
        segment_types = tuple(Orders().segment_types)

    # Dynamically construct the IN clause for service_user_types
    service_user_types_in_clause = ', '.join(['%s'] * len(service_user_types))
    # Dynamically construct the NOT IN clause for segment_types
    segment_types_not_in_clause = ', '.join(['%s'] * len(segment_types))

    # Prepare the SQL query with placeholders for parameters
    query = f"""
    SELECT date_trunc(week, created_at)::date as Date,
           avg(aht_ls/60) AS AHT
    FROM fivetran.support_bi.cs_all_tickets
    WHERE service_user_type IN ({service_user_types_in_clause})
    AND segment_type NOT IN ({segment_types_not_in_clause})
    GROUP BY 1
    """

    # Combine service_user_types and segment_types into a single tuple
    # Convert None to an empty tuple
    params = (service_user_types or ()) + (segment_types or ())

    # Execute the query with the parameters
    with conn.cursor() as cur:
        cur.execute(query, params)
        result = cur.fetch_pandas_all()

    return result


def fetch_orders_data(conn, countries=None, region=None, date_range=None, interval=False, gmv=False) -> pd.DataFrame:
    """
    Function to fetch data from the database
    :param conn: Snowflake connection object
    :param countries: List of countries to filter the data
    :param region: Region to filter the data
    :param date_range: 'YYYY-MM-DD' formatted string to specify the date range, e.g. '2023-01-01', '2023-01-31
    :param interval: Boolean to specify if the data should be grouped by interval
    :param gmv: Boolean to specify if the data should be fetched from the GMV table"""
    if gmv:
        return fetch_orders_gmv(conn, countries, region, date_range, interval)
    else:
        return fetch_orders_ops(conn, countries, region, date_range, interval)


def fetch_orders_gmv(conn, countries=None, region=None, date_range=None, interval=False) -> pd.DataFrame:
    """
    Function to fetch orders GMV from the database
    :param conn: Snowflake connection object
    :param countries: List of countries to filter the data
    :param region: Region to filter the data
    :param date_range: Tuple with start and end dates
    :param interval: Boolean to specify if the data should be grouped by interval
    """
    if interval:
        query = """
        SELECT 
            TIME_SLICE(created_at::TIMESTAMP, 30, 'm')::DATE AS FECHA,
            TIME_SLICE(created_at::TIMESTAMP, 30, 'm')::TIME AS INTERVALO,
            CASE WHEN COUNTRY = 'BR' THEN 'BR' ELSE 'SS' END AS region,
            country,
            COUNT(order_id) AS orders
        FROM 
            fivetran.global_finances.global_orders
        WHERE 
            CREATED_AT::date BETWEEN '2023-01-01' AND CURRENT_DATE()-1
        """
    else:
        query = """
        SELECT 
            created_at::DATE AS FECHA,
            CASE WHEN COUNTRY = 'BR' THEN 'BR' ELSE 'SS' END AS region,
            country,
            COUNT(order_id) AS orders
        FROM 
            fivetran.global_finances.global_orders
        WHERE 
            CREATED_AT::date BETWEEN '2023-01-01' AND CURRENT_DATE()-1
        """

    params = []

    if isinstance(countries, str):
        query += " AND country = %s "
        params.append(countries)
    elif isinstance(countries, list):
        country_placeholders = ', '.join(['%s'] * len(countries))
        query += f" AND country IN ({country_placeholders})"
        params.extend(countries)

    if region is not None:
        query += " AND region = %s "
        params.append(region)

    if date_range is not None:
        start_date, end_date = date_range
        query += " AND created_at::DATE BETWEEN DATE %s AND DATE %s "
        params.extend([start_date, end_date])

    if interval:
        query += "GROUP BY 1, 2, 3, 4"
    else:
        query += "GROUP BY 1, 2, 3"

    # Execute the query with the parameters
    with conn.cursor() as cur:
        cur.execute(query, params)
        result = cur.fetch_pandas_all()

    return result


def fetch_orders_ops(conn, countries=None, region=None, date_range=None, interval=False) -> pd.DataFrame:
    
    """
    Function to fetch orders ops from the database
    :param conn: Snowflake connection object
    :param countries: List of countries to filter the data
    :param region: Region to filter the data
    :param date_range: 'YYYY-MM-DD' formatted string to specify the date range, e.g. '2023-01-01', '2023-01-31
    :param interval: Boolean to specify if the data should be grouped by interval
    
    Returns:
        pd.DataFrame:
            DataFrame containing the fetched data.
    """
    if interval:
        query = """
        SELECT 
            TIME_SLICE(created_at,30,'m')::date FECHA,
            TIME_SLICE(created_at,30,'m')::time INTERVALO,
            CASE WHEN COUNTRY = 'BR' THEN 'BR' ELSE 'SS' END AS region,
            country,
            COUNT(order_id) AS orders
        FROM 
            FIVETRAN.SUPPORT_BI.CS_ORDERS_GENERAL_TBL
        WHERE 
            CREATED_AT::date BETWEEN '2023-01-01' AND CURRENT_DATE()-1
            AND NOT synthetic AND is_ops 
        """
    else:
        query = """
        SELECT 
            created_at::DATE AS FECHA,
            CASE WHEN COUNTRY = 'BR' THEN 'BR' ELSE 'SS' END AS region,
            country,
            COUNT(order_id) AS orders
        FROM 
            FIVETRAN.SUPPORT_BI.CS_ORDERS_GENERAL_TBL
        WHERE 
            CREATED_AT::date BETWEEN '2023-01-01' AND CURRENT_DATE()-1
            AND NOT synthetic AND is_ops 
        """

    params = []

    if isinstance(countries, str):
        query += " AND country = %s "
        params.append(countries)
    elif isinstance(countries, list):
        country_placeholders = ', '.join(['%s'] * len(countries))
        query += f" AND country IN ({country_placeholders})"
        params.extend(countries)

    if region is not None:
        query += " AND region = %s "
        params.append(region)

    if date_range is not None:
        start_date, end_date = date_range
        query += " AND created_at::date BETWEEN DATE %s AND DATE %s "
        params.extend([start_date, end_date])

    query += "GROUP BY FECHA, INTERVALO, region, country" if interval else "GROUP BY FECHA, region, country"

    # Execute the query with the parameters
    with conn.cursor() as cur:
        cur.execute(query, params)
        result = cur.fetch_pandas_all()

    return result

##############3
def fetch_special_days(conn, countries=None, region=None, date_range=None, interval=False) -> pd.DataFrame:
    
    """
    Function to fetch specia days from the database
    :param conn: Snowflake connection object
    :param countries: List of countries to filter the data
    :param region: Region to filter the data
    :param date_range: 'YYYY-MM-DD' formatted string to specify the date range, e.g. '2023-01-01', '2023-01-31
    :param interval: Boolean to specify if the data should be grouped by interval
    
    Returns:
        pd.DataFrame:
            DataFrame containing the fetched data.
    """
    if interval:
        query = """
        select
            TIME_SLICE(DATE,30,'m')::date DATE,
            TIME_SLICE(DATE,30,'m')::time INTERVALO,
            event_type as event,
            country,
            CASE WHEN COUNTRY = 'BR' THEN 'BR' ELSE 'SS' END AS region,
            tier_ops,
            tier_forecast,
            growth_orders
        from FIVETRAN.predictions.global_special_days_tier_growths 
        union
        select DATE::date as DATE,
            event_name as event,
            country,
            CASE WHEN COUNTRY = 'BR' THEN 'BR' ELSE 'SS' END AS region,
            tier as tier_ops,
            null as tier_forecast,
            orders_growth_vs_median as growth_orders
        from FIVETRAN.predictions.global_fcst_special_days 
        """
    else:
        query = """
        select DATE::date as DATE,
            event_type as event,
            country,
            CASE WHEN COUNTRY = 'BR' THEN 'BR' ELSE 'SS' END AS region,
            tier_ops,
            tier_forecast,
            growth_orders
        from FIVETRAN.predictions.global_special_days_tier_growths 
        union
        select DATE::date as DATE,
            event_name as event,
            country,
            CASE WHEN COUNTRY = 'BR' THEN 'BR' ELSE 'SS' END AS region,
            tier as tier_ops,
            null as tier_forecast,
            orders_growth_vs_median as growth_orders
        from FIVETRAN.predictions.global_fcst_special_days  
        """

    # params = []

    # if isinstance(countries, str):
    #     query += " AND country = %s "
    #     params.append(countries)
    # elif isinstance(countries, list):
    #     country_placeholders = ', '.join(['%s'] * len(countries))
    #     query += f" AND country IN ({country_placeholders})"
    #     params.extend(countries)

    # if region is not None:
    #     query += " AND region = %s "
    #     params.append(region)

    # if date_range is not None:
    #     start_date, end_date = date_range
    #     query += " AND created_at::date BETWEEN DATE %s AND DATE %s "
    #     params.extend([start_date, end_date])

    # query += "GROUP BY FECHA, INTERVALO, region, country" if interval else "GROUP BY FECHA, region, country"

    # Execute the query with the parameters
    with conn.cursor() as cur:
        cur.execute(query)
        result = cur.fetch_pandas_all()

    return result
