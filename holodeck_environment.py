import Holodeck.holodeck_agents as ha
import numpy as np

class HolodeckEnvironment:

    def __init__(self, agent_type, hostname="localhost", port=8989, agent_name="DefaultAgent",global_state_sensors={}):
        """

        :param agent_type: str()
        :param hostname:
        :param port:
        :param agent_name:
        """
        agents = {"UAV": ha.UAVAgent, "SPHERE": ha.SphereRobotAgent, "ANDROID": ha.AndroidAgent}
        if agent_type in agents.keys():
            agent = agents[agent_type]
        else:
            raise KeyError(agent_type + " is not a valid agent type")
        self.AGENT = agents[agent_type](hostname=hostname, port=port, agentName=agent_name,global_state_sensors=global_state_sensors)
        self.agent_type = agent_type

        #default have simulator to pause every 1 frame
        self.AGENT.worldCommand().setAllowedTicksBetweenCommands(1).send()

        # self.HOSTNAME = hostname
        # self.PORT = port
        # self.AGENT_NAME = agent_name

    def get_action_dim(self):
        return self.AGENT.get_action_space_dim()

    def get_state_dim(self):
        return self.AGENT.get_state_space_dim()

    def act(self, action):
        #TO DO: convert states to numpy arrays
        assert action.shape == self.get_action_dim()

        self.AGENT.act(action)
        return self.AGENT.get_next_state()

    def reset(self):
        pass