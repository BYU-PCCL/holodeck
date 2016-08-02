import Holodeck
import time
import threading
import math
import random as r
import json

if __name__ == "__main__":

    def uav():
        print ("Starting and waiting for UAV to connect...")
        agent = Holodeck.UAVAgent.UAVAgent(hostname="localhost", port=8989, agentName="UAV").waitFor("Connect")
        print ("Connected to UAV.")
        # Note: this command will affect ALL agents in the world
        print ("Setting the simulator to not pause at all after a command")
        agent.worldCommand()\
            .setAllowedTicksBetweenCommands(0)\
            .send()

        def onCamera(data):
            print (data)

        # Subscribe the function onCamera to the CameraSensorArray2D sensor messages
        agent.subscribe("CameraSensorArray2D", onCamera)

        for i in range(1000):
            print ("Commanding the UAV to rotate")
            agent.command()\
                .setLocalRotation(i/10,5,5)\
                .send()
            time.sleep(1)

        print ("Killing the UAV")
        agent.kill()
        print ("UAV killed.")

    #android()
    uav()