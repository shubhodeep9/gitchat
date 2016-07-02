#telnet program example
import socket,select,string,sys

from multiprocessing import Process
messages=[]

def A(sock,s):
		
		if sock==s:
			data = sock.recv(4096)
			if not data:
				print '\n Disconnected from chat server'
				sys.exit()
			else:
				messages.append(data)

def B(msg):
	global messages
	if msg:
		for y,x in enumerate(messages):
				sys.stdout.write(x)
				del messages[y]
		s.send(msg)
		prompt()
		messages=[]

def prompt():
	sys.stdout.write('<You>')
	sys.stdout.flush()

if __name__ =='__main__':
	if(len(sys.argv) < 3):
		print 'Usage : python telnet.py hostname port'
		sys.exit()

	host = sys.argv[1]
	port = int(sys.argv[2])

	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.settimeout(2)

	try:
		s.connect((host,port))
	except:
		print 'Unable to connect'
		sys.exit()

	print ' Connected to remote host. Start sending messages'
	prompt()
	while 1:
		socket_list=[sys.stdin,s]
		read_sockets,write_sockets,error_sockets =select.select(socket_list,[],[])
		for sock in read_sockets:
			msg = sys.stdin.readline()
			Process(target=A(sock,s)).start()
			Process(target=B(msg)).start()
				

