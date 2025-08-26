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

class cell_site:
	def __init__(self, name, IP):
		self.name     		= name
		self.IP     		= IP
		self.csr_connected	= True
		

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
	#pwd = crt.Dialog.Prompt("Enter your password", "Password Prompt","",True)
	
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
		site_writer.writerow(['Site ID','Reachability Status'])

		for site in site_list:
			max_tries 		= 3
			counter 		= 0

			crt.Session.SetStatusText("Script running for " + site.name)
			crt.Screen.Send("ping " + site.IP + chr(13))

			crt.Screen.WaitForStrings("icmp_seq=2", 3)

			crt.Screen.Send (chr(3))
			time.sleep(1)
			row = crt.Screen.CurrentRow
			column = crt.Screen.CurrentColumn
		
			var = crt.Screen.Get(row-2, 1, row-2, column+25)
			#crt.Dialog.MessageBox("N2 Link interface result from CUCP to AMF\n\n\n" + str(var))
			splitted_line_sctp = var.split(",")
			txpacket= (splitted_line_sctp[0].split())[0]
			rxpacket = (splitted_line_sctp[1].split())[0]
			
			if txpacket == rxpacket and int(rxpacket) > 0:
				site.pingstatus = "YES"

			else:
				site.pingstatus = "NO"

					
			site_writer.writerow([site.name, site.pingstatus])




	crt.Dialog.MessageBox(dump_file_path, "File Saved Below Location" )

	# os.chdir(Save_path)

	os.startfile(dump_file_path)

	
Main()