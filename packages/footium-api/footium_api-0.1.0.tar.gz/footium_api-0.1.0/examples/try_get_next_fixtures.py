from setup_environment import *  # noqa: F403
from footium_api import GqlConnection
from footium_api.queries import get_next_fixtures
import pandas as pd
from datetime import datetime

gql = GqlConnection()
clubIds = [
    78,
    102,
    1077,
    2897,
    1315,
    2715,
    3012,
    1450,
    462,
    2774,
    1511,
    676,
    1314,
    706,
    728,
    1901,
    894,
    604,
    2180,
    1198,
    85,
    2815,
    2388,
    2228,
    521,
    577,
    1291,
    523,
    1508,
    503,
    1278,
    1302,
    1834,
    2805,
    2839,
    498,
    1033,
    1332,
    1811,
    1831,
    2551,
    2659,
    2896,
    2661,
    2320,
    2915,
    2991,
    2453,
    2879,
]

fixtures = get_next_fixtures(gql, clubIds, 100)

fixtures["localTime"] = fixtures["realWorldTimestamp"].dt.tz_convert(None)
local_tz = datetime.now().astimezone().tzinfo
fixtures["localTime"] = fixtures["realWorldTimestamp"].dt.tz_convert(local_tz)


# preitty print the time until kickoff
def format_timedelta(td):
    total_seconds = int(td.total_seconds())
    time_string = ""
    if total_seconds < 0:
        total_seconds = abs(total_seconds)
        time_string += "ago "
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    if hours > 0:
        time_string += f"{hours}h, {minutes}m"
    elif minutes > 0:
        time_string += f"{minutes}m, {seconds}s"
    else:
        time_string += f"{seconds}s"
    return time_string


now = pd.Timestamp.now(tz="UTC")
fixtures["timeToKickOff"] = fixtures["realWorldTimestamp"] - now
fixtures["timeToKickOff"] = fixtures["timeToKickOff"].apply(format_timedelta)

# order by realWorldTimestamp ascending
fixtures = fixtures.sort_values(by="realWorldTimestamp")

print(fixtures.head())
# walk thrrough each row in the DataFrame and print the row
# for index, row in fixtures.iterrows():
# print(row)
print(fixtures.to_string(index=False))


print("Done!")
