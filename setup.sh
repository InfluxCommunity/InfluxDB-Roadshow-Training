#!/usr/bin/env bash
mkdir -p ./grafana/plugins

curl -L https://github.com/influxdata/grafana-flightsql-datasource/releases/download/v0.1.5/influxdata-flightsql-datasource-0.1.5.zip -o ./grafana/plugins/influxdata-flightsql-datasource-0.1.5.zip
unzip ./grafana/plugins/influxdata-flightsql-datasource-0.1.5.zip -d ./grafana/plugins/

echo "Running training instance...."
docker-compose up -d