# $language = "Python"
# $interface = "1.0"

# For issue contact Jayeshkumar.patel@dish.com


import csv
import time
from math import floor
import os
from datetime import datetime

#Sends Command to CSR and handles different CSR Outputs
def read_from_BEDC(command, read_string = "ssm-user@", timeout_timer = 20):
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

def read_from_POD(command, read_string = "#", timeout_timer = 20):
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

def read_from_EPOD(command, read_string = "[admin@", timeout_timer = 20):
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
	def __init__(self, NAME, GNODEB, F1CIP, F1UIP, UPFdata, UPFVoice,BEDC):
		self.NAME        	= NAME
		self.GNB        	= GNODEB
		self.F1C        	= F1CIP
		self.F1U        	= F1UIP
		self.UPFD        	= UPFdata
		self.UPFV        	= UPFVoice
		self.BEDC        	= BEDC
		#self.KEYID        	= KEYID
		#self.KEY        	= KEY
		#self.TOKEN        	= TOKEN
		self.reachable		= False
		self.csr_connected	= True
		self.CUCPCOUNT =  0
		self.gnbmgr_status =  "Not Connected"
		self.gnbmgr_Rebootnumber =  "Not Connected"
		self.gnbmgr_UPtime =  "Not Connected"
		self.ngclientiwf_status =  "Not Connected"
		self.ngclientiwf_Rebootnumber =  "Not Connected"
		self.ngclientiwf_UPtime =  "Not Connected"
		self.N2pingstatus =  "Not Connected"
		self.N2Link =  "Not Connected"
		self.N2txpacket =  "Not Connected"
		self.N2rxpacket =  "Not Connected"
		self.N2pinglost =  "Not Connected"
		self.N2Linkstatus =  "Not Connected"
		self.CUUPCOUNT =  0
		self.srmsvc_status =  "Not Connected"
		self.srmsvc_Rebootnumber =  "Not Connected"
		self.srmsvc_UPtime =  "Not Connected"
		self.iwfsvc_status =  "Not Connected"
		self.iwfsvc_Rebootnumber =  "Not Connected"
		self.iwfsvc_UPtime =  "Not Connected"
		self.E1Upingstatus =  "Not Connected"
		self.E1ULink =  "Not Connected"
		self.E1Utxpacket =  "Not Connected"
		self.E1Urxpacket =  "Not Connected"
		self.E1Upinglost =  "Not Connected"
		self.E1ULinkstatus =  "Not Connected"
		self.intfmgrsvc_status =  "Not Connected"
		self.intfmgrsvc_Rebootnumber =  "Not Connected"
		self.intfmgrsvc_UPtime =  "Not Connected"
		self.gwsvc_status =  "Not Connected"
		self.gwsvc_Rebootnumber =  "Not Connected"
		self.gwsvc_UPtime =  "Not Connected"
		self.dprmsvc_status =  "Not Connected"
		self.dprmsvc_Rebootnumber =  "Not Connected"
		self.dprmsvc_UPtime =  "Not Connected"
		self.dalsvc_status =  "Not Connected"
		self.dalsvc_Rebootnumber =  "Not Connected"
		self.dalsvc_UPtime =  "Not Connected"
		self.bccsvc_status =  "Not Connected"
		self.bccsvc_Rebootnumber =  "Not Connected"
		self.bccsvc_UPtime =  "Not Connected"
		self.N3pingstatus =  "Not Connected"
		self.N3Link =  "Not Connected"
		self.N3txpacket =  "Not Connected"
		self.N3rxpacket =  "Not Connected"
		self.N3pinglost =  "Not Connected"
		self.F1Upingstatus =  "Not Connected"
		self.F1Uip =  "Not Connected"
		self.F1Utxpacket =  "Not Connected"
		self.F1Urxpacket =  "Not Connected"
		self.F1Upinglost =  "Not Connected"
		self.ueconmgr_status =  "Not Connected"
		self.ueconmgr_Rebootnumber =  "Not Connected"
		self.ueconmgr_UPtime =  "Not Connected"
		self.sctpxniwf_status =  "Not Connected"
		self.sctpxniwf_Rebootnumber =  "Not Connected"
		self.sctpxniwf_UPtime =  "Not Connected"
		self.sctpf1iwf_status =  "Not Connected"
		self.sctpf1iwf_Rebootnumber =  "Not Connected"
		self.sctpf1iwf_UPtime =  "Not Connected"
		self.F1Cpingstatus  =  "Not Connected"
		self.F1Cip =  "Not Connected"
		self.F1Ctxpacket =  "Not Connected"
		self.F1Crxpacket =  "Not Connected"
		self.F1Cpinglost =  "Not Connected"
		self.F1CLinkstatus =  "Not Connected"
		self.sctpe1iwf_status =  "Not Connected"
		self.sctpe1iwf_Rebootnumber =  "Not Connected"
		self.sctpe1iwf_UPtime =  "Not Connected"
		self.E1pingstatus =  "Not Connected"
		self.E1CLink =  "Not Connected"
		self.E1txpacket =  "Not Connected"
		self.E1rxpacket =  "Not Connected"
		self.E1pinglost =  "Not Connected"
		self.E1CLinkstatus =  "Not Connected"
		self.N3pingstatusvoice =  "Not Connected"
		self.N3Linkvoice =  "Not Connected"
		self.N3txpacketvoice =  "Not Connected"
		self.N3rxpacketvoice =  "Not Connected"
		self.N3pinglostvoice =  "Not Connected"



				
	def get_pod_list(self, NAME, GNB, F1C, F1U, UPFD, UPFV):
	
		raw_interface = read_from_BEDC("kubectl get pod -A | grep -i " + GNB)
		
		if(raw_interface == "Disconnected!"):
			self.CUCPCOUNT =  0
			self.gnbmgr_status =  "Not Connected"
			self.gnbmgr_Rebootnumber =  "Not Connected"
			self.gnbmgr_UPtime =  "Not Connected"
			self.ngclientiwf_status =  "Not Connected"
			self.ngclientiwf_Rebootnumber =  "Not Connected"
			self.ngclientiwf_UPtime =  "Not Connected"
			self.N2pingstatus =  "Not Connected"
			self.N2Link =  "Not Connected"
			self.N2txpacket =  "Not Connected"
			self.N2rxpacket =  "Not Connected"
			self.N2pinglost =  "Not Connected"
			self.N2Linkstatus =  "Not Connected"
			self.CUUPCOUNT =  0
			self.srmsvc_status =  "Not Connected"
			self.srmsvc_Rebootnumber =  "Not Connected"
			self.srmsvc_UPtime =  "Not Connected"
			self.iwfsvc_status =  "Not Connected"
			self.iwfsvc_Rebootnumber =  "Not Connected"
			self.iwfsvc_UPtime =  "Not Connected"
			self.E1Upingstatus =  "Not Connected"
			self.E1ULink =  "Not Connected"
			self.E1Utxpacket =  "Not Connected"
			self.E1Urxpacket =  "Not Connected"
			self.E1Upinglost =  "Not Connected"
			self.E1ULinkstatus =  "Not Connected"
			self.intfmgrsvc_status =  "Not Connected"
			self.intfmgrsvc_Rebootnumber =  "Not Connected"
			self.intfmgrsvc_UPtime =  "Not Connected"
			self.gwsvc_status =  "Not Connected"
			self.gwsvc_Rebootnumber =  "Not Connected"
			self.gwsvc_UPtime =  "Not Connected"
			self.dprmsvc_status =  "Not Connected"
			self.dprmsvc_Rebootnumber =  "Not Connected"
			self.dprmsvc_UPtime =  "Not Connected"
			self.dalsvc_status =  "Not Connected"
			self.dalsvc_Rebootnumber =  "Not Connected"
			self.dalsvc_UPtime =  "Not Connected"
			self.bccsvc_status =  "Not Connected"
			self.bccsvc_Rebootnumber =  "Not Connected"
			self.bccsvc_UPtime =  "Not Connected"
			self.N3pingstatus =  "Not Connected"
			self.N3Link =  "Not Connected"
			self.N3txpacket =  "Not Connected"
			self.N3rxpacket =  "Not Connected"
			self.N3pinglost =  "Not Connected"
			self.F1Upingstatus =  "Not Connected"
			self.F1Uip =  "Not Connected"
			self.F1Utxpacket =  "Not Connected"
			self.F1Urxpacket =  "Not Connected"
			self.F1Upinglost =  "Not Connected"
			self.ueconmgr_status =  "Not Connected"
			self.ueconmgr_Rebootnumber =  "Not Connected"
			self.ueconmgr_UPtime =  "Not Connected"
			self.sctpxniwf_status =  "Not Connected"
			self.sctpxniwf_Rebootnumber =  "Not Connected"
			self.sctpxniwf_UPtime =  "Not Connected"
			self.sctpf1iwf_status =  "Not Connected"
			self.sctpf1iwf_Rebootnumber =  "Not Connected"
			self.sctpf1iwf_UPtime =  "Not Connected"
			self.F1Cpingstatus  =  "Not Connected"
			self.F1Cip =  "Not Connected"
			self.F1Ctxpacket =  "Not Connected"
			self.F1Crxpacket =  "Not Connected"
			self.F1Cpinglost =  "Not Connected"
			self.F1CLinkstatus =  "Not Connected"
			self.sctpe1iwf_status =  "Not Connected"
			self.sctpe1iwf_Rebootnumber =  "Not Connected"
			self.sctpe1iwf_UPtime =  "Not Connected"
			self.E1pingstatus =  "Not Connected"
			self.E1CLink =  "Not Connected"
			self.E1txpacket =  "Not Connected"
			self.E1rxpacket =  "Not Connected"
			self.E1pinglost =  "Not Connected"
			self.E1CLinkstatus =  "Not Connected"
			self.N3pingstatusvoice =  "Not Connected"
			self.N3Linkvoice =  "Not Connected"
			self.N3txpacketvoice =  "Not Connected"
			self.N3rxpacketvoice =  "Not Connected"
			self.N3pinglostvoice =  "Not Connected"


		else:
			#self.controller_set = True
	


			Raw_Infomation = split_text_by_lines(raw_interface)
			self.CUCPCOUNT = 0
			self.CUUPCOUNT = 0
			for line in Raw_Infomation:

					Lineinfo = line.split()
					Lineinfo = ((Lineinfo[1]).split("-"))[0]

	

					gnbmgrpodinfo = "gnbmgr"
					ngclientiwfpodinfo = "ngclientiwf"
					sctpe1iwfpodinfo = "sctpe1iwf"
					sctpf1iwfpodinfo = "sctpf1iwf"
					sctpxniwfpodinfo = "sctpxniwf"
					ueconmgrpodinfo = "ueconmgr"
					bccsvcpodinfo = "bccsvc"
					dalsvcpodinfo = "dalsvc"
					dprmsvcpodinfo = "dprmsvc"
					gwsvcpodinfo = "gwsvc"
					intfmgrsvcpodinfo = "intfmgrsvc"
					iwfsvcpodinfo = "iwfsvc"
					srmsvcpodinfo = "srmsvc"


					if Lineinfo == gnbmgrpodinfo:
						self.CUCPCOUNT = self.CUCPCOUNT + 1
						splitted_line = line.split()
						self.PODCommand = splitted_line[0] + "   " + splitted_line[1]
						self.gnbmgr_status = splitted_line[2] + " " + splitted_line[3]
						self.gnbmgr_containernumber = splitted_line[2]
						self.gnbmgr_Rebootnumber = splitted_line[4]
						self.gnbmgr_UPtime = splitted_line[5].replace("[K","")

					if Lineinfo == ngclientiwfpodinfo:

						crt.Session.SetStatusText("Script running for " + NAME + " - " + GNB + " - N2 LINK")
						self.CUCPCOUNT = self.CUCPCOUNT + 1
						splitted_line = line.split()
						self.PODCommand = splitted_line[0] + "   " + splitted_line[1]
						self.ngclientiwf_status = splitted_line[2] + " " + splitted_line[3]
						self.ngclientiwf_containernumber = splitted_line[2]
						self.ngclientiwf_Rebootnumber = splitted_line[4]
						self.ngclientiwf_UPtime = splitted_line[5].replace("[K","")

						crt.Screen.Send("kubectl exec -it -n "+ splitted_line[0] + "   " + splitted_line[1] + "  -- bash" + chr(13))
						
						
						nIndex  = crt.Screen.WaitForStrings(["]#","Error from server (NotFound)"],5)
							
						if nIndex == 2:
							crt.Screen.Send("export AWS_ACCESS_KEY_ID=" + chr(34) + self.KEYID + chr(34) + chr(13))
							crt.Screen.Send("export AWS_SECRET_ACCESS_KEY=" + chr(34) + self.KEY + chr(34) + chr(13))
							crt.Screen.Send("export AWS_SESSION_TOKEN=" + chr(34) + self.TOKEN + chr(34) + chr(13))
							crt.Screen.Send(self.BEDC + chr(13))
							crt.Screen.WaitForString("Updated context")
							crt.Screen.WaitForString("ssm-user@")
							crt.Screen.Send("kubectl exec -it -n "+ splitted_line[0] + "   " + splitted_line[1] + "  -- bash" + chr(13))
						
						row = crt.Screen.CurrentRow
						column = crt.Screen.CurrentColumn
						var = crt.Screen.Get(row, 1, row, column)

						
						if "root" in var and "#" in var:

							raw_sctp = read_from_POD("netstat -apn | grep sctp")
							raw_sctp_split = split_text_by_lines(raw_sctp)

							count = 0
							for line in raw_sctp_split:

								if "netstat" not in line:
									count = count + 1
									splitted_line_sctp = line.split()
									if count == 1:
										self.N2Linkstatus = splitted_line_sctp[5]
										self.N2Link = (splitted_line_sctp[4].split(":"))[0]
									else:
										self.N2Linkstatus = self.N2Linkstatus + "//" + splitted_line_sctp[5]
										self.N2Link = self.N2Link + "//" + (splitted_line_sctp[4].split(":"))[0]
									crt.Screen.Send("ping " + (splitted_line_sctp[4].split(":"))[0] + chr(13))
											
									crt.Screen.WaitForStrings("icmp_seq=5", 6)

									crt.Screen.Send (chr(3))
									time.sleep(2)
									row = crt.Screen.CurrentRow
									column = crt.Screen.CurrentColumn
								
									var = crt.Screen.Get(row-2, 1, row-2, column+25)
									#crt.Dialog.MessageBox("N2 Link interface result from CUCP to AMF\n\n\n" + str(var))
									splitted_line_sctp = var.split(",")
									if count == 1:
										self.N2txpacket= (splitted_line_sctp[0].split())[0]
										self.N2rxpacket = (splitted_line_sctp[1].split())[0]
										self.N2pinglost = (splitted_line_sctp[2].split())[0]
										if self.N2txpacket == self.N2rxpacket and int(self.N2txpacket) > 0:
											self.N2pingstatus = "PASS"

										else:
											self.N2pingstatus = "FAIL"
									else:
										N2txpacket= (splitted_line_sctp[0].split())[0]
										N2rxpacket = (splitted_line_sctp[1].split())[0]
									
										self.N2txpacket= self.N2txpacket + "//" + (splitted_line_sctp[0].split())[0]
										self.N2rxpacket = self.N2rxpacket + "//" + (splitted_line_sctp[1].split())[0]
										self.N2pinglost = self.N2pinglost + "//" + (splitted_line_sctp[2].split())[0]
										if N2txpacket == N2rxpacket and int(N2txpacket) > 0:
											self.N2pingstatus = self.N2pingstatus + "//" + "PASS"

										else:
											self.N2pingstatus = self.N2pingstatus + "//" + "FAIL"
									

							var = crt.Screen.Get(row, 1, row, column)
							splitted_line_sctp = var.split("@")
							lineinfo= splitted_line_sctp[0]
							if lineinfo == "[root":
								lineinfo = "good"
							else: 
								crt.Screen.WaitForString("[root@")
							crt.Screen.Send("exit" + chr(13))
							crt.Screen.WaitForString("ssm-user@")
							

					if Lineinfo == sctpe1iwfpodinfo:
						crt.Session.SetStatusText("Script running for " + NAME + " - " + GNB + " - E1C LINK")
						self.CUCPCOUNT = self.CUCPCOUNT + 1
						splitted_line = line.split()
						self.PODCommand = splitted_line[0] + "   " + splitted_line[1]
						self.sctpe1iwf_status = splitted_line[2] + " " + splitted_line[3]
						self.sctpe1iwf_containernumber = splitted_line[2]
						self.sctpe1iwf_Rebootnumber = splitted_line[4]
						self.sctpe1iwf_UPtime = splitted_line[5].replace("[K","")

						crt.Screen.Send("kubectl exec -it -n "+ self.PODCommand + "  -- bash" + chr(13))

						nIndex  = crt.Screen.WaitForStrings(["]#","Error from server (NotFound)"],5)
							
						if nIndex == 2:
							crt.Screen.Send("export AWS_ACCESS_KEY_ID=" + chr(34) + self.KEYID + chr(34) + chr(13))
							crt.Screen.Send("export AWS_SECRET_ACCESS_KEY=" + chr(34) + self.KEY + chr(34) + chr(13))
							crt.Screen.Send("export AWS_SESSION_TOKEN=" + chr(34) + self.TOKEN + chr(34) + chr(13))
							crt.Screen.Send(self.BEDC + chr(13))
							crt.Screen.WaitForString("Updated context")
							crt.Screen.WaitForString("ssm-user@")
							crt.Screen.Send("kubectl exec -it -n "+ splitted_line[0] + "   " + splitted_line[1] + "  -- bash" + chr(13))
						
						row = crt.Screen.CurrentRow
						column = crt.Screen.CurrentColumn
						var = crt.Screen.Get(row, 1, row, column)

						if "root" in var and "#" in var:
							raw_sctp = read_from_POD("netstat -apn | grep sctp")
							raw_sctp_split = split_text_by_lines(raw_sctp)
							count = 0
							for line in raw_sctp_split:

								if "netstat" not in line and "LISTEN" not in line:
									count = count + 1
						
									splitted_line_sctp = line.split()
									if count == 1:
										self.E1CLinkstatus = splitted_line_sctp[5]
										self.E1CLink = (splitted_line_sctp[4].split(":"))[0]
									else:
										self.E1CLinkstatus = self.E1CLinkstatus + "//" + splitted_line_sctp[5]
										self.E1CLink = self.E1CLink + "//" + (splitted_line_sctp[4].split(":"))[0]
									crt.Screen.Send("ping " + (splitted_line_sctp[4].split(":"))[0] + chr(13))
									
									crt.Screen.WaitForString("icmp_seq=5", 6)
									crt.Screen.Send (chr(3))
									time.sleep(2)
									row = crt.Screen.CurrentRow
									column = crt.Screen.CurrentColumn
								
									var = crt.Screen.Get(row-2, 1, row-2, column+25)


									#crt.Dialog.MessageBox("E1C Link interface result from CUCP to CUUP\n\n\n" + str(var))
									splitted_line_sctp = var.split(",")

									if count == 1:
										self.E1txpacket= (splitted_line_sctp[0].split())[0]
										self.E1rxpacket = (splitted_line_sctp[1].split())[0]
										self.E1pinglost = (splitted_line_sctp[2].split())[0]

										if self.E1txpacket == self.E1rxpacket and int(self.E1txpacket) > 0:
											self.E1pingstatus = "PASS"

										else:
											self.E1pingstatus = "FAIL"

									else:
										E1txpacket= (splitted_line_sctp[0].split())[0]
										E1rxpacket = (splitted_line_sctp[1].split())[0]
										self.E1txpacket= self.E1txpacket + "//" + (splitted_line_sctp[0].split())[0]
										self.E1rxpacket = self.E1rxpacket + "//" + (splitted_line_sctp[1].split())[0]
										self.E1pinglost = self.E1pinglost + "//" + (splitted_line_sctp[2].split())[0]

										if E1txpacket == E1rxpacket and int(E1txpacket) > 0:
											self.E1pingstatus = self.E1pingstatus + "//" + "PASS"

										else:
											self.E1pingstatus = self.E1pingstatus + "//" + "FAIL"

	
							var = crt.Screen.Get(row, 1, row, column)
							splitted_line_sctp = var.split("@")
							lineinfo= splitted_line_sctp[0]
							if lineinfo == "[root":
								lineinfo = "good"
							else: 
								crt.Screen.WaitForString("[root@")
							crt.Screen.Send("exit" + chr(13))
							crt.Screen.WaitForString("ssm-user@")

					if Lineinfo == sctpf1iwfpodinfo:
						crt.Session.SetStatusText("Script running for " + NAME + " - " + GNB + " - F1C LINK")
						self.CUCPCOUNT = self.CUCPCOUNT + 1
						splitted_line = line.split()
						self.PODCommand = splitted_line[0] + "   " + splitted_line[1]
						self.sctpf1iwf_status = splitted_line[2] + " " + splitted_line[3]
						self.sctpf1iwf_containernumber = splitted_line[2]
						self.sctpf1iwf_Rebootnumber = splitted_line[4]
						self.sctpf1iwf_UPtime = splitted_line[5].replace("[K","")

						crt.Screen.Send("kubectl exec -it -n "+ self.PODCommand + "  -- bash" + chr(13))

						nIndex  = crt.Screen.WaitForStrings(["]#","Error from server (NotFound)"],5)
							
						if nIndex == 2:
							crt.Screen.Send("export AWS_ACCESS_KEY_ID=" + chr(34) + self.KEYID + chr(34) + chr(13))
							crt.Screen.Send("export AWS_SECRET_ACCESS_KEY=" + chr(34) + self.KEY + chr(34) + chr(13))
							crt.Screen.Send("export AWS_SESSION_TOKEN=" + chr(34) + self.TOKEN + chr(34) + chr(13))
							crt.Screen.Send(self.BEDC + chr(13))
							crt.Screen.WaitForString("Updated context")
							crt.Screen.WaitForString("ssm-user@")
							crt.Screen.Send("kubectl exec -it -n "+ splitted_line[0] + "   " + splitted_line[1] + "  -- bash" + chr(13))
						
						row = crt.Screen.CurrentRow
						column = crt.Screen.CurrentColumn
						var = crt.Screen.Get(row, 1, row, column)

						if "root" in var and "#" in var:
							raw_sctp = read_from_POD("netstat -apn | grep sctp")
							raw_sctp_split = split_text_by_lines(raw_sctp)

							self.F1CLinkstatus = "ESTABLISHED"

							for line in raw_sctp_split:

								if "netstat" not in line and "LISTEN" not in line:
									
									splitted_line_sctp = line.split()
									if self.F1CLinkstatus == "ESTABLISHED":
										F1CLinkstatus = splitted_line_sctp[5]
										self.F1CLinkstatus = F1CLinkstatus[0:11]

									else: 
										self.F1CLinkstatus = "NOT ESTABLISHED"
										
							
							if "10" not in F1C:
								self.F1Cip = "Dark Fiber"
								self.F1Ctxpacket = "Dark Fiber"
								self.F1Crxpacket = "Dark Fiber"
								self.F1Cpinglost = "Dark Fiber"
								self.F1Cpingstatus = "Dark Fiber"
							
							else:

								splitted_line_sctp = F1C.split(".")
								
								self.F1Cip = splitted_line_sctp[0] + "." + splitted_line_sctp[1] + "." + splitted_line_sctp[2] + "." +str(int(splitted_line_sctp[3]) + 2)
								
								crt.Screen.Send("ping " + self.F1Cip + chr(13))
										
								crt.Screen.WaitForString("icmp_seq=5", 6)
								crt.Screen.Send (chr(3))
						
								time.sleep(2)
								row = crt.Screen.CurrentRow
								column = crt.Screen.CurrentColumn
									
								var = crt.Screen.Get(row-2, 1, row-2, column+25)
								#crt.Dialog.MessageBox("F1C Link interface result from CUCP to DU\n\n\n" + str(var))
								splitted_line_sctp = var.split(",")
								self.F1Ctxpacket= (splitted_line_sctp[0].split())[0]
								self.F1Crxpacket = (splitted_line_sctp[1].split())[0]
								self.F1Cpinglost = (splitted_line_sctp[2].split())[0]

								if self.F1Ctxpacket == self.F1Crxpacket and int(self.F1Ctxpacket) > 0:
									self.F1Cpingstatus = "PASS"

								else:
									self.F1Cpingstatus = "FAIL"

							crt.Screen.Send("exit" + chr(13))
							crt.Screen.WaitForString("ssm-user@")




					if Lineinfo == sctpxniwfpodinfo:
						self.CUCPCOUNT = self.CUCPCOUNT + 1
						splitted_line = line.split()
						self.PODCommand = splitted_line[0] + "   " + splitted_line[1]
						self.sctpxniwf_status = splitted_line[2] + " " + splitted_line[3]
						self.sctpxniwf_containernumber = splitted_line[2]
						self.sctpxniwf_Rebootnumber = splitted_line[4]
						self.sctpxniwf_UPtime = splitted_line[5].replace("[K","")


					if Lineinfo == ueconmgrpodinfo:
						self.CUCPCOUNT = self.CUCPCOUNT + 1
						splitted_line = line.split()
						self.ueconmgr_status = splitted_line[2] + " " + splitted_line[3]
						self.ueconmgr_containernumber = splitted_line[2]
						self.ueconmgr_Rebootnumber = splitted_line[4]
						self.ueconmgr_UPtime = splitted_line[5].replace("[K","")

					if Lineinfo == bccsvcpodinfo:
						crt.Session.SetStatusText("Script running for " + NAME + " - " + GNB + " - F1U LINK")
						self.CUUPCOUNT = self.CUUPCOUNT + 1
						splitted_line = line.split()
						self.PODCommand = splitted_line[0] + "   " + splitted_line[1]
						self.bccsvc_status = splitted_line[2] + " " + splitted_line[3]
						self.bccsvc_containernumber = splitted_line[2]
						self.bccsvc_Rebootnumber = splitted_line[4]
						self.bccsvc_UPtime = splitted_line[5].replace("[K","")

						crt.Screen.Send("kubectl exec -it -n "+ self.PODCommand + "  -- bash" + chr(13))

						nIndex  = crt.Screen.WaitForStrings(["]#","Error from server (NotFound)"],5)
							
						if nIndex == 2:
							crt.Screen.Send("export AWS_ACCESS_KEY_ID=" + chr(34) + self.KEYID + chr(34) + chr(13))
							crt.Screen.Send("export AWS_SECRET_ACCESS_KEY=" + chr(34) + self.KEY + chr(34) + chr(13))
							crt.Screen.Send("export AWS_SESSION_TOKEN=" + chr(34) + self.TOKEN + chr(34) + chr(13))
							crt.Screen.Send(self.BEDC + chr(13))
							crt.Screen.WaitForString("Updated context")
							crt.Screen.WaitForString("ssm-user@")
							crt.Screen.Send("kubectl exec -it -n "+ splitted_line[0] + "   " + splitted_line[1] + "  -- bash" + chr(13))
						
						row = crt.Screen.CurrentRow
						column = crt.Screen.CurrentColumn
						var = crt.Screen.Get(row, 1, row, column)

						if "root" in var and "#" in var:
							if "10" not in F1U:
								self.F1Uip = "Dark Fiber"
								self.F1Utxpacket = "Dark Fiber"
								self.F1Urxpacket = "Dark Fiber"
								self.F1Upinglost = "Dark Fiber"
								self.F1Upingstatus = "Dark Fiber"								

							else:
								
								splitted_line_sctp = F1U.split(".")

								self.F1Uip = splitted_line_sctp[0] + "." + splitted_line_sctp[1] + "." + splitted_line_sctp[2] + "." +str(int(splitted_line_sctp[3]) + 2)
								
								crt.Screen.Send("vppctl ping " + self.F1Uip + chr(13))
																
								time.sleep(7)
								row = crt.Screen.CurrentRow
								column = crt.Screen.CurrentColumn
									
								var = crt.Screen.Get(row-1, 1, row-1, column+25)
								#crt.Dialog.MessageBox("F1U Link interface result from CUUP to DU\n\n\n" + str(var))
								splitted_line_sctp = var.split(",")
								self.F1Utxpacket= (splitted_line_sctp[0].split())[1]
								self.F1Urxpacket = (splitted_line_sctp[1].split())[0]
								self.F1Upinglost = (splitted_line_sctp[2].split())[0]

								if self.F1Utxpacket == self.F1Urxpacket and int(self.F1Urxpacket) > 0:
									self.F1Upingstatus = "PASS"

								else:
									self.F1Upingstatus = "FAIL"

							crt.Session.SetStatusText("Script running for " + NAME + " - " + GNB + " - N3 Data LINK")

							crt.Screen.Send("vppctl ping " + UPFD + chr(13))

							self.N3Link = UPFD		
							time.sleep(7)
							row = crt.Screen.CurrentRow
							column = crt.Screen.CurrentColumn
							var = crt.Screen.Get(row-1, 1, row-1, column+25)
							#crt.Dialog.MessageBox("N3 Link interface result from CUUP to UPF\n\n\n" + str(var))
							splitted_line_sctp = var.split(",")
							self.N3txpacket= (splitted_line_sctp[0].split())[1]
							self.N3rxpacket = (splitted_line_sctp[1].split())[0]
							self.N3pinglost = (splitted_line_sctp[2].split())[0]
							if self.N3txpacket == self.N3rxpacket and int(self.N3rxpacket) > 0:
								self.N3pingstatus = "PASS"

							else:
								self.N3pingstatus = "FAIL"


							crt.Session.SetStatusText("Script running for " + NAME + " - " + GNB + " - N3 Voice LINK")

							crt.Screen.Send("vppctl ping " + UPFV + chr(13))

							self.N3Linkvoice = UPFV		
							time.sleep(7)
							row = crt.Screen.CurrentRow
							column = crt.Screen.CurrentColumn
							var = crt.Screen.Get(row-1, 1, row-1, column+25)
							#crt.Dialog.MessageBox("N3 Link interface result from CUUP to UPF\n\n\n" + str(var))
							splitted_line_sctp = var.split(",")
							self.N3txpacketvoice= (splitted_line_sctp[0].split())[1]
							self.N3rxpacketvoice = (splitted_line_sctp[1].split())[0]
							self.N3pinglostvoice = (splitted_line_sctp[2].split())[0]
							if self.N3txpacketvoice == self.N3rxpacketvoice and int(self.N3rxpacketvoice) > 0:
								self.N3pingstatusvoice = "PASS"

							else:
								self.N3pingstatusvoice = "FAIL"

							crt.Screen.Send("exit" + chr(13))
							crt.Screen.WaitForString("ssm-user@")


					if Lineinfo == dalsvcpodinfo:
						self.CUUPCOUNT = self.CUUPCOUNT + 1
						splitted_line = line.split()
						self.dalsvc_status = splitted_line[2] + " " + splitted_line[3]
						self.dalsvc_containernumber = splitted_line[2]
						self.dalsvc_Rebootnumber = splitted_line[4]
						self.dalsvc_UPtime = splitted_line[5].replace("[K","")
					


					if Lineinfo == dprmsvcpodinfo:
						self.CUUPCOUNT = self.CUUPCOUNT + 1
						splitted_line = line.split()
						self.dprmsvc_status = splitted_line[2] + " " + splitted_line[3]
						self.dprmsvc_containernumber = splitted_line[2]
						self.dprmsvc_Rebootnumber = splitted_line[4]
						self.dprmsvc_UPtime = splitted_line[5].replace("[K","")


					if Lineinfo == gwsvcpodinfo:
						self.CUUPCOUNT = self.CUUPCOUNT + 1
						splitted_line = line.split()
						self.gwsvc_status = splitted_line[2] + " " + splitted_line[3]
						self.gwsvc_containernumber = splitted_line[2]
						self.gwsvc_Rebootnumber = splitted_line[4]
						self.gwsvc_UPtime = splitted_line[5].replace("[K","")
						

					if Lineinfo == intfmgrsvcpodinfo:
						self.CUUPCOUNT = self.CUUPCOUNT + 1
						splitted_line = line.split()
						self.intfmgrsvc_status = splitted_line[2] + " " + splitted_line[3]
						self.intfmgrsvc_containernumber = splitted_line[2]
						self.intfmgrsvc_Rebootnumber = splitted_line[4]
						self.intfmgrsvc_UPtime = splitted_line[5].replace("[K","")
					


					if Lineinfo == iwfsvcpodinfo:
						crt.Session.SetStatusText("Script running for " + NAME + " - " + GNB + " - E1U LINK")
						self.CUUPCOUNT = self.CUUPCOUNT + 1
						splitted_line = line.split()
						self.PODCommand = splitted_line[0] + "   " + splitted_line[1]
						self.iwfsvc_status = splitted_line[2] + " " + splitted_line[3]
						self.iwfsvc_containernumber = splitted_line[2]
						self.iwfsvc_Rebootnumber = splitted_line[4]
						self.iwfsvc_UPtime = splitted_line[5].replace("[K","")

						crt.Screen.Send("kubectl exec -it -n "+ self.PODCommand + "  -- bash" + chr(13))

						nIndex  = crt.Screen.WaitForStrings(["go]$","Error from server (NotFound)"],5)
							
						if nIndex == 2:
							crt.Screen.Send("export AWS_ACCESS_KEY_ID=" + chr(34) + self.KEYID + chr(34) + chr(13))
							crt.Screen.Send("export AWS_SECRET_ACCESS_KEY=" + chr(34) + self.KEY + chr(34) + chr(13))
							crt.Screen.Send("export AWS_SESSION_TOKEN=" + chr(34) + self.TOKEN + chr(34) + chr(13))
							crt.Screen.Send(self.BEDC + chr(13))
							crt.Screen.WaitForString("Updated context")
							crt.Screen.WaitForString("ssm-user@")
							crt.Screen.Send("kubectl exec -it -n "+ splitted_line[0] + "   " + splitted_line[1] + "  -- bash" + chr(13))
						
						row = crt.Screen.CurrentRow
						column = crt.Screen.CurrentColumn
						var = crt.Screen.Get(row, 1, row, column)

						if "admin" in var and "go]$" in var:

							raw_sctp = read_from_EPOD("netstat -apn | grep sctp")
							raw_sctp_split = split_text_by_lines(raw_sctp)
							count = 0

							for line in raw_sctp_split:

								if "netstat" not in line and "sctp" in line:

									count = count + 1
									splitted_line_sctp = line.split()
									if count == 1:
										self.E1ULinkstatus = splitted_line_sctp[5]
										self.E1ULink = (splitted_line_sctp[4].split(":"))[0]
									else:
										self.E1ULinkstatus = self.E1ULinkstatus + "//" +  splitted_line_sctp[5]
										self.E1ULink = self.E1ULink + "//" +  (splitted_line_sctp[4].split(":"))[0]

									crt.Screen.Send("sudo ping " + (splitted_line_sctp[4].split(":"))[0] + chr(13))
									
									crt.Screen.WaitForString("icmp_seq=5", 6)
									crt.Screen.Send (chr(3))
									time.sleep(2)
									row = crt.Screen.CurrentRow
									column = crt.Screen.CurrentColumn
									var = crt.Screen.Get(row-2, 1, row-2, column+25)

									
									#crt.Dialog.MessageBox("E1U Link interface result from CUUP to CUCP\n\n\n" + str(var))
									splitted_line_sctp = var.split(",")

									if count == 1:
										self.E1Utxpacket= (splitted_line_sctp[0].split())[0]
										self.E1Urxpacket = (splitted_line_sctp[1].split())[0]
										self.E1Upinglost = (splitted_line_sctp[2].split())[0]

										if self.E1Utxpacket == self.E1Urxpacket and int(self.E1Utxpacket) > 0:
											self.E1Upingstatus = "PASS"

										else:
											self.E1Upingstatus = "FAIL"

									else:
										E1Utxpacket= (splitted_line_sctp[0].split())[0]
										E1Urxpacket = (splitted_line_sctp[1].split())[0]
										self.E1Utxpacket= self.E1Utxpacket + "//" +  (splitted_line_sctp[0].split())[0]
										self.E1Urxpacket = self.E1Urxpacket + "//" +  (splitted_line_sctp[1].split())[0]
										self.E1Upinglost = self.E1Upinglost + "//" +  (splitted_line_sctp[2].split())[0]

										if E1Utxpacket == E1Urxpacket and int(E1Utxpacket) > 0:
											self.E1Upingstatus = self.E1Upingstatus + "//" +  "PASS"

										else:
											self.E1Upingstatus = self.E1Upingstatus + "//" +  "FAIL"
							var = crt.Screen.Get(row, 1, row, column)
							splitted_line_sctp = var.split("@")
							lineinfo= splitted_line_sctp[0]
							if lineinfo == "[admin":
								lineinfo = "good"
							else: 
								crt.Screen.WaitForString("[admin@")
							crt.Screen.Send("exit" + chr(13))	
							crt.Screen.WaitForString("ssm-user@")


					if Lineinfo == srmsvcpodinfo:
						self.CUUPCOUNT = self.CUUPCOUNT + 1
						splitted_line = line.split()
						self.srmsvc_status = splitted_line[2] + " " + splitted_line[3]
						self.srmsvc_containernumber = splitted_line[2]
						self.srmsvc_Rebootnumber = splitted_line[4]
						self.srmsvc_UPtime = splitted_line[5].replace("[K","")



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
	#KEYID = crt.Dialog.Prompt("AWS Access Key Id",)
	#KEY = crt.Dialog.Prompt("AWS Secret access key",)
	#TOKEN = crt.Dialog.Prompt("AWS session token",)
	#crt.Screen.Send("export AWS_ACCESS_KEY_ID=" + chr(34) + KEYID + chr(34) + chr(13))
	#crt.Screen.Send("export AWS_SECRET_ACCESS_KEY=" + chr(34) + KEY + chr(34) + chr(13))
	#crt.Screen.Send("export AWS_SESSION_TOKEN=" + chr(34) + TOKEN + chr(34) + chr(13))
	filename1 = os.path.basename(file_path)
	objTab = crt.GetScriptTab()
	objTab.Caption = filename1
	with open(file_path) as csvfile:
		site_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
		site_list = []
		line_count = 0
		for row in site_reader:
			if line_count == 0:
				header_length = len(row)
			else:
				site_list.append(cell_site(row[0],row[1],row[2],row[3],row[4],row[5],row[6]))
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
	filename = str('\\Output_' + year + Month + Day + "_" + hr + Minute + Second + '.csv')
	dump_file_path =  Save_path + filename


	file_is_writable = True
	with open(dump_file_path, 'w') as csvfile:
		site_writer = csv.writer(csvfile, delimiter =',', quotechar='|', lineterminator='\n')
		site_writer.writerow(['SITE ID','GNODEB ID','TOTAL POD COUNT','POD TYPE','POD NAME', 'POD STATUS','REBOOT COUNT', 'UPTIME','INTERFACE CONNECTION', 'INTERFACE PING STATUS', 'PINGED IP', 'Packet Transmitted','Packet Received','PACKET LOSS%', 'INTERFACE LINK STATUS' ])
					

