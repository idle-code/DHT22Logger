import flask
from google.cloud import bigquery
from google.cloud.bigquery import TableReference
from datetime import datetime
import json


def default_encoder(o):
    if isinstance(o, datetime):
        return o.isoformat()


def upload(request: flask.Request):
    client = bigquery.Client(project='idlecode-va-data-collection')

    payload = {
        "timestamp": datetime.now(),
        "temperature": request.args.get("temperature", type=float),
        "humidity": request.args.get("humidity", type=float)
    }

    if not payload["temperature"]:
        return "Missing temperature", 400
    if not payload["humidity"]:
        return "Missing humidity", 400

    print(json.dumps({
        "event": "Got data",
        "payload": payload
    }, default=default_encoder))

    sensor_data: TableReference = client.get_table("DHT22_sensor_data.sensor_data")
    client.insert_rows(table=sensor_data, rows=[payload])

    return "OK", 200


if __name__ == "__main__":
    app = flask.Flask(__name__)

    @app.route("/")
    def upload_endpoint():
        return upload(flask.request)

    app.run()
