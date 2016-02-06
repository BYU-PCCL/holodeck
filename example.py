import Holodeck
import time

if __name__ == "__main__":
    agent = Holodeck.UAVAgent(hostname="localhost", port=8989, agentName="RobertsUAV")

    def onCamera(data):
        print data

    agent.subscribe("RawCameraSensorArray2D", onCamera)

    while True:
        agent.command().setLocalRotation(5,5,5).send()
        time.sleep(1)


    agent.kill()






