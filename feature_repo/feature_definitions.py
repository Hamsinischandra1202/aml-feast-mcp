
from datetime import timedelta

from feast import Entity, FeatureView, Field, FileSource
from feast.types import Int64, Float64


# Entity = the thing we want to look up
account = Entity(
    name="account",
    join_keys=["sender_account_id"],
    description="Bank account identified by sender account ID"
)


# Source = where Feast reads the feature data from
account_features_source = FileSource(
    name="account_features_source",
    path="data/account_features.parquet",
    timestamp_field="event_timestamp"
)


# Feature View = the group of account features Feast will manage
account_aml_features = FeatureView(
    name="account_aml_features",
    entities=[account],
    ttl=timedelta(days=3650),

    schema=[
        Field(name="transaction_count", dtype=Int64),
        Field(name="total_transaction_amount", dtype=Float64),
        Field(name="average_transaction_amount", dtype=Float64),
        Field(name="max_transaction_amount", dtype=Float64),
        Field(name="unique_receiver_count", dtype=Int64),
        Field(name="initial_balance", dtype=Float64),
        Field(name="transaction_behavior_id", dtype=Int64),
        Field(name="max_transactions_per_period", dtype=Int64),
        Field(name="active_period_count", dtype=Int64),
        Field(name="average_transactions_per_active_period", dtype=Float64),
        Field(name="max_transaction_to_balance_ratio", dtype=Float64),
    ],

    source=account_features_source,
    online=True,
)
