# MQTT Emergency Generator Simulator

This repoistory will allow you to spin up Emergency Generators producing fake IoT data. Each generator will write to its own MQTT topic the following values: 

1. Load
2. Voltage
3. Fuel Level
4. Temperature

The payload will look like this:

```json
{"generatorID": "generator1", "lat": 40.68066, "lon": -73.47429, "temperature": 186, "power": 186, "load": 2, "fuel": 277}
```

There are two ways to setup this Sim: Docker + Locally

## Option1: Locally

1. Install the Mosquitto MQTT Broker onto your device:

```bash
sudo apt-add-repository ppa:mosquitto-dev/mosquitto-ppa
sudo apt-get update
sudp apt-get install mosquitto
```

2. Start the Mosquitto broker:

```bash
sudo systemctl enable Mosquitto
sudo systemctl start Mosquitto
```

3. Clone this repo to your local system:

```bash
git clone https://github.com/Jayclifford345/mqtt-emergency-generator.git
```

4. Naviage to this folder

```bash
cd mqtt-emergency-generator/tree/master/generator_simulator
```

5. Install the pip requirements

```bash
RUN python3 -m pip install --no-cache-dir -r requirements.txt
```

6. Setup your enviroment variables

```bash
export GENERATORS=3
export BROKER=localhost
```

7. Run the the simulator

```bash
python3 src/emergency_generator.py
```

## Option2: Docker (Recommended)


1. Clone this repo to your system

```bash
git clone https://github.com/Jayclifford345/mqtt-emergency-generator.git
```

2. Build the simulator docker image:

```bash
docker build generator_simulator/. -t emergency-generator:latest
```

3. Deploy the docker-compose file:

```bash
docker-compose up -d
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
