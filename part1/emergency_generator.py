import threading
import json

from random import  randint
from time import sleep
from faker import Faker

from kafka_producer import kafka_producer
from mqtt_producer import mqtt_publisher
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.



number_of_generators = 3
generator_id_counter = 1
fake = Faker()



class emergency_generator():
    def __init__ (self) -> None:
        global generator_id_counter, fake
         
        self.coord = fake.local_latlng(country_code='US', coords_only=False)
        self.generator_id = "generator" + str(generator_id_counter)
        generator_id_counter+=1
        self.temperature = 0
        self.pressure = 0
        
        self.base_fuel = randint(900, 1000)
        self.current_fuel = None

    def returnGeneratorID(self):
        return self.generator_id

   
    def returnTemperature(self):
        self.temperature = randint(-10, 90)
        return self.temperature

    def returnPressure(self):
        self.pressure = randint(100, 1000)
        return self.pressure
    
        
    def returnFuelLevel(self):
        fuel_used = randint(1, 10)
        if self.current_fuel == None:
            self.current_fuel = self.base_fuel - fuel_used
        else:
            if self.current_fuel <= 0:
                refill = randint(500, 1000)
                self.current_fuel = self.current_fuel + refill
            else:
                self.current_fuel = self.current_fuel - fuel_used


        return self.current_fuel



def runFuelGenerator():
    emergencyGenerator = emergency_generator()

    kafkaProducer = kafka_producer()
    mqttProducer = mqtt_publisher(address="localhost", port=1883, clientID="EdgeGateway")
    mqttProducer.connect_client()
    

    sleeptime = randint(5, 10)
    
    while (True):
        check_generator = {"generatorID": emergencyGenerator.returnGeneratorID(),"lat": float (emergencyGenerator.coord[0]), "lon": float(emergencyGenerator.coord[1]),
                                                                                                                "temperature": emergencyGenerator.returnTemperature(), 
                                                                                                                "pressure": emergencyGenerator.returnPressure(), 
                                                                                                                "fuel": emergencyGenerator.returnFuelLevel() }
        print(check_generator,flush=True)
       
        kafkaProducer.sendSample(topic="emergency_generator",data=check_generator)
        mqttProducer.publish_to_topic(topic="emergency_generator", data=check_generator)
        
        sleep(sleeptime)




    


if __name__ == "__main__":
    
    x = 0
    while (x <= number_of_generators):
       generator = threading.Thread(target=runFuelGenerator, daemon=True)
       generator.start()
       x+=1
    sleep(500000)
   # runFuelGenerator()