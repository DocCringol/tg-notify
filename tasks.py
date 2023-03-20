import os
import utils
import worker
import schemas
from multiprocessing import Process, Queue



# Function that completes /new task (Creates new bot session)
def new(q: Queue, resQ: Queue, botQDict: dict, uuid: str, session_name: str, data: schemas.New, running: dict):
    # Checking existence of session
	# TODO change WHEN DB
	if os.path.exists(f"Configs/{session_name}.json"):
		processResponce(
			resQ,
			utils.returnResponce(uuid, "new", session_name, 400, 
				"Such session is already exist. /create new one with another name or /remove the old one first"),
			running
		)
		# Adding queues for current session if there is no such
		# TODO remove WHEN DB
		if session_name not in botQDict:
			botQDict[session_name] = [Queue(), Queue()]
		return
	# Adding queues for current session
	botQDict[session_name] = [Queue(), Queue()]
	# Starting process, that will make new bor session
	p = Process(target=worker.new, args=((q),(data),(uuid)))
	p.start()


# Function that completes /run task (Runs definite bot session)
def run(q: Queue, resQ: Queue, botQDict: dict, uuid: str, session_name: str, running: dict):
	# Checking existence of session
	# TODO change WHEN DB
	if not os.path.exists(f"Configs/{session_name}.json") or \
		not os.path.exists(f"Sessions/{session_name}.session"):
		processResponce(
			resQ, 
			utils.returnResponce(uuid, "run", session_name, 404,
				"No such session exists. At first /create it"),
			running
		)
		return
	# Checking if session is already started
	# TODO this check but for bot and not session only
	# TODO remove first condition WHEN DB
	if session_name in running and running[session_name]:
		processResponce(
			resQ, 
			utils.returnResponce(uuid, "run", session_name, 400,
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
	p = Process(target=worker.run, args=((q),(botQin),(botQout),(session_name),(uuid)))
	p.start()


# Function that completes /send task (Sends message from definite bot to definite user)
def send(q: Queue, resQ: Queue, botQDict: dict, uuid: str, session_name: str, data: schemas.New, running: dict):
	# Checking if session is already started
	# TODO this check but for bot and not session only
	# TODO remove first condition WHEN DB
	if session_name not in running or not running[session_name]:
		processResponce(
			resQ,
			utils.returnResponce(uuid, "send", session_name, 400,
				"Bot is not running. At first /run it"),
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
	if cmd == "new":
		new(q, resQ, botQDict, uuid, session_name, data, running)
	elif cmd == "change":
		pass
	elif cmd == "remove":
		pass
	elif cmd == "run":
		run(q, resQ, botQDict, uuid, session_name, running)
	elif cmd == "stop":
		pass
	elif cmd == "send":
		send(q, resQ, botQDict, uuid, session_name, data, running)


# Function that processes responces to API
def processResponce(resQ: Queue, qRes: dict, running: dict):
	_, uuid, request_cmd, session_name, status_code, detail = qRes.values()
	# Saving running state for current session
	if request_cmd == "new":
		if status_code == 200:
			running[session_name] = False
	if request_cmd == "run":
		if status_code == 200:
			running[session_name] = True
	# Returning responce to API
	resQ.put([uuid, status_code, detail])