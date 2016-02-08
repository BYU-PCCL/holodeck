import Holodeck
import time

if __name__ == "__main__":
    # agent = Holodeck.UAVAgent(hostname="localhost", port=8989, agentName="RobertsUAV_7")
    #
    # def onCamera(data):
    #     print data
    #
    # agent.subscribe("RawCameraSensorArray2D", onCamera)
    #
    # while True:
    #     agent.command().setLocalRotation(5,5,5).send()
    #     time.sleep(1)
    #
    #
    # agent.kill()


    agent = Holodeck.AndroidAgent(hostname="localhost", port=8989, agentName="RobertsAndroid")

    while True:
        print agent.command().setBoneConstraint("bone1", 1, 2, 3, 2).send()
        time.sleep(1)


    agent.kill()



