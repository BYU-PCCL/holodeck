import Holodeck
import time
import threading

if __name__ == "__main__":

    def android():
        print "Starting and waiting for Android to connect..."
        agent = Holodeck.AndroidAgent(hostname="localhost", port=8989, agentName="Android").waitFor("Connect")
        print "Connected to Android."

        # Note: this command will affect ALL agents in the world
        print "Setting the simulator to pause every 1 frame after a command"
        agent.worldCommand().setAllowedTicksBetweenCommands(0).send()
        agent.configure().setCollisionsVisible(False).send()

        def onCamera(data):
            print data

        def onHit(data):
            print data

        def onRelativePosition(data):
            print data

        # Subscribe the function onCamera to the CameraSensorArray2D sensor messages
        agent.subscribe("CameraSensorArray2D", onCamera)

        # Subscribe the function onHit to the PressureSensor messages
        agent.subscribe("PressureSensor", onHit)

        # Subscribe the function onRelativePosition to the PressureSensor messages
        agent.subscribe("RelativeSkeletalPositionSensor", onRelativePosition)

        for _ in range(10):
            print "Commanding the arms forward"
            agent.command().setBoneConstraint("upperarm_l", 0, 0, 0, 1, 100000)\
                .setBoneConstraint("upperarm_r", 0, 0, 0, 1, 100000)\
                .send()
            time.sleep(1)
            print "Commanding the arms backward"
            agent.command().setBoneConstraint("upperarm_l", 0, -40, 70, 1, 100000)\
                .setBoneConstraint("upperarm_r", 0, -40, 70, 1, 100000)\
                .send()
            time.sleep(1)

        print "Killing the Android"
        agent.kill()
        print "Android killed."


    def uav():
        print "Starting and waiting for UAV to connect..."
        agent = Holodeck.UAVAgent(hostname="localhost", port=8989, agentName="UAV").waitFor("Connect")
        print "Connected to UAV."
        # Note: this command will affect ALL agents in the world
        print "Setting the simulator to not pause at all after a command"
        agent.worldCommand()\
            .setAllowedTicksBetweenCommands(0)\
            .send()

        def onCamera(data):
            print data

        # Subscribe the function onCamera to the CameraSensorArray2D sensor messages
        agent.subscribe("CameraSensorArray2D", onCamera)

        for _ in range(10):
            print "Commanding the UAV to rotate"
            agent.command()\
                .setLocalRotation(5,5,5)\
                .send()
            time.sleep(1)

        print "Killing the UAV"
        agent.kill()
        print "UAV killed."

    android()
    uav()
