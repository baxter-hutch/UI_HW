import os
import time
import threading
from threading import *
from os import listdir #list files as array
import serial
import math

#https://stackoverflow.com/questions/676172/full-examples-of-using-pyserial-package
ser = serial.Serial( #Create object "ser" in the form defined and specified as class "Serial" of library "serial".
	baudrate=9600,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
	timeout=3)

class Serial_Device: #Create class called "Serial_Device" that holds the hardware info. ID & Description = class properties.
	def __init__(self, ID, Description):
		self.ID = ID
		self.Description = Description


class rx_object:
	def __init__(self):
		self.flag_endThread = 0
		#self.thread_rx

	def thread_start(self):
		try:
			time.sleep(.5)
			self.flag_endThread = 0
			thread_rx = threading.Thread(target=self.rx_print)
			print(thread_rx.is_alive())
			thread_rx.start()
			print(thread_rx.is_alive())
		except:
			print("ERROR: serial. try [x] to connect to a serial port. Ending thread.")
			self.thread_end()

	def thread_end(self):
		self.flag_endThread = 1

	#def thread_check(self):
		#return self.thread_rx.is_alive()


	def rx_print(self): #This method lives in it's own thread.  This thread should be terminated whenever main thread user input != "r".
		data_string = ""
		while self.flag_endThread == 0:
			data_currentByte = ser.readline(1) #byte
			if data_currentByte >= b'\x20' and data_currentByte <= b'\x7E': #Filter out everything but ascii 32(hex.20, "!") to 126(hex.7E, "~").  b'\x00'
				data_currentByte = data_currentByte.decode('utf-8') #decode to string
				data_string += data_currentByte #build printable data string.
				if len(data_string) > 255:
					print("ERROR: data_string overrun(>255 bytes).")
					data_currentByte = "\r" #exit loop, garbage will be printed, then data_sting will be reset.
					#data_string = "" #reset data, stay in loop.
			if data_currentByte == ".":
				print(data_string)
				data_string = ""
				#ser.reset_input_buffer()
			#time.sleep(.1)


list_DeviceData_Serial = []
list2_DeviceData_Serial = []

do_exit = False
i = 0
line = []
serialDir = '/dev/serial/by-id/'
flag_rx_close = False

#declare rx class object here.
rx_conn = rx_object()

list_menu_main = [
"MAIN MENU COMMANDS:",
"[x] connect to serial port.",
"[r] read serial port.",
"[q] quit."]

while do_exit == False:
	#Print all items in menu list(s).
	menu = list_menu_main
	for i in range(len(menu)):
		print(menu[i])
	userInput = input(":") #Get user input.
	#end menu


	if flag_rx_close == True and userInput != "r":
		#print("Thread alive:".format(rx_conn.thread_check()))
		rx_conn.thread_end()

		#rx_conn.flag_endThread = 1
		thread1.join()
		print(thread1.is_alive())
		print("RX thread has been closed.")

		flag_rx_close = False


	if userInput == "x": #Scan for serial ports that 
		try:
			aID = sorted(listdir(serialDir))

			for i in range(len(aID)):
				ID = os.path.realpath(serialDir + aID[i]) #use realpath to get canonical path of device.
				Description = aID[i]

				list_DeviceData_Serial.append(Serial_Device(ID, Description))
				list2_DeviceData_Serial.append(list_DeviceData_Serial)
					#save device IDs and Descriptions to class object.
				print("Target:", i)
				print(list_DeviceData_Serial[i].Description)
				print(list_DeviceData_Serial[i].ID)
				print("") #create blank line.


			print("[#] Enter the desired target number to connect to its corresponding serial port.")
			print("[m] Go to the main menu.")

			userInputGood_loop = False
			while userInputGood_loop == False:
				userInput = input(":") #Get user input.

				if(userInput == "m"):
					userInputGood_loop = True
					loop = False #Collapse loop, drop to main menu.

				else:
					try:
						userInput = int(userInput)
						ser = serial.Serial(list_DeviceData_Serial[userInput].ID)
						ser.baudrate = 38400
						print(ser)
						#whichport = list_DeviceData_Serial[userInput].ID
						print("Targeted:", list_DeviceData_Serial[userInput].Description)
						userInputGood_loop = True
					except:
						print("Invalid input.")
		except:
			print("No device detected.")


	if userInput == "t":
		print(thread_rx.is_alive())
		m = 10
		l = 10
		#
		ser.write(b'!') #start byte
		#
		data_RX_byteCount = 2
		data_RX_byteCount = data_RX_byteCount.to_bytes(1, 'big')
		ser.write(data_RX_byteCount) #data bytes count
		#
		ser.write(b'D') #Addr byte
		#
		ser.write(m) #data: MSB
		ser.write(l) #data: LSB


	if(userInput == "r"):
		#access rx class object methods here.
		if ser.is_open is True:
			print("port is open.")

		rx_conn.flag_endThread = 0

		thread1 = threading.Thread(target=rx_conn.rx_print)
		thread1.daemon = True
		thread1.start()

		while thread1.is_alive() == False:
			pass

		flag_rx_close = True


	if(userInput == "q"): #Quit/Exit
		ser.close()
		do_exit = True
		#exit()
	#do_exit == True #Exit script



