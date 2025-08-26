# $language = "Python"
# $interface = "1.0"

########################------------------------------------------------------###################################
######################## For issue Please contact jayeshkumar.patel@dish.com ####################################
########################------------------------------------------------------###################################

def Main():

	crt.Screen.Send(chr(13))
	row = crt.Screen.CurrentRow
	column = crt.Screen.CurrentColumn
	var = crt.Screen.Get(row, 1, row, column)
	x = var.split("\\")
	username = x[2].replace(" ", "" )
	username = username.replace(">", "" )

	x = username.split(".")
	firstname = x[0]
	Lastname = x[1]
	username = firstname + "_" + Lastname
	crt.Screen.Send("ssh -C -L 9998:localhost:9998 -L 33891:localhost:3389 " + username + "@localhost -p9922" + chr(13))
	crt.Screen.WaitForStrings("password", 3)
	crt.Screen.Send("Ambica!29041" + chr(13))
	crt.Screen.WaitForStrings(username, 3)
	crt.Screen.Send("proxy-connect" + chr(13))
	
Main()