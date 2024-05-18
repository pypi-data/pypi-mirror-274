from setup_environment import *  # noqa: F403
from footium_api import GqlConnection
from footium_api.queries import get_clubs_tournament_for_owners


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
clubs = get_clubs_tournament_for_owners(gql, owners)
# clubs is a pandas dataframe
# print a table with columns: id, name, division, position
print(clubs[["name", "division", "position"]].sort_values(["division", "position"]))
# print order by position
print(clubs[["name", "division", "position"]].sort_values(["position", "division"]))
# save to csv
clubs[["name", "division", "position", "owner_id", "owner_address"]].sort_values(
    ["division", "position"]
).to_csv("clubs.csv")
