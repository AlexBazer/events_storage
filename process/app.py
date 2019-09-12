import os
import json
import logging
from pymongo import MongoClient
from itertools import groupby

logger = logging.getLogger(__name__)


client = None


def get_db_client():
    global client
    if client:
        return client
    client = MongoClient(os.environ["MongoDBConnectionString"])
    return client


def process(event, context):
    client = get_db_client()

    grouped_events = extract_grouped_events(event["Records"])

    for (app, tenant), events in grouped_events.items():
        client[f"{app}_{tenant}"].events.insert_many(list(events))


def extract_grouped_events(records):
    app_tenant_key = lambda item: (item["app"], item["tenant"])
    events = sorted(
        (e for e in (event_factory(record) for record in records) if e),
        key=app_tenant_key,
    )

    return {
        (app, tenant): list(items)
        for (app, tenant), items in groupby(events, key=app_tenant_key)
    }


def event_factory(record):
    try:
        json_body = json.loads(record["body"])
    except json.JSONDecodeError:
        logger.info(f"Can't parse json body for message id ${record['messageId']}")
        return

    if not json_body.get("meta"):
        return

    return {
        "app": json_body["app"],
        "tenant": json_body["tenant"],
        "meta": json_body.get("meta") or {},
        "payload": json_body.get("payload") or {},
    }
