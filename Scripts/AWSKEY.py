# $language = "Python"
# $interface = "1.0"

########################------------------------------------------------------###################################
######################## For issue Please contact jayeshkumar.patel@dish.com ####################################
########################------------------------------------------------------###################################

def Main():

	crt.Screen.Send("SET AWS_ACCESS_KEY_ID=ASIA5YFOJBT7W2563YDF" + chr(13))
	crt.Screen.Send("SET AWS_SECRET_ACCESS_KEY=4W6MgiFlowp2wL7RRkrY9pX7nNGgdl8emYUnzS3s" + chr(13))
	crt.Screen.Send("SET AWS_SESSION_TOKEN=IQoJb3JpZ2luX2VjEBgaCXVzLXdlc3QtMiJHMEUCIGWex9JdmELkNEiqblaKWiv+ceC2apyJw3PzCXODEU8dAiEAwOjTriXvAVhPMy2FNxCCPfSRNgl2fUEFG/bP/wYm5ZEqpwMIkf//////////ARAAGgw5NDUyNTgzMDI3MTkiDDToSze4UccRPBxn8Sr7AqXSgcqqKQw6B0AcpslnFN7T/nwfktAH5GvlbYUlGYaLjuJ1JwTVBJL0vtedg9qj3CvRV7+qoSfLsH6CZG5p1eShIc89KnqTP4rSa+5uQbBDROH5WpJCIfOd2eubedPH4mkG0WjL8EagyVnLnQd80qmZbwC26ztSuev6ksvJ+I/AR8ZnWfKU7daHuYKsJbJLSlvyETDer/649WXWYgmEcc5ZMbPUfCS3umyTTE2q28QGjjDX0ad/FkgAnKfFchQ/Fr7mAunWzRiH0Ow28l1iJG+djvVSD/ANjm8wwtgvCbSrwxmM/2AtUgbkrP8wKwTreyfaTKqPZmEJB3cV2rPeVzJyBQDG1BJjkBJepG2d+zQcUelB8rrFjrvNUunBvIQ+0MmSHeWQZXwW6rkUYn0JqYzAsVWtXy8qgfCE/kaS+kIyrn9VgE7IDE1MrKhrUvzZHPX/WgIDN2RAEIFg6rKBx2+z1eT/ozSJvn4B50PXDNZwBuo7iiSRx4ZbuZww8bPavwY6pgFa5lj8J7gB8oQsVj0536I1VOPIO2t+Yrqpe5rXlptGls7xQ873DhTPDiGfZm55Z3Fxk3uI2zIWaVjdtx4tReXv3ICMrJKcuZq6BJhbpPDuDIOXTZFCzTQh35ueobAsrNx53Ctt8KbGwzJWgaHYlHYzKSdUHKD8i2ZTITt0TFZ9IG6I0PdagLT/thwtzmM3WsJ2xbxPCsjAAS8LWi2lx+3sFZ7Xi9zi" + chr(13))
	crt.Screen.Send('aws ssm start-session --target i-037ff342bf1032826 --document-name AWS-StartPortForwardingSession --parameters portNumber="3128",localPortNumber="9998" --region us-east-1' + chr(13))
	
Main()