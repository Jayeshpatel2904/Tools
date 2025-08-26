# $language = "Python"
# $interface = "1.0"

########################------------------------------------------------------###################################
######################## For issue Please contact jayeshkumar.patel@dish.com ####################################
########################------------------------------------------------------###################################

import csv
import time
from math import floor
import os
from datetime import datetime
import sys


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
		self.Alpha_TB_MAC = "Not Reachable"
		self.Beta_TB_MAC = "Not Reachable"
		self.Gamma_TB_MAC = "Not Reachable"
		self.Alpha_MB_MAC = "Not Reachable"
		self.Beta_MB_MAC = "Not Reachable"
		self.Gamma_MB_MAC = "Not Reachable"

		self.Alpha_TB_IP = "Not Reachable"
		self.Beta_TB_IP = "Not Reachable"
		self.Gamma_TB_IP = "Not Reachable"
		self.Alpha_MB_IP = "Not Reachable"
		self.Beta_MB_IP = "Not Reachable"
		self.Gamma_MB_IP = "Not Reachable"

		self.Alpha_MB_DCPower = "Not Reachable"
		self.Alpha_MB_SN = "Not Reachable"
		self.Beta_MB_DCPower = "Not Reachable"
		self.Beta_MB_SN = "Not Reachable"
		self.Gamma_MB_DCPower = "Not Reachable"
		self.Gamma_MB_SN = "Not Reachable"
		self.Alpha_TB_DCPower = "Not Reachable"
		self.Alpha_TB_SN = "Not Reachable"
		self.Beta_TB_DCPower = "Not Reachable"
		self.Beta_TB_SN = "Not Reachable"
		self.Gamma_TB_DCPower = "Not Reachable"
		self.Gamma_TB_SN = "Not Reachable"
		
		self.BV95 = "Not Reachable"
		self.BV95MAC = "Not Reachable"
		self.BV95IP = "Not Reachable"
		self.Port18 = "Not Reachable"
		self.Port3 = "Not Reachable"
		self.Port4 = "Not Reachable"
		self.Port5 = "Not Reachable"
		self.Port6 = "Not Reachable"
		self.Port7 = "Not Reachable"
		self.Port8 = "Not Reachable"
		self.Port9 = "Not Reachable"
		self.Port13 = "Not Reachable"
		self.Port14 = "Not Reachable"
		self.Port15 = "Not Reachable"
		self.Port19 = "Not Reachable"
		self.Port24 = "Not Reachable"
		self.Port27 = "Not Reachable"
		self.Port16 = "Not Reachable"
		self.Port17 = "Not Reachable"
		self.VMWAREPORT = "Not Reachable"
		self.VMWAREMAC = "Not Reachable"
		self.VMWAREIP = "Not Reachable"
		self.K8S = "Not Reachable"
		self.PortBV201 = "Not Reachable"
		self.PortBV311 = "Not Reachable"
		self.PortBV318 = "Not Reachable"
		self.PortBV323 = "Not Reachable"

		self.Port29 = "Not Reachable"
		self.Satellite = "Not Reachable"
		self.GPSstatus = "Not Reachable"
		self.GPSphaselock = "Not Reachable"
		self.GPSMajorAlarm = "Not Reachable"
		self.GPSMinorAlarm = "Not Reachable"

		self.PORT18MAC = "Not Reachable"
		self.SITEBOSSMAC = "Not Reachable"
		self.SITEBOSSIP = "Not Reachable"
		self.BMCPORT = "Not Reachable"
		self.SITEBOSSPORT = "Not Reachable"

		self.storm_control = "Not Reachable"

		


	def get_temperatures(self):
			ReadData = read_from_csr("sh env all")
			splitted_device_info = split_text_by_lines(ReadData)
			for line in splitted_device_info:
				if "MB-Inlet Temp Sensor" in line:
					splitted_line = " ".join(line.split("Temp Sensor")[1].split()).split(" ")
					self.MB_Inlet_Temp_Sensor = splitted_line[0] 
				
	def get_mac_ip(self):
			ReadData = read_from_csr("sh l2vpn mac mac all location 0/RP0/CPU0")
			splitted_device_info = split_text_by_lines(ReadData)
			for line in splitted_device_info:
				if "0/0/0/4.201" in line:
					splitted_line = " ".join(line.split("0/0/0/4.201")[1].split()).split(" ")
					self.Alpha_TB_MAC = splitted_line[0][0:14]
			
				if "0/0/0/6.201" in line:
					splitted_line = " ".join(line.split("0/0/0/6.201")[1].split()).split(" ")
					self.Beta_TB_MAC = splitted_line[0][0:14]
		
				if "0/0/0/8.201" in line:
					splitted_line = " ".join(line.split("0/0/0/8.201")[1].split()).split(" ")
					self.Gamma_TB_MAC = splitted_line[0][0:14]
			
				if "0/0/0/5.201" in line:
					splitted_line = " ".join(line.split("0/0/0/5.201")[1].split()).split(" ")
					self.Alpha_MB_MAC = splitted_line[0][0:14]

				if "0/0/0/7.201" in line:
					splitted_line = " ".join(line.split("0/0/0/7.201")[1].split()).split(" ")
					self.Beta_MB_MAC = splitted_line[0][0:14]

				if "0/0/0/9.201" in line:
					splitted_line = " ".join(line.split("0/0/0/9.201")[1].split()).split(" ")
					self.Gamma_MB_MAC = splitted_line[0][0:14]

				if "Te0/0/0/14.96" in line:
					splitted_line = " ".join(line.split("Te0/0/0/14.96")[1].split()).split(" ")
					self.VMWAREPORT = "14.96"
					self.VMWAREMAC = splitted_line[0][0:14]

				if "Te0/0/0/15.96" in line:
					splitted_line = " ".join(line.split("Te0/0/0/15.96")[1].split()).split(" ")
					self.VMWAREPORT = "15.96"
					self.VMWAREMAC = splitted_line[0][0:14]

				if "Gi0/0/0/2" in line:
					splitted_line = " ".join(line.split("Gi0/0/0/2")[1].split()).split(" ")
					self.BV95MAC = splitted_line[0][0:14]
				
				if "Gi0/0/0/17" in line:
					splitted_line = " ".join(line.split("Gi0/0/0/17")[1].split()).split(" ")
					self.BV95MAC = splitted_line[0][0:14]

				if "Gi0/0/0/0" in line:
					splitted_line = " ".join(line.split("Gi0/0/0/0")[1].split()).split(" ")
					self.SITEBOSSMAC = splitted_line[0][0:14]
				
				if "Gi0/0/0/16" in line:
					splitted_line = " ".join(line.split("Gi0/0/0/16")[1].split()).split(" ")
					self.SITEBOSSMAC = splitted_line[0][0:14]

				
				if "Te0/0/0/18" in line:
					splitted_line = " ".join(line.split("Te0/0/0/18")[1].split()).split(" ")
					self.PORT18MAC = splitted_line[0][0:14]
				

			ReadData = read_from_csr("sh l2vpn mac mac-ipv4 all location 0/RP0/CPU0")
			splitted_device_info = split_text_by_lines(ReadData)
			for line in splitted_device_info:
				if self.Alpha_TB_MAC in line:
					splitted_line = " ".join(line.split(self.Alpha_TB_MAC)[1].split()).split(" ")
					self.Alpha_TB_IP = splitted_line[0]

				if self.Beta_TB_MAC in line:
					splitted_line = " ".join(line.split(self.Beta_TB_MAC)[1].split()).split(" ")
					self.Beta_TB_IP = splitted_line[0]

				if self.Gamma_TB_MAC in line:
					splitted_line = " ".join(line.split(self.Gamma_TB_MAC)[1].split()).split(" ")
					self.Gamma_TB_IP = splitted_line[0]

				if self.Alpha_MB_MAC in line:
					splitted_line = " ".join(line.split(self.Alpha_MB_MAC)[1].split()).split(" ")
					self.Alpha_MB_IP = splitted_line[0]

				if self.Beta_MB_MAC in line:
					splitted_line = " ".join(line.split(self.Beta_MB_MAC)[1].split()).split(" ")
					self.Beta_MB_IP = splitted_line[0]

				if self.Gamma_MB_MAC in line:
					splitted_line = " ".join(line.split(self.Gamma_MB_MAC)[1].split()).split(" ")
					self.Gamma_MB_IP = splitted_line[0]

				if self.VMWAREMAC in line:
					splitted_line = " ".join(line.split(self.VMWAREMAC)[1].split()).split(" ")
					self.VMWAREIP = splitted_line[0]

				if self.BV95MAC in line:
					splitted_line = " ".join(line.split(self.BV95MAC)[1].split()).split(" ")
					self.BV95IP = splitted_line[0]

				if self.SITEBOSSMAC in line:
					splitted_line = " ".join(line.split(self.SITEBOSSMAC)[1].split()).split(" ")
					self.SITEBOSSIP = splitted_line[0]

	
	def get_portsinfo(self):
			ReadData = read_from_csr("sh int description")
			splitted_device_info = split_text_by_lines(ReadData)
			for line in splitted_device_info:
				if "BV95" in line:
					splitted_line = " ".join(line.split("BV95")[1].split()).split(" ")
					self.BV95 = splitted_line[0]

				if "BV96" in line:
					splitted_line = " ".join(line.split("BV96")[1].split()).split(" ")
					self.BV96 = splitted_line[0]

				if "Gi0/0/0/0" in line:
					splitted_line = " ".join(line.split("Gi0/0/0/0 ")[1].split()).split(" ")
					self.SITEBOSSPORT = splitted_line[0]

				if "Gi0/0/0/16" in line:
					splitted_line = " ".join(line.split("Gi0/0/0/16 ")[1].split()).split(" ")
					self.SITEBOSSPORT = splitted_line[0]

				if "Gi0/0/0/17" in line:
					splitted_line = " ".join(line.split("Gi0/0/0/17")[1].split()).split(" ")
					self.BMCPORT = splitted_line[0]

				if "0/0/0/18" in line:
					splitted_line = " ".join(line.split("0/0/0/18")[1].split()).split(" ")
					self.Port18 = splitted_line[0]

				if "Gi0/0/0/2" in line:
					splitted_line = " ".join(line.split("Gi0/0/0/2")[1].split()).split(" ")
					self.BMCPORT = splitted_line[0]

				if "Gi0/0/0/3" in line:
					splitted_line = " ".join(line.split("Gi0/0/0/3")[1].split()).split(" ")
					self.Port3 = splitted_line[0]

				if "BV201" in line:
					splitted_line = " ".join(line.split("BV201")[1].split()).split(" ")
					self.PortBV201 = splitted_line[0]

				if "BV311" in line:
					splitted_line =  " ".join(line.split("BV311")[1].split()).split(" ")
					self.PortBV311 = splitted_line[0]

				if "BV318" in line:
					splitted_line = " ".join(line.split("BV318")[1].split()).split(" ")
					self.PortBV318 = splitted_line[0]

				if "BV323" in line:
					splitted_line = " ".join(line.split("BV323")[1].split()).split(" ")
					self.PortBV323 = splitted_line[0]
