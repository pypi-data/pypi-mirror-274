from data_processing import *
from modeling import *
from export import *
from order_distribution import distribute_orders
from order_distribution import create_ordenes_financieras, create_curva_ordenes

# Path to the Parquet file containing order data
# parquet_path = "C:/Users/jonathan.marin/Documents/GitHub/rappi/wfm/libreria/one_year_and_a_half.parquet.gzip"
date_range=['2024-04-01', '2024-04-10']

# Path to the CSV file containing special dates
csv_path = "C:/Users/jonathan.marin/Documents/GitHub/rappi/wfm/Calendario Rappi - BD_Feriados.csv"

# Start date for the dataset
startdate = "2024-01-01"

# Read and sort order data
df_ordered = read_and_sort_orders(date_range)

# Preprocess special dates
special_days = preprocess_special_dates(csv_path)

# Filter special dates from the ordered dataframe
df_filtered = filter_special_dates(df_ordered, special_days)

# Pivot the filtered dataframe to get orders by region and day
orders = pivot_orders(df_filtered)

# Set the index of orders dataframe to "FECHA" column
data = orders.set_index("FECHA")

# Split the data into training and testing sets
train, test = split_train_test_data(data, startdate)

# Create time series features for training and testing sets
train = create_features(train)
test = create_features(test)

# Features and target variable
FEATURES = ['dayofweek', 'quarter', 'month', 'year', 'dayofyear', 'dayofmonth', 'weekofyear']
TARGET = "SS"

# Extract features and target variable for training and testing sets
X_train = train[FEATURES]
y_train = train[TARGET]

X_test = test[FEATURES]
y_test = test[TARGET]

# Train an XGBoost model
model = train_xgboost_model(X_train, y_train, X_test, y_test)

# Make predictions using the trained model
predictions = make_predictions(model, X_test)

# Add predictions to the test dataframe
test['prediction'] = predictions

# Calculate RMSE score
score = calculate_rmse(y_test, predictions)

# Select data for April
abril = test[test.index >= '2024-04-01']

# Create financial orders based on predicted values and average daily weights
ordenes_financieras = create_ordenes_financieras(df_ordered, abril)

# Create an order curve based on order distribution throughout the week
curva_ordenes = create_curva_ordenes(df_ordered)

# Distribute financial orders according to the order curve
df3 = distribute_orders(ordenes_financieras, curva_ordenes)
print(df3.head())
print("Done!")
