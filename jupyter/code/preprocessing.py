import pandas as pd


def cleanse_match_results(
    match_results_df,
    innings_results_df,
    cols_to_keep=['matchid', 'dates', 'gender', 'outcome.winner', 'teams'],
):
    # *********************************************************************************************************
    # Accepts match results and innings results, drops uneeded columns, imputes incomplete information,
    # and filters matches to only those with natrual winner (exludings DLS decisions, ties, etc.)
    # *********************************************************************************************************

    # Removes all games decided by DLS
    match_results_df = match_results_df.loc[match_results_df["outcome.method"].isna()]
    # Removes all tied/no results games
    match_results_df = match_results_df.loc[match_results_df["result"].isna()]

    # Teams information only lists a single team (?), collecting other team from corresonding innings data
    for index, row in match_results_df.iterrows():
        temp_df = innings_results_df.loc[
            innings_results_df['matchid'] == row['matchid']
        ]
        match_results_df.at[index, 'teams'] = list(temp_df['team'].unique())

    # Drops superfluous columns
    match_results_df = match_results_df.drop(
        list(set(match_results_df.columns).difference(set(cols_to_keep))), axis=1
    )

    return match_results_df


def split_by_gender(df):
    # **********************************************************************
    # Splits match_results_df by gender and returns resulting tuple
    # **********************************************************************

    return df.loc[df['gender'] == 'male'].drop(['gender'], axis=1), df.loc[
        df['gender'] == 'female'
    ].drop(['gender'], axis=1)
