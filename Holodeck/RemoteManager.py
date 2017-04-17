import paramiko
import getpass
import subprocess
import os

class RemoteManager():


	def __init__(self,connections):
		#connections is array of tuples of type (username, hostname)
		self.connections = connections
		self.export_display = "export DISPLAY=:0; "
		self.binary_location = "/mnt/pccfs/backed_up/derek/MazeWorld_sphere_v1.00/LinuxNoEditor/Holodeck/Binaries/Linux/Holodeck"
		self.command = self.binary_location + " -opengl4 -SILENT -LOG=MyLog.txt -ResX=32 -ResY=32 &"
		self.password = "beware the pccl"
	
	def start_remote_holodecks(self):

		self.password = "beware the pccl" #getpass.getpass("Enter password to ssh into machines: ")

		#ssh into each machine and start holodeck
		for username,hostname in self.connections:
			client = paramiko.SSHClient()
			client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			client.connect(hostname, username=username, password=self.password)
			client.exec_command(self.export_display + self.command)
			client.close()

		print("Started holodecks on clients")

		#in A3C,start up HolodeckEnvironment by passing in the correct hostname for the agent to connect to

	def close_remote_holodecks(self):

		print("Closing holodecks")
		
		#ssh into each machine and close holodeck
		for username,hostname in self.connections:
			client = paramiko.SSHClient()
			client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			client.connect(hostname, username=username, password=self.password)
			client.exec_command("pkill -f derek &")
			client.close()

		print("Closed all holodecks")

	def start_local_holodeck(self,hostname,username):
		verbose = False
		print("Starting local holodeck")
		client = paramiko.SSHClient()
		client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		client.connect(hostname, username=username, password=self.password)
		client.exec_command(self.export_display + self.command)
		client.close()
		print("Done starting local holodeck")
		# for line in stdout:
		# 	print('... ' + line.strip('\n'))

	def close_local_holodeck(self,hostname,username):
		client = paramiko.SSHClient()
		client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		client.connect(hostname, username=username, password=self.password)
		client.exec_command("pkill -f derek &")
		# for line in stdout:
		# 	print('... ' + line.strip('\n'))
		client.close()