###################################### RADIO PORT 4 ##########################################################
				if "Te0/0/0/4" in line:
					splitted_line = " ".join(line.split("Te0/0/0/4")[1].split()).split(" ")
					#crt.Dialog(line)                   
					
					if(self.Port4 == ''):
						self.Port4 = splitted_line[0]
						if(self.Port4 == 'up') or (self.Port4 == 'down') or (self.Port4 == 'admin-down'):
							self.Port4 = self.Port4
						else:
							self.Port4 = splitted_line[1]
					
					elif(self.Port4 == 'down') or (self.Port4 == 'admin-down'):
						self.Port4 = self.Port4
					else:
						self.Port4 = splitted_line[1]


###################################### RADIO PORT 5 ##########################################################
				if "Te0/0/0/5" in line:
					splitted_line = " ".join(line.split("Te0/0/0/5")[1].split()).split(" ")
					#crt.Dialog(line)                   
					
					if(self.Port5 == ''):
						self.Port5 = splitted_line[0]
						if(self.Port5 == 'up') or (self.Port5 == 'down') or (self.Port5 == 'admin-down'):
							self.Port5 = self.Port5
						else:
							self.Port5 = splitted_line[1]
					
					elif(self.Port5 == 'down') or (self.Port5 == 'admin-down'):
						self.Port5 = self.Port5
					else:
						self.Port5 = splitted_line[1]



