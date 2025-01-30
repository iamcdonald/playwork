from kafka import KafkaConsumer
from app.conf import conf
import asyncio
import threading
import httpx
import json

def run():
    consumer = KafkaConsumer(
        'pg_conn.public.things',
        bootstrap_servers = "{host}:9092".format(host=conf.KAFKA_HOST),
        # will consume from beginning of topic events
        # auto_offset_reset='earliest',
        group_id=None,
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    )
    for msg in consumer:
        httpx.post(
            url="http://{host}:5561/publish".format(host=conf.PUSHPIN_INTERNAL_HOST),
            headers={"Content-Type": "application/json"},
            json={
                "items": [
                    {
                        "channel":"things",
                        "formats": {
                            "http-stream": {
                                "content": "{json}\n\n".format(json=json.dumps(msg.value))
                            }
                        }
                    }
                ]
            }
        )
        yield

thread = threading.Thread(target=asyncio.run, args=run())
