import Holodeck

if __name__ == "__main__":
    agent = Holodeck.UAVAgent(hostname="localhost", port=8989, agentName="RobertsUAV")

    while(True):
        agent.command().setLocalRotation(5,5,5).send()
        for x in range(10):
            print agent.receive()





