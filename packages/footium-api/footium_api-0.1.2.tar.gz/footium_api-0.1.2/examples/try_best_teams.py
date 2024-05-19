from setup_environment import *  # noqa: F403
from footium_api import GqlConnection
from footium_api.queries.players import get_players_in_clubs
from footium_api.tools import get_best_teams

gql = GqlConnection()
owners = [
    1164,
    65,
    72,
    1079,
    1405,
    1413,
    1414,
    1415,
    1416,
    1417,
]

# clubs = [2879] # Rocklant
# clubs = [85] # Nordenhave
# clubs = [78] # Bead Stanley
clubs = [102]  # Martot Park

players = get_players_in_clubs(gql, clubs)
best_teams_result = get_best_teams(gql, players)
team_pos = 0
for formation, team in best_teams_result:
    average_rating = round(team["topRating"].mean(), 2)
    fullNames = team["fullName"].values
    print(f"{team_pos}: {formation}: {average_rating}")
    print(team[["topPosition", "topRating", "fullName", "assetId", "clubName"]])
    print()

    # f.write(", ".join(fullNames))
    # loop over unique owenerIds
    for owner in team["ownerId"].unique():
        # fullName for this owner
        owner_fullName = ", ".join(team[team["ownerId"] == owner]["fullName"].values)
        print(f"{int(owner)}: {owner_fullName}")
    print("------")
    team_pos += 1

print("done")
