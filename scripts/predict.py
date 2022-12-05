import pandas as pd
import pickle
from sklearn.preprocessing import StandardScaler
import sys

_, data_path, matchid, num_overs = sys.argv

df = pd.read_csv(data_path, index_col=0)
df = df.loc[df['matchid'] == int(matchid)].head(int(num_overs))

X = StandardScaler().fit_transform(
    df[["Innings", "RemainingOvers", "RemainingWickets"]]
)
loaded_model = pickle.load(
    open('../data/models/linear-regression-runsPerOver.sav', 'rb')
)
print(loaded_model.predict(X))


input('\n\nPress ENTER to exit')
