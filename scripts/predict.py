import pandas as pd
import pickle
from sklearn.preprocessing import StandardScaler

df = pd.read_csv('../data/results/over_summary.csv', index_col=0)
df = df.loc[df['matchid'] == 1029001].head(5)

X = StandardScaler().fit_transform(
    df[["Innings", "RemainingOvers", "RemainingWickets"]]
)
loaded_model = pickle.load(
    open('../data/models/linear-regression-runsPerOver.sav', 'rb')
)
print(loaded_model.predict(X))


input('\n\nPress ENTER to exit')
