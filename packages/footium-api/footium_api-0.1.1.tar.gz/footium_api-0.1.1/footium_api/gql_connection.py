from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport
from box import Box
from gql.transport.exceptions import TransportQueryError
from .report import ReportStrategy, LogReportStrategy


class GqlConnection:
    def __init__(
        self,
        url="https://live.api.footium.club/api/graphql",
        load_schema=None,
        report_strategy: ReportStrategy = LogReportStrategy(),
    ):
        self.url = url
        self.report = report_strategy
        self.transport = RequestsHTTPTransport(
            url=self.url,
            use_json=True,
        )
        if load_schema is None:
            self.client = Client(transport=self.transport)
        else:
            try:
                with open(load_schema) as f:
                    schema_str = f.read()
                self.client = Client(transport=self.transport, schema=schema_str)
            except Exception:
                self.client = Client(
                    transport=self.transport, fetch_schema_from_transport=True
                )

    def send_query(self, query, variables=None, operation_name=None):
        gql_query = gql(query)
        response = self.client.execute(
            gql_query, variable_values=variables, operation_name=operation_name
        )
        boxed_response = Box(response)
        return boxed_response

    def send_paging_query(
        self, query, variables=None, operation_name=None, skip=0, take=20, stop=None
    ):
        gql_query = gql(query)
        results = None
        count = 0
        while True:
            variables["skip"] = skip
            variables["take"] = take
            response = self.client.execute(
                gql_query, variable_values=variables, operation_name=operation_name
            )
            boxed_response = Box(response)
            if len(list(boxed_response.keys())) != 1:
                raise NotImplementedError(
                    f"send_paging_query only supports single key, got {len(list(boxed_response.keys()))}"
                )
            key = list(boxed_response.keys())[0]
            boxed_response = boxed_response[key]
            if results is None:
                results = boxed_response
            else:
                results.extend(boxed_response)
            count += len(boxed_response)
            if stop is not None and count >= stop:
                break
            if len(boxed_response) < take:
                break
            skip += take
        return results

    def send_mutation(self, query, variables=None, operation_name=None):
        gql_query = gql(query)
        try:
            response = self.client.execute(
                gql_query, variable_values=variables, operation_name=operation_name
            )
            boxed_response = Box(response["submitAction"])
        except TransportQueryError as e:
            response = {
                "code": "500",
                "error": "Internal Server Error",
                "message": str(e),
                "__typename": "Error",
            }
            boxed_response = Box(response)
        return boxed_response
