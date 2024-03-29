# Set up code checking
import os

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge, SGDRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor


def normilize(df):
    return (df - df.min()) / (df.max() - df.min())


# Path of the file to read. We changed the directory structure to simplify submitting to a competition
iowa_file_path = 'train.csv'

imputer = SimpleImputer()
home_data = pd.read_csv(iowa_file_path)
# Create target object and call it y
y = home_data.SalePrice
# Create X
# features = [
#     'LotArea', 'YearBuilt', '1stFlrSF', '2ndFlrSF', 'FullBath', 'BedroomAbvGr',
#     'TotRmsAbvGrd', 'GrLivArea', 'WoodDeckSF', 'OverallCond', 'FullBath']
# X = home_data[features]
X = home_data.select_dtypes(exclude=['object'])
X = pd.DataFrame(imputer.fit_transform(X))

# Split into validation and training data
train_X, val_X, train_y, val_y = train_test_split(X, y, random_state=1)

# train_X = normilize(train_X)
# val_X = normilize(val_X)

# Specify Model
iowa_model = DecisionTreeRegressor(random_state=1)
# Fit Model
iowa_model.fit(train_X, train_y)

# Make validation predictions and calculate mean absolute error
val_predictions = iowa_model.predict(val_X)
val_mae = mean_absolute_error(val_predictions, val_y)
print(
    "Validation MAE when not specifying max_leaf_nodes: {:,.0f}".format(val_mae))

# Using best value for max_leaf_nodes
iowa_model = DecisionTreeRegressor(max_leaf_nodes=100, random_state=1)
iowa_model.fit(train_X, train_y)
val_predictions = iowa_model.predict(val_X)
val_mae = mean_absolute_error(val_predictions, val_y)
print(
    "Validation MAE for best value of max_leaf_nodes: {:,.0f}".format(val_mae))

# Define the model. Set random_state to 1
rf_model = RandomForestRegressor(random_state=1)
rf_model.fit(train_X, train_y)
rf_val_predictions = rf_model.predict(val_X)
rf_val_mae = mean_absolute_error(rf_val_predictions, val_y)

print("Validation MAE for Random Forest Model: {:,.0f}".format(rf_val_mae))

# To improve accuracy, create a new Random Forest model which you will train on all training data
rf_model_on_full_data = RandomForestRegressor(
    random_state=1, n_estimators=500, max_leaf_nodes=250, max_depth=18)
# rf_model_on_full_data = SGDRegressor(random_state = 0, alpha=0.005, eta0=0.1, power_t=0.5, learning_rate="adaptive")
# rf_model_on_full_data = SVR(kernel='poly', degree=5, coef0=1, C=.3, max_iter=500)

# fit rf_model_on_full_data on all data from the training data
rf_model_on_full_data.fit(train_X, train_y)

# path to file you will use for predictions
test_data_path = 'test.csv'

# read test data file using pandas
test_data = pd.read_csv(test_data_path)

# create test_X which comes from test_data but includes only the columns you used for prediction.
# The list of columns is stored in a variable called features
# test_X = test_data[features]
test_X = test_data.select_dtypes(exclude=['object'])
test_X = pd.DataFrame(imputer.fit_transform(test_X))

# make predictions which we will submit.
# test_preds = rf_model_on_full_data.predict(test_X)
preds = rf_model_on_full_data.predict(val_X)

print("Validation MAE for tuned Random Forest Model: {:,.0f}".format(
    mean_absolute_error(val_y, preds)))

# The lines below shows how to save predictions in format used for competition scoring
# Just uncomment them.

# output = pd.DataFrame({'Id': test_data.Id,
#                       'SalePrice': test_preds})
# output.to_csv('submission.csv', index=False)
