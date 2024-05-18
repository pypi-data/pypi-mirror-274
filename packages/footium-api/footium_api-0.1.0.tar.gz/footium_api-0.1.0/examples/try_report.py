from setup_environment import *  # noqa: F403
from footium_api import GqlConnection, DiscordReportStrategy


gql = GqlConnection(report_strategy=DiscordReportStrategy())
id = "03"

gql.report.info(f"This is an info message; id: {id}")
gql.report.event(f"This is an event message; id: {id}")
gql.report.warning(f"This is a warning message; id: {id}")
gql.report.error(f"This is an error message; id: {id}")