############### Loop that checks all sites in the csv list
	
		for site in site_list:
				crt.Screen.Send(chr(13))
				#crt.Dialog.MessageBox(site.GNB)
				crt.Screen.WaitForString("ssm-user@")
				
				crt.Screen.Send(site.BEDC + chr(13))
				crt.Screen.WaitForString("Updated context")
				crt.Screen.WaitForString("ssm-user@")
				
				crt.Session.SetStatusText("Script running for " + site.NAME + " - " + site.GNB)

				site.get_pod_list(site.NAME, site.GNB, site.F1C, site.F1U, site.UPFD, site.UPFV)
					

				site_writer.writerow([site.NAME, site.GNB, site.CUCPCOUNT, "CUCP",'gnbmgr', site.gnbmgr_status, site.gnbmgr_Rebootnumber, site.gnbmgr_UPtime,'','','','','','',''])
				site_writer.writerow([site.NAME, site.GNB, site.CUCPCOUNT, "CUCP",'ngclientiwf', site.ngclientiwf_status, site.ngclientiwf_Rebootnumber, site.ngclientiwf_UPtime,'CUCP to AMF - N2 Link',site.N2pingstatus, site.N2Link, site.N2txpacket, site.N2rxpacket, site.N2pinglost, site.N2Linkstatus])
				site_writer.writerow([site.NAME, site.GNB, site.CUCPCOUNT, "CUCP",'sctpe1iwf', site.sctpe1iwf_status, site.sctpe1iwf_Rebootnumber, site.sctpe1iwf_UPtime,'CUCP to CUUP - E1C Link',site.E1pingstatus,site.E1CLink, site.E1txpacket, site.E1rxpacket, site.E1pinglost,site.E1CLinkstatus])
				site_writer.writerow([site.NAME, site.GNB, site.CUCPCOUNT, "CUCP",'sctpf1iwf', site.sctpf1iwf_status, site.sctpf1iwf_Rebootnumber, site.sctpf1iwf_UPtime,'CUCP to DU - F1C Link',site.F1Cpingstatus ,site.F1Cip, site.F1Ctxpacket, site.F1Crxpacket, site.F1Cpinglost,site.F1CLinkstatus])
				site_writer.writerow([site.NAME, site.GNB, site.CUCPCOUNT, "CUCP",'sctpxniwf', site.sctpxniwf_status, site.sctpxniwf_Rebootnumber, site.sctpxniwf_UPtime,'','','','','','',''])
				site_writer.writerow([site.NAME, site.GNB, site.CUCPCOUNT, "CUCP",'ueconmgr', site.ueconmgr_status, site.ueconmgr_Rebootnumber, site.ueconmgr_UPtime,'','','','','','',''])
				site_writer.writerow([site.NAME, site.GNB, site.CUUPCOUNT, "CUUP",'bccsvc', site.bccsvc_status, site.bccsvc_Rebootnumber, site.bccsvc_UPtime,'CUUP to DU - F1U Link',site.F1Upingstatus, site.F1Uip, site.F1Utxpacket, site.F1Urxpacket, site.F1Upinglost])
				site_writer.writerow([site.NAME, site.GNB, site.CUUPCOUNT, "CUUP",'bccsvc', site.bccsvc_status, site.bccsvc_Rebootnumber, site.bccsvc_UPtime,'CUUP to UPF DATA - N3 Link',site.N3pingstatus, site.N3Link, site.N3txpacket, site.N3rxpacket, site.N3pinglost])
				site_writer.writerow([site.NAME, site.GNB, site.CUUPCOUNT, "CUUP",'bccsvc', site.bccsvc_status, site.bccsvc_Rebootnumber, site.bccsvc_UPtime,'CUUP to UPF VOICE- N3 Link',site.N3pingstatusvoice, site.N3Linkvoice, site.N3txpacketvoice, site.N3rxpacketvoice, site.N3pinglostvoice])
				site_writer.writerow([site.NAME, site.GNB, site.CUUPCOUNT, "CUUP",'dalsvc', site.dalsvc_status, site.dalsvc_Rebootnumber, site.dalsvc_UPtime,'','','','','','',''])
				site_writer.writerow([site.NAME, site.GNB, site.CUUPCOUNT, "CUUP",'dprmsvc', site.dprmsvc_status, site.dprmsvc_Rebootnumber, site.dprmsvc_UPtime,'','','','','','',''])
				site_writer.writerow([site.NAME, site.GNB, site.CUUPCOUNT, "CUUP",'gwsvc', site.gwsvc_status, site.gwsvc_Rebootnumber, site.gwsvc_UPtime,'','','','','','',''])
				site_writer.writerow([site.NAME, site.GNB, site.CUUPCOUNT, "CUUP",'intfmgrsvc', site.intfmgrsvc_status, site.intfmgrsvc_Rebootnumber, site.intfmgrsvc_UPtime,'','','','','','',''])
				site_writer.writerow([site.NAME, site.GNB, site.CUUPCOUNT, "CUUP",'iwfsvc', site.iwfsvc_status, site.iwfsvc_Rebootnumber, site.iwfsvc_UPtime,'CUUP to CUCP - E1U Link',site.E1Upingstatus,site.E1ULink, site.E1Utxpacket, site.E1Urxpacket, site.E1Upinglost,site.E1ULinkstatus])
				site_writer.writerow([site.NAME, site.GNB, site.CUUPCOUNT, "CUUP",'srmsvc', site.srmsvc_status, site.srmsvc_Rebootnumber, site.srmsvc_UPtime,'','','','','','',''])			
					
		

	crt.Session.SetStatusText("Ready")
	crt.Dialog.MessageBox(dump_file_path, "File Saved Below Location" )		
		
############################     Login to Fujistu server    #################################################
	
Main()