###################################### RADIO PORT 6 ##########################################################
				if "Te0/0/0/6" in line:
					splitted_line = " ".join(line.split("Te0/0/0/6")[1].split()).split(" ")
					#crt.Dialog(line)                   
					
					if(self.Port6 == ''):
						self.Port6 = splitted_line[0]
						if(self.Port6 == 'up') or (self.Port6 == 'down') or (self.Port6 == 'admin-down'):
							self.Port6 = self.Port6
						else:
							self.Port6 = splitted_line[1]
					
					elif(self.Port6 == 'down') or (self.Port6 == 'admin-down'):
						self.Port6 = self.Port6
					else:
						self.Port6 = splitted_line[1]

###################################### RADIO PORT 7 ##########################################################
				if "Te0/0/0/7" in line:
					splitted_line = " ".join(line.split("Te0/0/0/7")[1].split()).split(" ")
					#crt.Dialog(line)                   
					
					if(self.Port7 == ''):
						self.Port7 = splitted_line[0]
						if(self.Port7 == 'up') or (self.Port7 == 'down') or (self.Port7 == 'admin-down'):
							self.Port7 = self.Port7
						else:
							self.Port7 = splitted_line[1]
					
					elif(self.Port7 == 'down') or (self.Port7 == 'admin-down'):
						self.Port7 = self.Port7
					else:
						self.Port7 = splitted_line[1]

