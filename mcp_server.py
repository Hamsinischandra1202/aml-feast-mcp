
import requests
from mcp.server import MCPServer


# Create the MCP server
mcp = MCPServer("AML Feast MCP Server")


# Address of the Feast HTTP Feature Server
FEAST_URL = "http://127.0.0.1:6566"


@mcp.tool()
def get_account_aml_features(sender_account_id: int) -> dict:
    """
    Retrieve behavioural financial-crime-related features
    for a sender account from Feast.
    """

    payload = {
        "features": [
            "account_aml_features:transaction_count",
            "account_aml_features:total_transaction_amount",
            "account_aml_features:average_transaction_amount",
            "account_aml_features:max_transaction_amount",
            "account_aml_features:unique_receiver_count",
            "account_aml_features:initial_balance",
            "account_aml_features:transaction_behavior_id",
            "account_aml_features:max_transactions_per_period",
            "account_aml_features:active_period_count",
            "account_aml_features:average_transactions_per_active_period",
            "account_aml_features:max_transaction_to_balance_ratio"
        ],

        "entities": {
            "sender_account_id": [sender_account_id]
        }
    }

    response = requests.post(
        f"{FEAST_URL}/get-online-features",
        json=payload,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    # Feast returns feature names and values separately.
    # Convert them into an easier dictionary for the AI.
    feature_names = data["metadata"]["feature_names"]
    results = data["results"]

    output = {}

    for feature_name, result in zip(feature_names, results):

        if result["statuses"][0] == "PRESENT":
            output[feature_name] = result["values"][0]

        else:
            output[feature_name] = None

    return output


if __name__ == "__main__":
    mcp.run()
