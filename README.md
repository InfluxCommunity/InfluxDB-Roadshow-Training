# InfluxDB Road Show Training
**Note: this repoistory is used in conjunction with the Hybrid Training Course Setup instructions will be provided during the lecture**

## Setup
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