###################################### RADIO PORT 8 ##########################################################
				if "Te0/0/0/8" in line:
					splitted_line = " ".join(line.split("Te0/0/0/8")[1].split()).split(" ")
					#crt.Dialog(line)                   
					
					if(self.Port8 == ''):
						self.Port8 = splitted_line[0]
						if(self.Port8 == 'up') or (self.Port8 == 'down') or (self.Port8 == 'admin-down'):
							self.Port8 = self.Port8
						else:
							self.Port8 = splitted_line[1]
					
					elif(self.Port8 == 'down') or (self.Port8 == 'admin-down'):
						self.Port8 = self.Port8
					else:
						self.Port8 = splitted_line[1]



###################################### RADIO PORT 9 ##########################################################
				if "Te0/0/0/9" in line:
					splitted_line = " ".join(line.split("Te0/0/0/9")[1].split()).split(" ")
					#crt.Dialog(line)                   
					
					if(self.Port9 == ''):
						self.Port9 = splitted_line[0]
						if(self.Port9 == 'up') or (self.Port9 == 'down') or (self.Port9 == 'admin-down'):
							self.Port9 = self.Port9
						else:
							self.Port9 = splitted_line[1]
					
					elif(self.Port9 == 'down') or (self.Port9 == 'admin-down'):
						self.Port9 = self.Port9
					else:
						self.Port9 = splitted_line[1]



###################################### RADIO PORT 13 ##########################################################
				if "Te0/0/0/13" in line:
					splitted_line = " ".join(line.split("Te0/0/0/13")[1].split()).split(" ")
					#crt.Dialog(line)                   
					
					if(self.Port13 == ''):
						self.Port13 = splitted_line[0]
						if(self.Port13 == 'up') or (self.Port13 == 'down') or (self.Port13 == 'admin-down'):
							self.Port13 = self.Port13
						else:
							self.Port13 = splitted_line[1]
					
					elif(self.Port13 == 'down') or (self.Port13 == 'admin-down'):
						self.Port13 = self.Port13
					else:
						self.Port13 = splitted_line[1]

