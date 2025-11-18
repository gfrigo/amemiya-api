import asyncio
import json
import types

import pytest

from src.mqtt_worker import worker
from src.core import migrations

class FakeCursor:
    def __init__(self):
        self.queries = []
    def execute(self, stmt, params=None):
        self.queries.append((stmt, params))
    def fetchone(self):
        return None
    def close(self):
        pass

class FakeConn:
    def __init__(self):
        self.committed = False
    def commit(self):
        self.committed = True
    def close(self):
        pass

class Msg:
    def __init__(self, topic, payload):
        self.topic = topic
        self.payload = payload

@pytest.mark.asyncio
async def test_handle_message_persists(monkeypatch):
    fake_cursor = FakeCursor()
    fake_conn = FakeConn()

    # patch start_connection and start_cursor
    def fake_start_connection(creds):
        class Ctx:
            def __enter__(self):
                return fake_conn
            def __exit__(self, exc_type, exc, tb):
                return False
        return Ctx()

    def fake_start_cursor(conn):
        class Ctx:
            def __enter__(self):
                return fake_cursor
            def __exit__(self, exc_type, exc, tb):
                return False
        return Ctx()

    monkeypatch.setattr('src.mqtt_worker.worker.start_connection', fake_start_connection)
    monkeypatch.setattr('src.mqtt_worker.worker.start_cursor', fake_start_cursor)

    # create a fake message
    payload = json.dumps({"temperature": 25}).encode()
    msg = types.SimpleNamespace(topic='amemiya/1/device/dev01/telemetry', payload=payload)

    # call handler
    await worker.handle_message(msg)

    # verify that an insert was attempted
    assert len(fake_cursor.queries) >= 1
    insert_stmt, params = fake_cursor.queries[0]
    assert 'INSERT INTO Telemetry' in insert_stmt
    assert params[0] == 1 or params[0] is None
    assert params[1] == 'dev01' or params[1] is None
