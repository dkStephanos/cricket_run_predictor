import matplotlib.pyplot as plt


def plot_runs_per_over(
    overs_df, matchid=None, team=None, target_col="Over", aggr="sum", save_result=True
):
    # ************************************************************************************
    # Plots the runs per over for the provided data set with a number of optional params
    # Params:
    # overs_df -> the dataset itself (see data/results/over_summary.csv)
    # matchid -> The id(s) being requested, defaults to None for entire dataset
    # team -> The team name(s) being requested, defaults to None for entire dataset
    # target_col -> The column of intereste to be grouped against, defaults to Over
    # aggr -> The aggregation to apply, currently supported (sum, mean)
    # save_result -> bool, if True, outputs created graph to png image in data/plots
    # ************************************************************************************

    # Filter for the match/matches requested, if none requested default to entire dataset
    if matchid is not None:
        if isinstance(matchid, int):
            match_df = overs_df.loc[(overs_df["matchid"] == matchid)]
        elif isinstance(matchid, list):
            match_df = overs_df.loc[(overs_df["matchid"].isin(matchid))]
    else:
        match_df = overs_df

    # Build the graph title based on input params, filter for requested team/teams (optional)
    title = f"{'Total' if aggr == 'sum' else 'Average'} RunsPerOver v {target_col}"
    if team is not None:
        if isinstance(team, int):
            match_df = match_df.loc[match_df['Team'] == team]
            title += f" for: {team}"
        elif isinstance(team, list):
            match_df = overs_df.loc[(overs_df["Team"].isin(team))]
            title += f" for: {', '.join(team)}"

    # Apply appropriate aggr to groupby results on provided target column and plot results
    if aggr == "sum":
        match_df.groupby([target_col]).sum(numeric_only=True)["RunsPerOver"].plot(
            y='RunsPerOver',
            kind='bar',
            title=title,
        )
    elif aggr == "mean":
        match_df.groupby([target_col]).mean(numeric_only=True)["RunsPerOver"].plot(
            y='RunsPerOver',
            kind='bar',
            title=title,
        )

    # If prompted, save results as image, and always show!
    if save_result:
        plt.savefig(f'../data/plots/runs-per-over-{matchid if matchid is not None else "allgames"}-{team if team is not None else "allteams"}-{target_col}-{aggr}.png')
    plt.show()
