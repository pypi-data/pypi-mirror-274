from setup_environment import *  # noqa: F403
from footium_api import GqlConnection
from footium_api.queries import (
    get_formations,
    get_lineup_for_club,
    get_server_timestamp,
)
from footium_api.mutations import prepare_lineup_to_sign, submit_lineup
from key_signer import KeySigner

gql = GqlConnection()
formations = get_formations(gql)
for formation in formations:
    print(f"{formation.id}: {formation.name}")
lineup = get_lineup_for_club(gql, 2879, False)
# print(lineup)
timestamp = get_server_timestamp(gql)
print(timestamp)


key_signer = KeySigner()
lineup_message = prepare_lineup_to_sign(gql, lineup)

# signature = "0x2a1e2db05a713e5965563d27bb12e07b715808980fefba0dd2f124fef4c63b99516d3e9c0cc1d3604beaf24fe22bf375690fc0bea460cdad6a46b2f5a97c147b1c"
# address = "0x1839faea698cbae6ede826c09d943de1dba7dd96"
signature = key_signer.sign_message(lineup_message)
address = key_signer.get_eth_address()
is_legit = key_signer.validate_signed_message(signature, lineup_message)
print(f"signature: {signature}, is_legit: {is_legit}")
result = submit_lineup(
    gql, message=lineup_message, signed_message=signature, address=address
)

if result.code == 200:
    print("Lineup submitted successfully")
else:
    print(f"Error: {result.message}")

print("done")