###################################### RADIO PORT 14 ##########################################################
				if "Te0/0/0/14" in line:
					splitted_line = " ".join(line.split("Te0/0/0/14")[1].split()).split(" ")

					
					if "Te0/0/0/14.311" in line:
						self.K8S = "Port 14.311"          
					
					if(self.Port14 == ''):
						self.Port14 = splitted_line[0]
						if(self.Port14 == 'up') or (self.Port14 == 'down') or (self.Port14 == 'admin-down'):
							self.Port14 = self.Port14
						else:
							self.Port14 = splitted_line[1]
					
					elif(self.Port14 == 'down') or (self.Port14 == 'admin-down'):
						self.Port14 = self.Port14
					else:
						self.Port14 = splitted_line[1]


###################################### RADIO PORT 15 ##########################################################
				if "Te0/0/0/15" in line:
					splitted_line = " ".join(line.split("Te0/0/0/15")[1].split()).split(" ")
					if "Te0/0/0/15.311" in line:
						self.K8S = "Port 15.311"				                 
					
					if(self.Port15 == ''):
						self.Port15 = splitted_line[0]
						if(self.Port15 == 'up') or (self.Port15 == 'down') or (self.Port15 == 'admin-down'):
							self.Port15 = self.Port15
						else:
							self.Port15 = splitted_line[1]
					
					elif(self.Port15 == 'down') or (self.Port15 == 'admin-down'):
						self.Port15 = self.Port15
					else:
						self.Port15 = splitted_line[1]


###################################### RADIO PORT 19 ##########################################################
				if "0/0/0/19" in line:
					splitted_line = " ".join(line.split("0/0/0/19")[1].split()).split(" ")

					if(self.Port19 == ''):
						self.Port19 = splitted_line[0]
						if(self.Port19 == 'up') or (self.Port19 == 'down') or (self.Port19 == 'admin-down'):
							self.Port19 = self.Port19
						else:
							self.Port19 = splitted_line[1]
					
					elif(self.Port19 == 'down') or (self.Port19 == 'admin-down'):
						self.Port19 = self.Port19
					else:
						self.Port19 = splitted_line[1]

###################################### RADIO PORT 24 ##########################################################
				if "TF0/0/0/24" in line:
					splitted_line = " ".join(line.split("TF0/0/0/24")[1].split()).split(" ")

					if(self.Port24 == ''):
						self.Port24 = splitted_line[0]
						if(self.Port24 == 'up') or (self.Port24 == 'down') or (self.Port24 == 'admin-down'):
							self.Port24 = self.Port24
						else:
							self.Port24 = splitted_line[1]
					
					elif(self.Port24 == 'down') or (self.Port24 == 'admin-down'):
						self.Port24 = self.Port24
					else:
						self.Port24 = splitted_line[1]

###################################### RADIO PORT 27 ##########################################################
				if "0/0/0/27" in line:
					splitted_line = " ".join(line.split("0/0/0/27")[1].split()).split(" ")

					if(self.Port27 == ''):
						self.Port27 = splitted_line[0]
						if(self.Port27 == 'up') or (self.Port27 == 'down') or (self.Port27 == 'admin-down'):
							self.Port27 = self.Port27
						else:
							self.Port27 = splitted_line[1]
					
					elif(self.Port27 == 'down') or (self.Port27 == 'admin-down'):
						self.Port27 = self.Port27
					else:
						self.Port27 = splitted_line[1]
