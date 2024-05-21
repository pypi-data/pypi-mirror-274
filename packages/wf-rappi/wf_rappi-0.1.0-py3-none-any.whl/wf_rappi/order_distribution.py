import pandas as pd
import numpy as np
import datetime

def create_ordenes_financieras(df, abril, ordenes_aprobadas=None):
    """
    Create financial orders based on predicted values and average daily weights.

    Args:
    - df (pd.DataFrame): Dataframe containing order information.
    - abril (pd.DataFrame): Dataframe containing predicted values for April.
    - ordenes_aprobadas (int, optional): Number of approved orders. If provided, the orders will be distributed based on this value. If not, it will distribute the orders based on the predicted values.


    Returns:
    - pd.DataFrame: DataFrame with financial/forecasted orders.
    """

    orders = df.copy()
    orders = orders[orders["COUNTRY"] != "BR"]
    start_date = datetime.datetime.strptime("2024-01-01", "%Y-%m-%d").date()
    orders = orders[orders["FECHA"] >= start_date]

    orders['FECHA'] = pd.to_datetime(orders['FECHA'])
    pivot_table = orders.pivot_table(index='FECHA', columns='COUNTRY', values='ORDERS', aggfunc='mean', fill_value=0)
    SS = pivot_table.sum(axis=1)
    SS.name = 'SS'
    pivot_table_with_total = pd.merge(pivot_table, SS.to_frame(), on="FECHA", how="inner")
    pivot_table_percentage = pivot_table_with_total.div(pivot_table_with_total['SS'], axis=0) * 100
    pivot_table_percentage = pivot_table_percentage.round(2)
    average_weight_by_day = pivot_table_percentage.groupby(pivot_table_percentage.index.day).mean()
    average_weight_by_day = average_weight_by_day[:-1] # quitar el 31 de abril
    date_strings = [f'2024-04-{day}' for day in average_weight_by_day.index]
    average_weight_by_day.index = pd.to_datetime(date_strings, format='%Y-%m-%d')
    average_weight_by_day.index = average_weight_by_day.index.strftime('%Y-%m-%d')

    df_abril = abril['prediction']
    series_reindexed = df_abril.reindex(average_weight_by_day.index, fill_value=0)
    # if there are diferent numbers of approved orders then use it.
    if ordenes_aprobadas:
        ordenes_aprobadas = ordenes_aprobadas
        prop_ordenes_dias_mes = series_reindexed/series_reindexed.sum()
        series_reindexed = prop_ordenes_dias_mes*ordenes_aprobadas
    # series_reindexed_modif.head()
    ordenes_financieras = average_weight_by_day.mul(series_reindexed, axis=0) / 100
    orden_dias = ['CO', 'MX', 'EC', 'PE', 'CL', 'AR', 'UY', 'CR', 'SS']
    ordenes_financieras = ordenes_financieras.filter(orden_dias)
    ordenes_financieras = ordenes_financieras.reset_index()
    ordenes_financieras.rename(columns={"index": "FECHA"}, inplace=True)
        
    return ordenes_financieras

def create_curva_ordenes(df):
    """
    Create order curve based on order distribution throughout the week.

    Args:
    - df (pd.DataFrame): Dataframe containing order information.

    Returns:
    - pd.DataFrame: DataFrame with order curve.
    """

    orders = df.copy()
    orders = orders[orders["COUNTRY"] != "BR"]
    start_date = datetime.datetime.strptime("2024-01-01", "%Y-%m-%d").date()
    orders = orders[orders["FECHA"] >= start_date]

    orders['FECHA'] = pd.to_datetime(orders['FECHA'])
    orders['INTERVALO'] = pd.to_datetime(orders['INTERVALO'], format='%H:%M:%S').dt.time
    orders['DAY_OF_WEEK'] = orders['FECHA'].dt.day_name()

    pivot_table = orders.pivot_table(index='INTERVALO', columns='DAY_OF_WEEK', values='ORDERS', aggfunc='mean', fill_value=0)
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    pivot_table.columns = pd.CategoricalIndex(pivot_table.columns, categories=weekdays, ordered=True)
    pivot_table = pivot_table.sort_index(axis=1)

    total_general = pivot_table.sum(axis=0)
    total_general.name = 'Total general'

    pivot_table_with_total = pd.concat([pivot_table, total_general.to_frame().T])

    pivot_table_percentage = pivot_table_with_total.div(pivot_table_with_total.loc['Total general']) * 100
    pivot_table_percentage = pivot_table_percentage.round(2)
    curva_ordenes = pivot_table_percentage.drop(pivot_table_percentage.tail(1).index)  # drop last row
    curva_ordenes = curva_ordenes.reset_index()
    curva_ordenes.rename(columns={"index": "intervalo"}, inplace=True)
    curva_ordenes.set_index("intervalo", inplace=True)
    curva_ordenes = curva_ordenes / 100
    
    return curva_ordenes


def distribute_orders(ordenes_financieras, curva_ordenes):
    """
    Distribute financial orders according to the order curve.

    Args:
    - ordenes_financieras (pd.DataFrame): Dataframe containing financial orders.
    - curva_ordenes (pd.DataFrame): Dataframe containing order curve.

    Returns:
    - pd.DataFrame: DataFrame with distributed orders by day and interval.
    """

    index = pd.MultiIndex.from_product([ordenes_financieras['FECHA'].unique(), curva_ordenes.index], names=['FECHA', 'Intervalo'])
    df3 = pd.DataFrame(index=index, columns=ordenes_financieras.columns[1:], data=np.zeros((len(index), len(ordenes_financieras.columns[1:]))))
    df3 = df3.reset_index()

    def get_day_of_week(date):
        return pd.to_datetime(date).strftime('%A')

    for i, row in ordenes_financieras.iterrows():
        day_of_week = get_day_of_week(row['FECHA'])
        values = row[1:].values
        for j, interval in enumerate(curva_ordenes.index):
            proportion = curva_ordenes.loc[interval, day_of_week]
            df3.loc[(df3['FECHA'] == row['FECHA']) & (df3['Intervalo'] == interval), ordenes_financieras.columns[1:]] += values * proportion
    
    return df3
