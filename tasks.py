import utils
import worker
import schemes
from multiprocessing import Process, Queue



# Function that completes /create task (Creates new bot session)
def create(q: Queue, botQDict: dict, uuid: str, session_name: str, data: schemes.CreateSession):
	# Adding queues for current session
	botQDict[session_name] = [Queue(), Queue()]
	# Starting process, that will make new bot session
	p = Process(target=worker.create, args=((q),(data),(uuid)))
	p.start()


# Function that completes /update task (Updates bot session)
def update(q: Queue, resQ: Queue, botQDict: dict, uuid: str, session_name: str, data: schemes.CreateSession, running: dict):
	# TODO remove WHEN DB
	if session_name not in botQDict:
		botQDict[session_name] = [Queue(), Queue()]
	if session_name in running and running[session_name]:
		processResponce(
			resQ, 
			utils.returnResponce(uuid, "update", session_name, 400,
				"Bot is running. At first /stop it"),
			running
		)
	# Starting process, that will update bot session
	p = Process(target=worker.update, args=((q),(data),(uuid)))
	p.start()


# Function that completes /remove task (Removes new bot session)
def remove(q: Queue, resQ: Queue, uuid: str, session_name: str, data: schemes.CreateSession, running: dict):
	if session_name in running and running[session_name]:
		processResponce(
			resQ, 
			utils.returnResponce(uuid, "update", session_name, 400,
				"Bot is running. At first /stop it"),
			running
		)
	# Starting process, that will remove bot session
	p = Process(target=worker.remove, args=((q),(session_name),(uuid)))
	p.start()


# Function that completes /start task (Runs definite bot session)
def start(q: Queue, resQ: Queue, botQDict: dict, uuid: str, session_name: str, running: dict):
	# Checking existence of session
	# TODO this check but for bot and not session only
	# TODO remove first condition WHEN DB
	if session_name in running and running[session_name]:
		processResponce(
			resQ, 
			utils.returnResponce(uuid, "start", session_name, 400,
				"Bot is already running. At first /stop it"),
			running
		)
		return
	# Adding queues for current session if there is no such
	# TODO change WHEN DB
	if session_name not in botQDict:
		botQDict[session_name] = [Queue(), Queue()]
	# Starting process, that will start bot session
	botQin = botQDict[session_name][0]
	botQout = botQDict[session_name][1]
	p = Process(target=worker.start, args=((q),(botQin),(botQout),(session_name),(uuid)))
	p.start()


# Function that completes /stop task (Stops definite bot session)
def stop(q: Queue, resQ: Queue, botQDict: dict, uuid: str, session_name: str, running: dict):
	# Checking existence of session
	# TODO remove first condition WHEN DB
	if session_name not in running or not running[session_name]:
		processResponce(
			resQ, 
			utils.returnResponce(uuid, "start", session_name, 400,
				"Bot is not running. At first /start it"),
			running
		)
		return
	# Starting process, that will stop bot session
	botQin = botQDict[session_name][0]
	botQout = botQDict[session_name][1]
	p = Process(target=worker.stop, args=((q),(botQin),(botQout),(uuid)))
	p.start()

# Function that completes /send task (Sends message from definite bot to definite user)
def send(q: Queue, resQ: Queue, botQDict: dict, uuid: str, session_name: str, data: schemes.CreateSession, running: dict):
	# Checking if session is already started
	# TODO this check but for bot and not session only
	# TODO remove first condition WHEN DB
	if session_name not in running or not running[session_name]:
		processResponce(
			resQ,
			utils.returnResponce(uuid, "send", session_name, 400,
				"Bot is not running. At first /start it"),
			running
		)
		return
	# Starting process, that will send message from bot session
	botQin = botQDict[session_name][0]
	botQout = botQDict[session_name][1]
	p = Process(target=worker.send, args=((q),(botQin),(botQout),(data),(uuid)))
	p.start()


# Function that processes requests coming to mainloop
def processRequest(q: Queue, qRes: list, botQDict: dict, resQ: Queue, running: dict):
	data, cmd, uuid = qRes
	session_name = data.session_name
	# Completing received task
	if cmd == "create":
		create(q, botQDict, uuid, session_name, data)
	elif cmd == "update":
		update(q, resQ, botQDict, uuid, session_name, data, running)
	elif cmd == "remove":
		remove(q, resQ, uuid, session_name, data, running)
	elif cmd == "start":
		start(q, resQ, botQDict, uuid, session_name, running)
	elif cmd == "stop":
		stop(q, resQ, botQDict, uuid, session_name, running)
	elif cmd == "send":
		send(q, resQ, botQDict, uuid, session_name, data, running)


# Function that processes responces to API
def processResponce(resQ: Queue, qRes: dict, running: dict):
	_, uuid, request_cmd, session_name, status_code, detail = qRes.values()
	# Saving running state for current session
	if request_cmd == "create" or request_cmd == "stop":
		if status_code == 200:
			running[session_name] = False
	if request_cmd == "start":
		if status_code == 200:
			running[session_name] = True
	
	# Returning responce to API
	resQ.put([uuid, status_code, detail])
