# $language = "Python"
# $interface = "1.0"

# For issue contact Jayeshkumar.patel@dish.com


import csv
import time
from math import floor
import os
from datetime import datetime

#Sends Command to CSR and handles different CSR Outputs
def read_from_CU(command, read_string = "capv@", timeout_timer = 20):
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

# Class for each site ##
class cell_site:
	def __init__(self, NAME, IP, CSRIP):
		self.NAME = NAME
		self.IP  = IP
		self.CSRIP = CSRIP
	
		self.vmwareIP =  "Not Found"
		self.vmwarestatus=  "Not Found"
		self.f1cip =  "Not Found"
		self.mplaneip =  "Not Found"
		self.dustatus =  "Not Found"
		self.containernumber = "Not Found"
		self.removemplaneip = "No"
		self.removef1cip = "No"
		self.CSRVMWAREMAC = "CSR Not Reachable"
		self.CSRVMWAREIP = "CSR Not Reachable"
		self.storm_control = "CSR Not Reachable"
		self.BV96pingstatus = "CSR Not Reachable"
		self.BMCPORT = "Not Reachable"
		self.BV96 = "CSR Not Reachable"
		self.BV95 = "CSR Not Reachable"
		self.Port18 = "CSR Not Reachable"
		self.Port3 = "CSR Not Reachable"
		self.Port13 = "CSR Not Reachable"
		self.Port14 = "CSR Not Reachable"
		self.Port15 = "CSR Not Reachable"
	


	def get_storm_control(self, timeout_timer = 20):
		
		self.storm_control = ""
		self.BV96pingstatus = "IP Missing"
		raw_port_info = read_from_csr("sh run l2vpn bridge group Mavenir bridge-domain CU-PLANE | i storm")
		splitted_port_info = split_text_by_lines(raw_port_info, header_lines = 1)
		try:
			self.storm_control = splitted_port_info[1].rstrip().strip()			
		except:
			self.storm_control = "No Info available"

		crt.Screen.Send("exit" + chr(13))
		crt.Screen.WaitForString("closed.")		

		if "10." in self.CSRVMWAREIP:
				crt.Screen.Send("ping " + self.CSRVMWAREIP + chr(13))						
				crt.Screen.WaitForStrings("icmp_seq=5", 6)
				crt.Screen.Send (chr(3))
				time.sleep(2)

				row = crt.Screen.CurrentRow
				column = crt.Screen.CurrentColumn
			
				var = crt.Screen.Get(row-2, 1, row-2, column+25)

				splitted_line_sctp = var.split(",")

				self.BV96txpacket= (splitted_line_sctp[0].split())[0]
				self.BV96rxpacket = (splitted_line_sctp[1].split())[0]
				self.BV96pinglost = (splitted_line_sctp[2].split())[0]
				if self.BV96txpacket == self.BV96rxpacket and int(self.BV96txpacket) > 0:
					self.BV96pingstatus = "PASS"

				else:
					self.BV96pingstatus = "FAIL"			

	def get_mac_ip(self):
		self.CSRVMWAREMAC = "MAC Missing"
		self.CSRVMWAREIP = "IP Missing"
		ReadData = read_from_csr("sh l2vpn mac mac all location 0/RP0/CPU0")
		splitted_device_info = split_text_by_lines(ReadData)
		for line in splitted_device_info:	

			if "Te0/0/0/14.96" in line:
				splitted_line = " ".join(line.split("Te0/0/0/14.96")[1].split()).split(" ")
				self.CSRVMWAREMAC = splitted_line[0][0:14]

			if "Te0/0/0/15.96" in line:
				splitted_line = " ".join(line.split("Te0/0/0/15.96")[1].split()).split(" ")
				self.CSRVMWAREMAC = splitted_line[0][0:14]

		
	
		if self.CSRVMWAREMAC != "MAC Missing":
			ReadData = read_from_csr("sh l2vpn mac mac-ipv4 all location 0/RP0/CPU0")
			splitted_device_info = split_text_by_lines(ReadData)
			for line in splitted_device_info:
				
				if self.CSRVMWAREMAC in line:
					splitted_line = " ".join(line.split(self.CSRVMWAREMAC)[1].split()).split(" ")
					self.CSRVMWAREIP = splitted_line[0]

			



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

				if "0/0/0/18" in line:
					splitted_line = " ".join(line.split("0/0/0/18")[1].split()).split(" ")
					self.Port18 = splitted_line[0]

				if "Gi0/0/0/2" in line:
					splitted_line = " ".join(line.split("Gi0/0/0/2")[1].split()).split(" ")
					self.BMCPORT = splitted_line[0]

				if "Gi0/0/0/3" in line:
					splitted_line = " ".join(line.split("Gi0/0/0/3")[1].split()).split(" ")
					self.Port3 = splitted_line[0]

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

		

		
				
	def get_vmwareinfo(self, NAME, IP, CSRIP):

		du_interface = read_from_CU("kubectl get pod -A | grep -i  " + NAME)
	
		du_Infomation = split_text_by_lines(du_interface)
		ducount = 0
		sitecount = 0
		vmwarecount = 0
		duname = ""
		for line in du_Infomation:

			if "du-" in line:
				ducount = ducount + 1

				if ducount == 1:
					duinfo = line.split()
					self.dustatus = duinfo[3]
					self.containernumber = duinfo[2]
					self.dupod = duinfo[0]

					
					#if self.dustatus == "ContainerCreating" and self.containernumber == "0/2":
					rowdunode = read_from_CU("kubectl describe pod -n " + self.dupod + " | grep Node")
					node_Infomation = split_text_by_lines(rowdunode)

					for line in node_Infomation:

						#crt.Dialog.MessageBox(str(line)) 

						if "siteid=" in line:
							sitecount = sitecount + 1
							

							if sitecount == 1:

								#crt.Dialog.MessageBox("siteid = " + str(sitecount)) 

								splitted_line_dunode = line.split("=")

								duname = splitted_line_dunode[1].replace("[K","")

								duname = duname[0:11]

						if "dupool" in line:
							sitecount = sitecount + 1
							

							if sitecount == 1:

								#crt.Dialog.MessageBox("dupool = " + str(sitecount))

								splitted_line_dunode = line.split("=")

								duname = splitted_line_dunode[1].replace("[K","")

								duname = duname[0:22]

						if duname != "":
							
							if sitecount == 1:
								sitecount = sitecount + 1
								#crt.Dialog.MessageBox(duname + "," + str(sitecount))

								raw_interface = read_from_CU("kubectl get nodes -owide | grep -i " + duname)

								Raw_Infomation = split_text_by_lines(raw_interface)

								for line in Raw_Infomation:
									

									if duname in line and "kubectl" not in line:
										Lineinfo = line.split()
										self.vmwarestatus = Lineinfo[1]
										self.vmwareIP = Lineinfo[5]

										if "10." in self.vmwareIP and self.vmwarestatus == "Ready":

											self.CSRVMWAREIP = "Not Checked"
											self.BV96pingstatus = "Not Checked"
											self.storm_control = "Not Checked"
											self.BV96 = "Not Checked"
											self.BV95 = "Not Checked"
											self.Port18 = "Not Checked"
											self.Port3 = "Not Checked"
											self.Port13 = "Not Checked"
											self.Port14 = "Not Checked"
											self.Port15 = "Not Checked"
											self.BMCPORT = "Not Checked"

									
											crt.Screen.Send("ssh capv@" + self.vmwareIP + chr(13))

											crt.Screen.ReadString(["Are you sure you want to continue connecting", "Password:"],10)
											index = crt.Screen.MatchIndex


											if(index == 0):
												crt.Screen.Send(chr(3))
												crt.Screen.Send(chr(13))

											if(index == 1):
												crt.Screen.Send("yes" + chr(13))
												crt.Screen.WaitForString("Password:")


											crt.Screen.Send("VMware1!VMware1!" + chr(13))

											crt.Screen.WaitForString("capv@use")

											crt.Screen.Send("su"  + chr(13))
											crt.Screen.WaitForString("Password:")
											crt.Screen.Send("VMware1!VMware1!" + chr(13))
											

											#crt.Dialog.MessageBox(site.GNB)
											crt.Screen.WaitForString("capv",2)

											crt.Screen.Send("cd /var/lib/cni/networks/du-f1c-conf" + chr(13))

											crt.Screen.WaitForString( "]#" ,2)

											crt.Screen.Send("ls"  + chr(13))
											crt.Screen.WaitForString("lock",1)

											crt.Screen.WaitForString("]#",1)

											row = crt.Screen.CurrentRow
											column = crt.Screen.CurrentColumn

											var = crt.Screen.Get(row-1, 1, row-1, column)

											ipinfo = var.split(" ")
											ip = ipinfo[0]

											if "10." in ip:
												self.f1cip= ip
												if self.dustatus == "ContainerCreating" :
													crt.Screen.Send("rm -rf "  + ip +chr(13))
													self.removef1cip = "Yes"
												else:
													self.removef1cip = "No"
													

											else:
												self.f1cip= "ip missing"
												self.removef1cipip = "No"

											crt.Screen.Send("cd /var/lib/cni/networks/du-mplane-conf" + chr(13))

											crt.Screen.WaitForString("]#",1)

											crt.Screen.Send("ls"  + chr(13))

											crt.Screen.WaitForString("lock",1)

											crt.Screen.WaitForString("]#",1)
											row = crt.Screen.CurrentRow
											column = crt.Screen.CurrentColumn

											var = crt.Screen.Get(row-1, 1, row-1, column)

											ipinfo = var.split(" ")
											ip = ipinfo[0]

											if "10." in ip:
												self.mplaneip= ip
												if self.dustatus == "ContainerCreating" :
													crt.Screen.Send("rm -rf "  + ip +chr(13))
													self.removemplaneip = "Yes"
												else:
													self.removemplaneip = "No"
												
											else:
												self.mplaneip= "ip missing"
												self.removemplaneip = "No"

											crt.Screen.Send("exit"  + chr(13))

											crt.Screen.WaitForString("capv@use")

											crt.Screen.Send("exit"  + chr(13))

											crt.Screen.WaitForString("closed.")

											if self.f1cip == "ip missing":
												crt.Screen.Send("kubectl rollout restart daemonset/vsphere-cloud-controller-manager -n kube-system"  + chr(13))



										elif self.vmwarestatus == "Ready" and self.vmwareIP == "<none>":
											crt.Screen.Send("kubectl rollout restart daemonset/vsphere-cloud-controller-manager -n kube-system"  + chr(13))
											self.CSRVMWAREIP = "Not Checked"
											self.BV96pingstatus = "Not Checked"
											self.storm_control = "Not Checked"
											self.BV96 = "Not Checked"
											self.BV95 = "Not Checked"
											self.Port18 = "Not Checked"
											self.Port3 = "Not Checked"
											self.Port13 = "Not Checked"
											self.Port14 = "Not Checked"
											self.Port15 = "Not Checked"
											self.BMCPORT = "Not Checked"
											self.f1cip =  "Not Checked"
											self.mplaneip =  "Not Checked"
											
										else:
											self.f1cip =  "Not Checked"
											self.mplaneip =  "Not Checked"
											



