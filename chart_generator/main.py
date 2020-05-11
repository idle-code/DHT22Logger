from flask import Request, Flask, render_template, request
from google.cloud import bigquery
from google.cloud.bigquery import TableReference
from datetime import datetime


def trim_date(timestamp: datetime) -> str:
    return timestamp.time().replace(second=0, microsecond=0).isoformat()


def generate_page(request: Request):
    client = bigquery.Client(project='idlecode-va-data-collection')
    sensor_data: TableReference = client.get_table("DHT22_sensor_data.sensor_data")

    query_job = client.query("""
SELECT
  *
FROM
  `idlecode-va-data-collection.DHT22_sensor_data.sensor_data`
WHERE
  `timestamp` > DATETIME_SUB(CURRENT_DATETIME('Europe/Warsaw'), INTERVAL 24 HOUR)
ORDER BY `timestamp` ASC
    """)
    results = query_job.result()

    rows = list(results)
    dates = list(map(trim_date, map(lambda r: r['timestamp'], rows)))
    temperature_values = list(map(lambda r: round(r['temperature'], ndigits=1), rows))
    humidity_values = list(map(lambda r: round(r['humidity'], ndigits=1), rows))

    return render_template("index.html", chart_data={
        "labels": dates,
        "temperature_values": temperature_values,
        "humidity_values": humidity_values
    })


if __name__ == "__main__":
    app = Flask(__name__)

    @app.route("/")
    def generate_page_endpoint():
        return generate_page(request)

    app.run()
