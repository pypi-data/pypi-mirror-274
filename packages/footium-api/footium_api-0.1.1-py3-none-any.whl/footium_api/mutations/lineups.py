import json

from footium_api import GqlConnection
from footium_api.queries import get_server_timestamp


def prepare_lineup_to_sign(gql: GqlConnection, lineup):
    timestamp = get_server_timestamp(gql)
    message = {
        "id": -1,
        "type": "LINEUP_SET",
        "data": {
            "lineup": {
                "id": lineup.id,
                "clubId": lineup.clubId,
                "isSelected": lineup.isSelected,
                "tacticsId": lineup.tacticsId,
            },
            "tactics": {
                "id": lineup.tactics.id,
                "mentality": lineup.tactics.mentality,
                "formationId": lineup.tactics.formationId,
            },
            "playerLineups": lineup.playerLineups.to_list(),
        },
        "timestamp": timestamp,
    }
    json_message = json.dumps(message)
    return json_message


def submit_lineup(gql: GqlConnection, message, signed_message, address):
    query = """
mutation SubmitAction($action: String!, $signature: String!, $address: String!) {
    submitAction(action: $action, signature: $signature, address: $address)
    {
        code
        error
        message
        __typename
    }
}
"""
    variables = {
        "signature": signed_message,
        "address": address,
        "action": message,
    }
    response = gql.send_mutation(query, variables)
    return response
