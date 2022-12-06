def cleanse_match_results(
    match_results_df,
    cols_to_keep=['matchid', 'dates', 'gender', 'outcome.winner', 'teams'],
):
    # ************************************************************************************
    # Accepts match results, drops uneeded columns, and filters matches to only those
    # with natrual winner (exludings DLS decisions, ties, etc.)
    # ************************************************************************************

    # Removes all games decided by DLS
    match_results_df = match_results_df.loc[match_results_df["outcome.method"].isna()]
    # Removes all tied/no results games
    match_results_df = match_results_df.loc[match_results_df["result"].isna()]

    # Drops superfluous columns
    match_results_df = match_results_df[cols_to_keep]

    return match_results_df


def split_by_gender(df):
    # **********************************************************************
    # Splits match_results_df by gender and returns resulting tuple
    # **********************************************************************

    return df.loc[df['gender'] == 'male'].drop(['gender'], axis=1), df.loc[
        df['gender'] == 'female'
    ].drop(['gender'], axis=1)


def cleanse_innings_results(
    innings_results_df,
    match_results_df,
    cols_to_keep=['matchid', 'team', 'innings', 'over', 'runs.total', 'wicket.kind'],
):
    # ************************************************************************************
    # Accepts innings results and match_results_df and filters/returns innings results
    # for only those matches that end in a result, also drops uneeded columns
    # ************************************************************************************

    matchids = _collect_matchids(match_results_df)
    innings_results_df = innings_results_df.loc[
        innings_results_df['matchid'].isin(matchids)
    ]

    # Drops superfluous columns
    innings_results_df = innings_results_df[cols_to_keep]

    return innings_results_df


def _collect_matchids(match_results_df):
    # *******************************************************************************
    # Filters match_results to those that have a result, and returns those matchids
    # *******************************************************************************
    match_results_df['result'].unique()
    return match_results_df.loc[
        (match_results_df["result"].isna()) | (match_results_df["result"] == "tied")
    ]['matchid'].unique()
