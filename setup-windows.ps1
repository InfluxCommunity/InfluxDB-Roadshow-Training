mkdir -Force ./grafana/plugins

Invoke-WebRequest https://github.com/influxdata/grafana-flightsql-datasource/releases/download/v0.1.5/influxdata-flightsql-datasource-0.1.5.zip -OutFile ./grafana/plugins/influxdata-flightsql-datasource-0.1.5.zip
Expand-Archive ./grafana/plugins/influxdata-flightsql-datasource-0.1.5.zip -DestinationPath ./grafana/plugins/

Write-Output "Running training instance...."
docker-compose up -d