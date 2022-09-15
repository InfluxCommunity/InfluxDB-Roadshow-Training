from bdb import GENERATOR_AND_COROUTINE_FLAGS
import faulthandler
import os
import threading
from threading import Event


from random import  randint
from time import sleep
from mqtt_producer import mqtt_publisher




machine_id_counter = 1




class machine():
    def __init__ (self) -> None:
        global machine_id_counter
        self.machine_id = "machine" + str(machine_id_counter)
        machine_id_counter+=1
        self.temperature = 0
        self.load = 0
        self.power = 0
        self.vibration = 0

    def returnMachineID(self):
        return self.machine_id

   
    def returnTemperature(self):
        currentLoad = self.load
        if currentLoad > 100: self.temperature = randint(80, 90)
        elif currentLoad > 0: self.temperature = 30
        else: self.temperature = 20
        return self.temperature

    def setLoad(self, load):
        # TODO dont randomise    
        self.load = load
       

    def returnPower(self):
        currentLoad = self.load
        if currentLoad > 100: self.power = randint(2500, 3500)
        elif currentLoad == 0: self.power = 0
        else: self.power = randint(100, 500)
        
        return self.power
    
        
    def returnVibration(self):
        currentLoad = self.load
        if currentLoad > 100: self.vibration = randint(300, 500)
        elif currentLoad == 0: self.vibration  = 0
        else: self.vibration = randint(50, 80)
        return self.vibration

    def returnMachineHealth(self):
        # trigger load first as needs to be constent:
        return {"machineID": self.returnMachineID(),
                "temperature": self.returnTemperature(), 
                "power": self.returnPower(),
                "load": self.load, 
                "vibration": self.returnVibration() }



def runMachine(mqtthost, fault):
    counter = 0
    m = machine()

    mqttProducer = mqtt_publisher(address=mqtthost, port=1883, clientID=m.returnMachineID())
    mqttProducer.connect_client()
    sleeptime = randint(1, 5)
    m.setLoad(50)
    
    while (True):
        # Chance of fault
        if fault == True:
            if counter == 60:
                fault_chance = randint(0, 10)
                if fault_chance >= 2:
                    m.setLoad(120)
                else:
                    m.setLoad(randint(15, 75))


                counter = 0
        else:
             m.setLoad(randint(15, 75))

        # Publish messages
        check_machine = m.returnMachineHealth()
        print(check_machine,flush=True)
        mqttProducer.publish_to_topic(topic="machine", data=check_machine)
        
        sleep(sleeptime)
        counter = counter + 1




    


if __name__ == "__main__":
    GENERATORS = os.getenv('MACHINES', 1)
    BROKER = os.getenv('BROKER', "localhost")


    i =0
    while (i < int(GENERATORS)):
        fault = False
        generator = threading.Thread(target=runMachine, args=[BROKER, fault], daemon=True)
        generator.start()
        i = i +1
    fault = True
    generator = threading.Thread(target=runMachine, args=[BROKER, fault], daemon=True)
    generator.start()
            
    Event().wait()