###################################### RADIO PORT 27 ##########################################################
				if "0/0/0/29" in line:
					splitted_line = " ".join(line.split("0/0/0/29")[1].split()).split(" ")
					#crt.Dialog.MessageBox(str(line), "File Saved Below Location" )
					if(self.Port29 == ''):
						self.Port29 = splitted_line[0]
						#crt.Dialog.MessageBox(str(splitted_line[0]), "File Saved Below Location" )
						if(self.Port29 == 'up') or (self.Port29 == 'down') or (self.Port29 == 'admin-down'):
							self.Port29 = self.Port29
						else:
							self.Port29 = splitted_line[1]
					
					elif(self.Port29 == 'down') or (self.Port29 == 'admin-down'):
						self.Port29 = self.Port29
					else:
						self.Port29 = splitted_line[1]
				
	def get_GPSinfo(self):
			ReadData = read_from_csr("sh gnss-receiver")
			splitted_device_info = split_text_by_lines(ReadData)
			count = 0
			for line in splitted_device_info:
				if "Satellite Count:" in line:
					#splitted_line = line.replace(" ", "")
					splitted_line = " ".join(line.split("Satellite Count:")[1].split()).split(" ")
					
					self.Satellite = splitted_line[0]
				


				if "Major Alarms:" in line:
					splitted_line = " ".join(line.split("Major Alarms:")[1].split()).split(" ")
					self.GPSMajorAlarm = splitted_line[0]

				if "Minor Alarms:" in line:
					splitted_line = " ".join(line.split("Minor Alarms:")[1].split()).split(" ")
					self.GPSMinorAlarm = splitted_line[0]

				if "Status:" in line:
					count = count + 1
					if (count == 1):
						splitted_line = " ".join(line.split("Status:")[1].split())
						#splitted_line = splitted_line.replace("\n", "")
						self.GPSstatus = splitted_line.replace(", ", "-")
						#self.GPSstatus = 'up'
						
						
					else:
						splitted_line = " ".join(line.split("Lock Status:")[1].split()).split(",")
						self.GPSphaselock = splitted_line[0]

	def get_storm_control(self, timeout_timer = 20):
		raw_port_info = read_from_csr("sh run l2vpn bridge group Mavenir bridge-domain CU-PLANE | i storm")
		if(raw_port_info == "Disconnected!"):
			#Future version will check if csr is connected to the site
			self.csr_connected = False
			self.storm_control = "Could not Retreive"
		else:
			splitted_port_info = split_text_by_lines(raw_port_info, header_lines = 1)
			#splitted_port_info = [" ".join(line.split()).split(" ") for line in splitted_port_info]
			try:
				self.storm_control = splitted_port_info[1].rstrip().strip()			
			except:
				self.storm_control = "No Storm Control Info available"
# Class for each site ##
class cell_site:
	def __init__(self, name, IP):
		self.name     		= name
		self.IP     		= IP
		self.csr_connected	= True
		self.csr			= csr()			

################################# Main Class #################################	
def Main():
	
#crt.Screen.Synchronous = True
	crt.Screen.Send(chr(13))
	# row = crt.Screen.CurrentRow
	# column = crt.Screen.CurrentColumn
	# var = crt.Screen.Get(row, 1, row, column)
	# x = var.split("@")
	# username = x[0]



	file_path = crt.Dialog.FileOpenDialog("Select csv file with your site list. Use first row as header row, 1st column site name, 2nd column ip address","Open", "", "CSV Files Comma Delimited (*.csv)|*.csv||")
	Save_path = os.path.dirname(file_path)
	Save_path = Save_path + '/Output'
	isExist = os.path.exists(Save_path)
	if not isExist:
		os.makedirs(Save_path)

	with open(file_path) as csvfile:
		site_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
		site_list = []
		line_count = 0
		for row in site_reader:
			if line_count == 0:
				header_length = len(row)
			else:
				site_list.append(cell_site(row[0],row[1]))
			line_count = line_count+1
	csvfile.close()
	#username = "jayeshkumar.patel" #crt.Dialog.Prompt("Enter your Username")
	pwd = crt.Dialog.Prompt("Enter your password", "Password Prompt","",True)

	username = crt.Dialog.Prompt("Enter your username")
	
	crt.Screen.Send(chr(13))

	total_sites = len(site_list)
	current_site_count = 0
