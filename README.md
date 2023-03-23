# InfluxDB Road Show Training
**Note: this repoistory is used in conjunction with the Hybrid Training Course Setup instructions will be provided during the lecture**

## Setup (MacOS and Linux)
Download the repo:
```bash
git clone https://github.com/InfluxCommunity/InfluxDB-Roadshow-Training.git
cd InfluxDB-Roadshow-Training
```

First time setup
```bash
chmod +x ./setup
./setup
```

### Windows Users Only
This training enviromenmt was not designed for Windows users. However, if you would like to attempt to run this training on Windows you can try the following setup:
```
git clone https://github.com/InfluxCommunity/InfluxDB-Roadshow-Training.git
cd InfluxDB-Roadshow-Training
.\setup-windows.ps1
```

If this does not work, you may still take part in the training by using the online training environment found ["here"](https://killercoda.com/influxdata/scenario/influxdb-roadshow-training).

## Use
For first time use please make sure you use the setup script first as this installs the FlightSQL Grafana plugin. Once run you may control your demo instance with the following commands:

Spin up instance:
```bash
docker-compose up -d
```

Spin down instance:
```bash
docker-compose down -d
```
