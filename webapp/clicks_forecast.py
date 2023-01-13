import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split

def load_data() -> pd.DataFrame:
    """This code contains a function called "load_data()" that uses the Pandas library to read in and process a CSV file. """

    file = "static/data.csv"
    df = pd.read_csv(file)
    df = df[["reporting_start", "reporting_end", "spent", "impressions", "clicks", "campaign_id"]]

    df_without_missing = df.dropna()
    q_low = df_without_missing["spent"].quantile(0.01)
    q_hi  = df_without_missing["spent"].quantile(0.99)

    df_filtered = df_without_missing[(df_without_missing["spent"] < q_hi) & (df_without_missing["spent"] > q_low)]
    return df_filtered

def transform_data(df, dependent: str, campaign: str) -> tuple:
    """Processes data by filtering and transforming it into a suitable format for use in a statistical model."""
    df_filtered = df[df["campaign_id"] == campaign]
    y = df_filtered[dependent].values.reshape(-1, 1)
    x = df_filtered["spent"].values.reshape(-1, 1)
    return (x,y)

def train_model(x,y) -> tuple:
    """Trains a linear regression model based on two input arguments (x, y)."""
    regressor = LinearRegression()
    regressor.fit(x, y)
    coef = regressor.coef_
    intercept = regressor.intercept_
    return (coef,intercept)

def predict(slope: float, interc: float, eu: float) -> float:
    """The user must provide the coefficients and y-intercept of the model as arguments
    and the value of the independent variable for which the prediction is to be made.
    The function then returns the prediction for the dependent variable."""
    return round(float(slope * eu + interc),2)

def evaluate(df, coef, interc, campaign, target):
    """The user has to provide the DataFrame, coefficients and y-intercept of the model, campaign and target column as arguments.
     The function then returns a list of the MAE, MSE, RMSE, R^2 score and correlation between the target and spent column,
     which can be used to determine how well the model is performing."""

    df = df[df["campaign_id"] == campaign]
    y_actual = df[target]
    df["prediction"] = df.apply(lambda row: float(coef * row.spent + interc), axis=1)
    mae = mean_absolute_error(y_actual, df["prediction"])
    mse = mean_squared_error(y_actual, df["prediction"])
    rmse = np.sqrt(mse)
    rs = r2_score(y_actual, df["prediction"])
    correlation_df = df.corr()
    correlation = correlation_df[target].loc["spent"]
    return [mae, mse, rmse, rs, correlation]

def check_reliablity(correlation: float, r_squared: float) -> bool:
    """Returns a boolean value to determine if the prediction is reliable"""
    return correlation >= 0.8 and r_squared >= 0.7



