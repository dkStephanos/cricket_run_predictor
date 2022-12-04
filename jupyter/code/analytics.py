import pandas as pd


def assemble_yearly_summaries_per_team(
    match_results_df, start_year=2009, end_year=2022
):
    # **********************************************************************
    # Extracts the win records per year/per team from the match_results
    # accepts start/end year as optional parameters
    # **********************************************************************

    # Initialize result df
    yearly_summary_df = pd.DataFrame(
        columns=['Year', 'Team', 'TotalGames', 'TotalWins', 'Win%']
    )

    # Iterate through years, and then teams to collect statistics
    for year in [str(x) for x in list(range(start_year, end_year))]:
        year_df = match_results_df.loc[match_results_df['dates'].str.contains(year)]
        for team in year_df['teams'].unique():
            total_wins = year_df[
                (year_df['outcome.winner'] == team) & (year_df['teams'] == team)
            ].shape[0]
            total_games = year_df[year_df['teams'] == team].shape[0]

            yearly_summary_df = pd.concat(
                [
                    yearly_summary_df,
                    pd.DataFrame.from_dict(
                        {
                            'Year': [year],
                            'Team': [team],
                            'TotalGames': [total_games],
                            'TotalWins': [total_wins],
                            'Win%': [total_wins / total_games],
                        }
                    ),
                ]
            )

    return yearly_summary_df


def assemble_over_statistics(innings_results_df):
    # **************************************************************************************
    # Extracts the runs_per_over and relevant associated data accross all provided innings
    # **************************************************************************************

    # Initialize result df
    overs_summary_df = pd.DataFrame(
        columns=[
            'matchid',
            'Team',
            'Innings',
            'Over',
            'RemainingOvers',
            'RunsPerOver',
            'TotalRuns',
            'RemainingWickets',
        ]
    )
    for index, row in innings_results_df.iterrows():
        if index == 0 or row['innings'] > last_innings:
            # Initialize
            last_innings = row['innings']
            last_over = int(str(row['over']).split('.')[0])
            runs_per_over = row['runs.total']
            total_runs = row['runs.total']
            remaining_wickets = 10
        else:
            curr_over = int(str(row['over']).split('.')[0])
            # Check to see if we just transitioned overs, in which case commit the statistics
            if curr_over > last_over:
                overs_summary_df = pd.concat(
                    [
                        overs_summary_df,
                        pd.DataFrame.from_dict(
                            {
                                'matchid': [row['matchid']],
                                'Team': [row['team']],
                                'Innings': [row['innings']],
                                'Over': [last_over],
                                'RemainingOvers': [50 - last_over],
                                'RunsPerOver': [runs_per_over],
                                'TotalRuns': [total_runs],
                                'RemainingWickets': [remaining_wickets],
                            }
                        ),
                    ]
                )
                runs_per_over = 0

            # Collect statistics for this bowl
            last_innings = row['innings']
            last_over = curr_over
            runs_per_over += row['runs.total']
            total_runs += row['runs.total']
            if pd.notnull(row['wicket.kind']):
                remaining_wickets -= 1

    # Commit the last iteration
    overs_summary_df = pd.concat(
        [
            overs_summary_df,
            pd.DataFrame.from_dict(
                {
                    'matchid': [innings_results_df['matchid'].iloc[-1]],
                    'Team': [innings_results_df['team'].iloc[-1]],
                    'Innings': [innings_results_df['innings'].iloc[-1]],
                    'Over': [last_over],
                    'RemainingOvers': [50 - last_over],
                    'RunsPerOver': [runs_per_over],
                    'TotalRuns': [total_runs],
                    'RemainingWickets': [remaining_wickets],
                }
            ),
        ]
    )

    return overs_summary_df
