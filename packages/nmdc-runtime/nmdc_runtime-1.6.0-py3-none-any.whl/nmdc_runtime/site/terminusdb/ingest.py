import json
from pathlib import Path

from terminusdb_client import WOQLClient

team = "admin"
client = WOQLClient(f"http://localhost:6364/")
# make sure you have put the token in environment variable
# https://docs.terminusdb.com/v10.0/#/terminusx/get-your-api-key
client.connect(user=team, team=team, key="root")

dbid = "nmdc"
label = "NMDC"
description = "."
prefixes = {
    "@base": "terminusdb:///data/",
    "@schema": "terminusdb:///schema#",
    "gold": "https://gold.jgi.doe.gov/biosample?id=",
}


def import_schema(client):
    # sd = get_nmdc_schema_definition()
    # sd.source_file = f"{REPO_ROOT_DIR.parent}/nmdc-schema/src/schema/nmdc.yaml"
    # print(sd.source_file)
    with open(Path(__file__).parent.joinpath("nmdc.schema.terminusdb.json")) as f:
        schema_objects = json.load(f)

    client.message = "Adding NMDC Schema"
    results = client.insert_document(schema_objects, graph_type="schema")
    print(f"Added schema: {results}")


if __name__ == "__main__":
    exists = client.get_database(dbid)

    if exists:
        client.delete_database(dbid, team=team, force=True)

    client.create_database(
        dbid, team, label=label, description=description, prefixes=prefixes
    )

    import_schema(client)
