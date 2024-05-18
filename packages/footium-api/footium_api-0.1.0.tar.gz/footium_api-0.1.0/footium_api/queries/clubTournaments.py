from typing import List
import pandas as pd
from footium_api import GqlConnection


def get_clubs_tournament_for_owners(gql: GqlConnection, owner_ids: List[int]):
    query = """
query GetClubsByOwnerId($ownerIdFilter: IntFilter!, $take: Int, $skip: Int) {
  clubs(where: {ownerId: $ownerIdFilter}, take: $take, skip: $skip) {
    id
    name
    ownerId
    owner {
      id
      address
    }
    clubTournaments(orderBy: [{tournament: {id: desc}}], take: 1, where: {tournament: {isNot: {isComplete: {equals: true}}}}) {
      position
      tournament {
        name
        type
        competition{
            divisionId
            leagueIndex
        }
      }
    }
  }
}
    """
    variables = {
        "ownerIdFilter": {"in": owner_ids},
    }
    response = gql.send_paging_query(query, variables)
    clubs = response
    # flatter the clubs so we dont gave depth
    clubs = [
        {
            "id": club.id,
            "name": club.name,
            "division": club.clubTournaments[0].tournament.competition.divisionId,
            "position": club.clubTournaments[0].position,
            "league": club.clubTournaments[0].tournament.competition.leagueIndex,
            "tournament_name": club.clubTournaments[0].tournament.name,
            "tournament_type": club.clubTournaments[0].tournament.type,
            "owner_id": club.owner.id,
            "owner_address": club.owner.address,
        }
        for club in clubs
    ]
    clubs = sorted(clubs, key=lambda x: (x["division"], x["position"]))
    # convert to pandas dataframe
    # id is the index
    clubs = pd.DataFrame(clubs).set_index("id")
    return clubs