################################# Main Class #################################	
def Main():
	
#crt.Screen.Synchronous = True
	crt.Screen.Send(chr(13))

	file_path = crt.Dialog.FileOpenDialog("Select csv file ","Open", "", "CSV Files Comma Delimited (*.csv)|*.csv||")
	Save_path = os.path.dirname(file_path)
	Save_path = Save_path + '/Output'
	isExist = os.path.exists(Save_path)
	if not isExist:
		os.makedirs(Save_path)

	pwd = crt.Dialog.Prompt("Enter your NT password", "Password Prompt","",True)
	
	crt.Screen.Send(chr(13))
	with open(file_path) as csvfile:
		site_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
		site_list = []
		line_count = 0
		for row in site_reader:
			if line_count == 0:
				header_length = len(row)
			else:
				site_list.append(cell_site(row[0],row[1],row[2]))
			line_count = line_count+1
	csvfile.close()

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
	filename = str('\\VMWARE_Output_' + year + Month + Day + "_" + hr + Minute + Second + '.csv')
	dump_file_path =  Save_path + filename


	file_is_writable = True
	with open(dump_file_path, 'w') as csvfile:
		site_writer = csv.writer(csvfile, delimiter =',', quotechar='|', lineterminator='\n')
		site_writer.writerow(['SITE ID','IP-1','CSR IP','Du status','Vmwarestatus','VmwareIP','F1cip', 'Mplaneip', 'RemoveF1CIP', 'RemovemplaneIP', 'CSR VMWAREIP', 'VMWARE PINGABLE', 'StormControl', 'BV95', 'BV96', 'PORT2(BMC)','PORT3/PORT18', 'PORT13(PTP)', 'PORT14(K8S MGMT)', 'PORT15(MIDHAUL)'])
