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