############### Loop that checks all sites in the csv list
	
	file_is_writable = False
	####### Writes information to file_path, if the file is open, prompt user to close file.

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

		
		
	file_is_writable = True
	with open(dump_file_path, 'w') as csvfile:
		site_writer = csv.writer(csvfile, delimiter =',', quotechar='|', lineterminator='\n')
		site_writer.writerow(['Site ID','GPS Alarm','GPSstatus','GPSphaselock','Satellite Count','Alpha_TB_MAC', 'Alpha_TB_IP', 'Beta_TB_MAC','Beta_TB_IP','Gamma_TB_MAC','Gamma_TB_IP', 'Alpha_MB_MAC', 'Alpha_MB_IP', 'Beta_MB_MAC','Beta_MB_IP','Gamma_MB_MAC','Gamma_MB_IP','BV95MAC','BV95IP','SITEBOSSMAC','SITEBOSSIP','K8S','VMWAREPORT','VMWAREMAC','VMWAREIP', 'BV201','BV311','BV318','BV323','SITEBOSSPORT', 'BMCPORT', 'Port3', 'Port4', 'Port5', 'Port6', 'Port7', 'Port8', 'Port9', 'Port13', 'Port14', 'Port15','Port18', 'Port19', 'Port24', 'Port27', 'Port29', "Storm Control"])

		for site in site_list:
			max_tries 		= 3
			counter 		= 0

			crt.Session.SetStatusText("Script running for " + site.name)
			crt.Screen.Send("ssh " + username + "@" + site.IP + chr(13))
		
			site_reachable = crt.Screen.ReadString(["Are you sure you want to continue connecting ", "Password:"],10)
			index = crt.Screen.MatchIndex
			if(index == 1):
				site.reachable = False
				crt.Screen.Send("yes" + chr(13))
				crt.Screen.WaitForString("Password:")
				crt.Screen.Send(pwd + chr(13))
				crt.Screen.WaitForString("RP/0/RP0/CPU0:")
				#site.csr.get_temperatures()
				site.csr.get_mac_ip()
				site.csr.get_portsinfo()
				site.csr.get_GPSinfo()
				site.csr.get_storm_control()
				crt.Screen.Send("q" + chr(13))
				crt.Screen.WaitForString("closed.")


				crt.Screen.Send(chr(13))


			elif(index == 0):
				crt.Screen.Send(chr(3))
				crt.Screen.Send(chr(13))

			else:

				crt.Screen.Send(pwd + chr(13))
				crt.Screen.WaitForString("RP/0/RP0/CPU0:")
				site.csr.get_mac_ip()
				site.csr.get_portsinfo()
				site.csr.get_GPSinfo()
				site.csr.get_storm_control()
				crt.Screen.Send("q" + chr(13))
				crt.Screen.WaitForString("closed.")
					
			site_writer.writerow([site.name, site.csr.GPSMajorAlarm + '-' + site.csr.GPSMinorAlarm, site.csr.GPSstatus, site.csr.GPSphaselock, site.csr.Satellite, site.csr.Alpha_TB_MAC, site.csr.Alpha_TB_IP, site.csr.Beta_TB_MAC, site.csr.Beta_TB_IP,  site.csr.Gamma_TB_MAC, site.csr.Gamma_TB_IP, site.csr.Alpha_MB_MAC, site.csr.Alpha_MB_IP, site.csr.Beta_MB_MAC, site.csr.Beta_MB_IP,  site.csr.Gamma_MB_MAC, site.csr.Gamma_MB_IP, site.csr.BV95MAC, site.csr.BV95IP, site.csr.SITEBOSSMAC, site.csr.SITEBOSSIP,site.csr.K8S, site.csr.VMWAREPORT, site.csr.VMWAREMAC, site.csr.VMWAREIP,site.csr.PortBV201,site.csr.PortBV311,site.csr.PortBV318,site.csr.PortBV323, site.csr.SITEBOSSPORT, site.csr.BMCPORT, site.csr.Port3, site.csr.Port4, site.csr.Port5, site.csr.Port6, site.csr.Port7, site.csr.Port8, site.csr.Port9,site.csr.Port13,site.csr.Port14,site.csr.Port15, site.csr.Port18, site.csr.Port19,site.csr.Port24,site.csr.Port27,site.csr.Port29, site.csr.storm_control])




	crt.Dialog.MessageBox(dump_file_path, "File Saved Below Location" )

	
	
Main()