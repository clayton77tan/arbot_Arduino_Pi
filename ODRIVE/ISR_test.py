import threading

def printfunc():
	print("2 sec")

def func():
	print("1 sec")
	
while True:
	event1 = threading.Event()
	event1.wait(2)
	printfunc()
	event2 = threading.Event()
	event2.wait(1)
	func()


