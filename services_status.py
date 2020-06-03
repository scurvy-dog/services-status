import subprocess

class Service:
	def __init__(self,name,status,uptime):
		self.name = name
		self.status = status
		self.uptime = uptime
	
	def __str__(self):
		a = self.name.ljust(22)
		b = self.status.ljust(10)
		c = self.uptime.ljust(20)
		return  "| %s| %s| %s|" % (a,b,c)
	
	def grab_status (self,process):
		# Grab Service Data
		output = subprocess.run(f'systemctl status {process}', shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8')
		output = output.splitlines()

		# Parse to easily grab service status
		output2 = output[2].split()
		self.status = output2[1]

		# Check to see if process is running with uptime
		# Check for ; in output. If true than grab uptime
		if (";" in output[2]):
			# Parse to easily grab uptime
			output3 = output[2].split(";")
			output4 = output3[1].strip()
			self.uptime = output4
		else:
			self.uptime = "Down"

# Grab Plex Service Data
output = subprocess.run(['snap', 'services'], stdout=subprocess.PIPE).stdout.decode('utf-8')
output = output.splitlines()
output2 = output[1].split()

# Grabbing PID works. The output of the ps command though seems to add 1 character per line in the output
plex_pid = subprocess.run('pidof \'Plex Media Server\'', shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8')
#print(plex_pid)
plex_uptime = subprocess.run(f'ps -o etime -p {plex_pid}', shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8')

#for i in plex_uptime:
#	print (i)


# Create class object
plex = Service("Plex Media Server",output2[2],plex_uptime[1])

# Grab Influxdb Service Data
influxdb = Service("Influxdb","","")
influxdb.grab_status("influxdb2")

# Create Grafana class object
grafana = Service("Grafana","","")
grafana.grab_status("grafana-server")

# Create SignalK.service class object
signalk_service = Service("SignalK-Service","","")
signalk_service.grab_status("signalk.service")

# Create SignalK.socket class object
signalk_socket = Service("SignalK-Socket","","")
signalk_socket.grab_status("signalk.socket")



#Print Table
table_row = "-----------------------------------------------------------"
table_header = "| Service Name          |   Status  |        Uptime       |"

print (table_row)
print (table_header)
print (table_row)
print (plex)
print (table_row)
print (influxdb)
print (table_row)
print (grafana)
print (table_row)
print (signalk_service)
print (table_row)
print (signalk_socket)
print (table_row)
