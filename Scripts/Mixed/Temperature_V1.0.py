# $language = "Python"
# $interface = "1.0"


import csv
import time
from math import floor
import os
from datetime import datetime

#Sends Command to CSR and handles different CSR Outputs
def read_from_csr(command, read_string = "RP/0/RP0/CPU0:", timeout_timer = 20):
	crt.Screen.Send(command + chr(13))
	index = 3
	information = ""
	while index >=3:
		information = information + crt.Screen.ReadString(["disconnect", read_string,"--More--"],timeout_timer)
		index = crt.Screen.MatchIndex
		if(index == 2):
			return information
		elif(index == 3):
			crt.Screen.Send(" ")
		else:
			return "Disconnected!"

#converts a paragraph of text to a list where each element is a a line of text in the paragraph
def split_text_by_lines(raw_text, header_lines = 0):
	new_text = raw_text.split("\n")[header_lines:-1]
	#new_text = [" ".join(line.split()).split(" ") for line in new_text] 
	return new_text


## Class for CSR ##
class csr:

	def __init__(self):
		self.MB_Inlet_Temp_Sensor = "Not Reachable"



	def set_environment_temperatures(self):
		raw_interface = read_from_csr("sh env all")
		if(raw_interface == "Disconnected!"):
			 self.MB_Inlet_Temp_Sensor = "Not Reachable"
			
		else:
			#self.controller_set = True
			splitted_device_info = split_text_by_lines(raw_interface)
			for line in splitted_device_info:
				if "MB-Inlet Temp Sensor" in line:
					splitted_line = " ".join(line.split("Temp Sensor")[1].split()).split(" ")
					self.MB_Inlet_Temp_Sensor = splitted_line[0] 
				


# Class for each site ##
class cell_site:
	def __init__(self, name):
		self.name     		= name
		self.csr_connected	= True
		self.csr			= csr()			

################################# Main Class #################################	
def Main():
	
#crt.Screen.Synchronous = True
	file_path = crt.Dialog.FileOpenDialog("Select csv file with your site list. Use first row as header row, 1st column site name, 2nd column ip address","Open", "", "CSV Files Comma Delimited (*.csv)|*.csv||")
	Save_path = os.path.dirname(file_path)
	#dump_file_path = crt.Dialog.FileOpenDialog("Select csv file to dump report to.","Open", "", "CSV Files Comma Delimited (*.csv)|*.csv||")
	with open(file_path) as csvfile:
		site_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
		site_list = []
		line_count = 0
		for row in site_reader:
			if line_count == 0:
				header_length = len(row)
			else:
				site_list.append(cell_site(row[0]))
			line_count = line_count+1
	csvfile.close()
	username = crt.Dialog.Prompt("Enter your Username")
	pwd = crt.Dialog.Prompt("Enter your password", "Password Prompt","",True)
	crt.Screen.Send(chr(13))

	total_sites = len(site_list)
	current_site_count = 0
############### Loop that checks all sites in the csv list

	
	for site in site_list:
		max_tries 		= 3
		counter 		= 0
		crt.Screen.Send("ssh -o ConnectTimeout=10 -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null " + username + "@" + site.name + "-cs000-csr001-lo10.net.corp.dish-wireless.net" + chr(13))
		while counter < max_tries :
		
			site_reachable = crt.Screen.ReadString(["Are you sure you want to continue connecting (yes/no/[fingerprint])?", "Host key verification failed.","kex_exchange_identification: Connection closed by remote host", "exceptions","Password:"],5)
			index = crt.Screen.MatchIndex
			if(index == 0):
				counter = max_tries
#Enter code for the case the site times out and cannot be reached
				site.reachable = False
				crt.Screen.Send(chr(3))
				crt.Screen.Send(chr(13))
				break
				  

			elif(index == 1):
#counter =  max_tries
				crt.Screen.Send("yes" + chr(13))
				crt.Screen.Send("ssh " + username + "@" + site.name + "-cs000-csr001-lo10.net.corp.dish-wireless.net" + chr(13))
			elif(index == 2):
				counter += 1
#Comment the line below, and uncomment the line below that if you want to ask the users if they want to refresh remote host identification key instead of automatically refreshing it
				refresh_remote_host_identification_value = 6
#refresh_remote_host_identification_value = crt.Dialog.MessageBox(site.name + "'s Remote Hosts Identification has changed since you last download it. Do you wish to refresh it?", "WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!",  48|4) #Yes=6, No = 7
				if refresh_remote_host_identification_value == 6:
					for line in split_text_by_lines(site_reachable):
						if "ssh-keygen -f" in line:
							site_reachable = ""
							#crt.Screen.WaitForString("dishjmp",10)
							crt.Screen.Send(line + chr(13))
							crt.Screen.WaitForString("dishjmp",10)
							crt.Screen.Send("ssh -o ConnectTimeout=10 -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null " + username + "@" + site.name + "-cs000-csr001-lo10.net.corp.dish-wireless.net" + chr(13))
							break
				else:
					site.reachable = False
					break#exit while loop

			elif(index == 3):
				counter += 1
				crt.Screen.Send("ssh -o ConnectTimeout=10 -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null " + username + "@" + site.name + "-cs000-csr001-lo10.net.corp.dish-wireless.net" + chr(13))
			
			elif(index == 4):
				counter = max_tries
				crt.Screen.WaitForString("Password:")
				crt.Screen.Send(pwd + chr(13))
				crt.Screen.WaitForString("RP/0/RP0/CPU0:")
				site.csr.set_environment_temperatures()
				crt.Screen.Send("q" + chr(13))
				crt.Screen.WaitForString("closed.")
			
			else:
				counter = max_tries
				crt.Screen.Send(pwd + chr(13))
				crt.Screen.WaitForString("RP/0/RP0/CPU0:")
				site.csr.set_environment_temperatures()
				crt.Screen.Send("q" + chr(13))
				crt.Screen.WaitForString("closed.")

		current_site_count += 1



	file_is_writable = False
	####### Writes information to file_path, if the file is open, prompt user to close file.
	crt.Session.SetStatusText("Writing to file")

	now = datetime.now()
	print("now = ", now)
	#x = now.replace("-", "")
	year = str(now.year)
	Month = str(now.month)
	Day = str(now.day)
	hr = str(now.hour)
	Minute = str(now.minute)
	Second = str(now.second)

	if len(Month)==1:
		Month = "0" + Month
		
	if len(Day)==1:
		Day = "0" + Day
		
	if len(hr)==1:
		hr = "0" + hr
		
	if len(Minute)==1:
		Minute = "0" + Minute
		
	if len(Second)==1:
		Second = "0" + Second

	#path = str('C:\\Users\\')
	filename = str('\\Output_' + year + Month + Day + "_" + hr + Minute + Second + '.csv')
	dump_file_path =  Save_path + filename

	while file_is_writable == False:			
		try:
			file_is_writable = True
			with open(dump_file_path, 'w') as csvfile:
				site_writer = csv.writer(csvfile, delimiter =',', quotechar='|', lineterminator='\n')
				site_writer.writerow(['Site ID', 'MB-Inlet Temp Sensor',])
				
				for site in site_list:
					site_writer.writerow([site.name, site.csr.MB_Inlet_Temp_Sensor])
					
		except IOError as e:
			crt.Dialog.MessageBox(" cannot be edited because is open by another process. Please close it and press OK")
			file_is_writable = 0
	
Main()