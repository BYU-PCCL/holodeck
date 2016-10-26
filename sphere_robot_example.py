import Holodeck
import time
import threading
import math
import random as r
import json

if __name__ == "__main__":

    def sphereRobot():
        print("Starting and waiting for SphereRobot to connect...")
        agent = Holodeck.SphereRobotAgent.SphereRobotAgent(hostname="localhost", port=8989, agentName="BB-8",
                                                   global_state_sensors={"CameraSensorArray2D", "Score", "Terminal"}).waitFor("Connect")
        print("Connected to SphereRobot.")

        # Note: this command will affect ALL agents in the world
        print("Setting the simulator to pause every 1 frame after a command")
        agent.worldCommand().setAllowedTicksBetweenCommands(1).send()
        
        #some other example world commands
        #agent.worldCommand().restartLevel().send()
        #agent.worldCommand().loadLevel("MyNextLevel").send()

        def onState(data, type=None):
            #print("i just got your state message")
            print("Message from " + type)
            print(data)

        #agent.subscribe('State', onState)

        for i in range(300):

          output = agent.getNextState()
          print("---------- State " + str(i) + " ----------")
          if "CameraSensorArray2D" in output and len(output["CameraSensorArray2D"]) > 0:
            print "Saving robot image..."
            with open("robot_sight.jpg", "wb") as myfile:
              myfile.write(output["CameraSensorArray2D"][0])

          if "Score" in output:
            print "Score: " + str(output["Score"])

          if "Terminal" in output:
            print "Terminal: " + str(output["Terminal"])

          # command = ""
          # command = str(raw_input()).strip()
          # print(command)
          # if command == "f":
          #   agent.command().move(2,0).send()
          # elif command == "r":
          #   agent.command().move(0,2).send()
          # elif command == "l":
          #   agent.command().move(0,-2).send()
          # else:
          #   print("Invalid command")

          agent.command().move(2,0).send()
 
        print("Killing the SphereRobot")
        agent.kill()
        print("SphereRobot killed.")

    sphereRobot()
