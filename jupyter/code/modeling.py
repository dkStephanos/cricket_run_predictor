from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd
import pickle

def predict_runs_per_over(
    overs_df,
    feature_cols=["Innings", "RemainingOvers", "RemainingWickets"],
    test_size=0.3,
):

    # Select the target_col
    y = overs_df["RunsPerOver"]

    # Select the feature cols, and normalize them to avoid scale bias
    X = StandardScaler().fit_transform(overs_df[feature_cols])

    # Split the data into training/testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42
    )

    # Fit the model, generate predictions on test set
    regr = LinearRegression().fit(X_train, y_train)
    y_pred = regr.predict(X_test)

    # The coefficients
    print("Coefficients: \n", regr.coef_)
    # The mean squared error
    print("Mean squared error: %.2f" % mean_squared_error(y_test, y_pred))
    # The coefficient of determination: 1 is perfect prediction
    print("Coefficient of determination: %.3f" % r2_score(y_test, y_pred))

    pickle.dump(regr, open('./data/models/linear-regression-runsPerOver.sav', 'wb'))

def apply_model(X_test, y_test):
    loaded_model = pickle.load(
        open('./data/models/linear-regression-runsPerOver.sav', 'rb')
    )
    result = loaded_model.score(X_test, y_test)
    print(result)

