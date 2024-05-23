import pandas as pd
import numpy as np


def orders_dist(df, region=None, country=None, aggfunc='sum', dist=False, month=False):
    # Convert 'FECHA' column to datetime
    df['FECHA'] = pd.to_datetime(df['FECHA'])

    # Convert region and country to list if they are not already
    if isinstance(region, str):
        region = [region]
    if isinstance(country, str):
        country = [country]

    # Filter DataFrame if region and/or country are provided
    if region:
        df = df[df['REGION'].isin(region)]
    if country:
        df = df[df['COUNTRY'].isin(country)]

    # Determine the index for the pivot table based on the month parameter
    if month:
        # Extract unique month names from the 'FECHA' column
        unique_months = df['FECHA'].dt.strftime('%B').unique()
        index = df['FECHA'].dt.strftime('%B')
    else:
        index = df['FECHA'].dt.strftime('%A')

    # Pivot DataFrame and calculate distribution of orders by day of the week or month name
    pivot_table = df.pivot_table(
        index=index,
        columns=['REGION', 'COUNTRY'],
        values='ORDERS',
        aggfunc=aggfunc,
        fill_value=np.nan
    )

    # Reorder the index based on the unique months present in the data
    if month:
        # Convert the index to an ordered categorical type for correct month sorting
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        pivot_table.index = pd.CategoricalIndex(pivot_table.index, categories=months, ordered=True)
        pivot_table = pivot_table.sort_index()
    else:
        # Convert the index to an ordered categorical type for correct weekday sorting
        weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        pivot_table.index = pd.CategoricalIndex(pivot_table.index, categories=weekdays, ordered=True)
        pivot_table = pivot_table.sort_index()

    # Compute row totals (grand totals for each day or month)
    pivot_table['Total'] = pivot_table.sum(axis=1)

    # Compute column totals (grand totals for each region and country)
    pivot_table.loc['Grand Total'] = pivot_table.sum()
    
    # Calculate percentage distribution if dist is True
    if dist:
        for col in pivot_table.columns[:-1]: # Exclude 'Total' and 'Grand Total' columns
            pivot_table[col] = (pivot_table[col] / pivot_table['Total']) * 100
        
        # Calculate the percentage for each day or month
        pivot_table['Total'] = (pivot_table['Total'] / pivot_table['Total'].iloc[-1]) * 100

    pivot_table.replace(0, np.nan, inplace=True)

    return pivot_table