############### Loop that checks all sites in the csv list
	
		for site in site_list:
				crt.Screen.Send(chr(13))
				#crt.Dialog.MessageBox(site.GNB)
				crt.Screen.WaitForString("dishjmp")

				#crt.Dialog.MessageBox("script Name")	

				crt.Session.SetStatusText("Script running for " + site.NAME)
				
				crt.Screen.Send("ssh capv@" + site.IP + chr(13))

				
				crt.Screen.ReadString(["Are you sure you want to continue connecting", "Password:"],10)
				index = crt.Screen.MatchIndex


				if(index == 0):
					crt.Screen.Send(chr(3))
					crt.Screen.Send(chr(13))

				if(index == 1):
					crt.Screen.Send("yes" + chr(13))
					crt.Screen.WaitForString("Password:")



				crt.Screen.Send("VMware1!VMware1!" + chr(13))

				crt.Screen.WaitForString("capv@use")
				
				

				site.get_vmwareinfo(site.NAME, site.IP, site.CSRIP)
		
				crt.Screen.Send("exit" + chr(13))

				crt.Screen.WaitForString("closed.")

				if site.vmwarestatus == "NotReady" :
					crt.Screen.Send("ssh " + site.CSRIP + chr(13))
					crt.Screen.ReadString(["Are you sure you want to continue connecting ", "Password:"],10)
					index = crt.Screen.MatchIndex
					if(index == 1):
						crt.Screen.Send("yes" + chr(13))
						crt.Screen.WaitForString("Password:")
						crt.Screen.Send(pwd + chr(13))
						crt.Screen.WaitForString("RP/0/RP0/CPU0:")
						site.get_mac_ip()
						site.get_portsinfo()
						site.get_storm_control()
						crt.Screen.Send(chr(13))

					elif(index == 0):
						crt.Screen.Send(chr(3))
						crt.Screen.Send(chr(13))

					else:
						crt.Screen.Send(pwd + chr(13))
						crt.Screen.WaitForString("RP/0/RP0/CPU0:")
						site.get_mac_ip()
						site.get_portsinfo()
						site.get_storm_control()
						


					

				site_writer.writerow([site.NAME, site.IP,site.CSRIP, site.containernumber +" " + site.dustatus, site.vmwarestatus, site.vmwareIP, site.f1cip, site.mplaneip, site.removef1cip ,site.removemplaneip,site.CSRVMWAREIP, site.BV96pingstatus, site.storm_control, site.BV95, site.BV96, site.BMCPORT, site.Port3+"//"+site.Port18, site.Port13,site.Port14,site.Port15])
		

	crt.Session.SetStatusText("Ready")
	crt.Dialog.MessageBox(dump_file_path, "File Saved Below Location" )	

		
############################     Login to Fujistu server    #################################################
	
Main()