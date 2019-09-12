import json
import pytest

from process import app


@pytest.fixture
def records():
    return [
        {
            "body": json.dumps(
                {
                    "app": "APM",
                    "tenant": "alfalavale",
                    "meta": {
                        "timestamp": 1568275763,
                        "type": "user-registration-completed",
                    },
                    "payload": {
                        "actor": "278f1d18-8193-4f5f-a94c-203f21541e2c",
                        "target": "298cb315-40f7-4a09-9881-e08f111b9048",
                    },
                }
            )
        },
        {
            "body": json.dumps(
                {
                    "app": "DCX",
                    "tenant": "alfalavale",
                    "meta": {
                        "timestamp": 1568278092,
                        "type": "equipment-request-rejected",
                    },
                    "payload": {
                        "actor": "2549d315-23f1-45b7-86ee-b553bd3d6be2",
                        "target": "c084a5e1-6bf4-4583-b6c3-ca0aa402deb2",
                    },
                }
            )
        },
        {
            "body": json.dumps(
                {
                    "app": "APM",
                    "tenant": "alfalavale",
                    "meta": {
                        "timestamp": 1568278069,
                        "type": "equipment-request-rejected",
                    },
                    "payload": {
                        "actor": "9628848e-2192-419b-8981-4d5f7a7774ab",
                        "target": "b4f8da1f-893d-450b-bb86-d18171db59ac",
                    },
                }
            )
        },
    ]


def test_extract_grouped_events(records):
    assert app.extract_grouped_events(records) == {
        ("APM", "alfalavale"): [
            {
                "app": "APM",
                "tenant": "alfalavale",
                "meta": {
                    "timestamp": 1568275763,
                    "type": "user-registration-completed",
                },
                "payload": {
                    "actor": "278f1d18-8193-4f5f-a94c-203f21541e2c",
                    "target": "298cb315-40f7-4a09-9881-e08f111b9048",
                },
            },
            {
                "app": "APM",
                "tenant": "alfalavale",
                "meta": {"timestamp": 1568278069, "type": "equipment-request-rejected"},
                "payload": {
                    "actor": "9628848e-2192-419b-8981-4d5f7a7774ab",
                    "target": "b4f8da1f-893d-450b-bb86-d18171db59ac",
                },
            },
        ],
        ("DCX", "alfalavale"): [
            {
                "app": "DCX",
                "tenant": "alfalavale",
                "meta": {"timestamp": 1568278092, "type": "equipment-request-rejected"},
                "payload": {
                    "actor": "2549d315-23f1-45b7-86ee-b553bd3d6be2",
                    "target": "c084a5e1-6bf4-4583-b6c3-ca0aa402deb2",
                },
            }
        ],
    }

