import os
import sys
import uuid as UUID
import uvicorn
import schemas
import utils
import worker
from multiprocessing import Process, Queue
from fastapi import FastAPI
from fastapi.responses import JSONResponse



#
# MAIN LOOP
#

# Function that process requests getting in mainloop
def processRequest(q: Queue, qRes: list, botQDict: dict, resQ: Queue, running: dict):
	data, cmd, uuid = qRes
	session_name = data.session_name

	# Completing received task
	if cmd == "new":
		# Checking existence of session
		# TODO change WHEN DB
		if os.path.exists(f"Configs/{session_name}.json"):
			processResponce(
				resQ,
				utils.returnResponce(uuid, cmd, session_name, 400, 
					"Such session is already exist. /create new one with another name or /remove the old one first"),
				running
			)
			if session_name not in botQDict:
				botQDict[session_name] = [Queue(), Queue()]
			return
		botQDict[session_name] = [Queue(), Queue()]
		p = Process(target=worker.new, args=((q),(data),(uuid)))
		p.start()

	elif cmd == "change":
		pass
	elif cmd == "remove":
		pass
	elif cmd == "run":
		# TODO change WHEN DB
		if not os.path.exists(f"Configs/{session_name}.json") or \
			not os.path.exists(f"Sessions/{session_name}.session"):
			processResponce(
				resQ, 
				utils.returnResponce(uuid, cmd, session_name, 404,
					"No such session exists. At first /create it"),
				running
			)
			return
		# TODO del first condition WHEN DB
		if session_name in running and running[session_name]:
			processResponce(
				resQ, 
				utils.returnResponce(uuid, cmd, session_name, 400,
					"Bot is already running. At first /stop it"),
				running
			)
			return
		# TODO change WHEN DB
		if session_name not in botQDict:
			botQDict[session_name] = [Queue(), Queue()]
		botQin = botQDict[session_name][0]
		botQout = botQDict[session_name][1]
		p = Process(target=worker.run, args=((q),(botQin),(botQout),(session_name),(uuid)))
		p.start()

	elif cmd == "stop":
		pass

	elif cmd == "send":
		botQin = botQDict[session_name][0]
		botQout = botQDict[session_name][1]
		p = Process(target=worker.send, args=((q),(botQin),(botQout),(data),(uuid)))
		p.start()


# Function that process responce getting in mainloop
def processResponce(resQ: Queue, qRes: dict, running: dict):
	_, uuid, request_cmd, session_name, status_code, detail = qRes.values()
	if request_cmd == "new":
		if status_code == 200:
			running[session_name] = False
	if request_cmd == "run":
		if status_code == 200:
			running[session_name] = True
	resQ.put([uuid, status_code, detail])


# Function that performs reqested operations in parallel with API
def mainloop(q: Queue, resQ: Queue, running: dict):
	botQDict = dict()
	while True:
		# Waiting for new request and or exiting in case of fatal error with queue
		try:
			qRes = q.get()
		except:
			# TODO Logging
			print('\nExiting...\n')
			sys.exit()

		# Processing Request or Responce, depending on what were inside of queue
		if qRes["fromAPI"]:
			processRequest(q, qRes["data"], botQDict, resQ, running)
		elif not qRes["fromAPI"]:
			processResponce(resQ, qRes, running)
		else:
			sys.exit()



# 
# API Functions
# 

app = FastAPI()

# Dictionary for results of requests (key - UUID)
results = dict()

def post(cmd: str, data: schemas.Default):
	# Making UUID for client to get result of operation
	uuid = str(UUID.uuid1())
	# Adding UUID to list of results (False - responce is not ready)
	results[uuid] = False
	# Sending request to complete the task
	q.put(
		{
			"fromAPI": True,
			"data": [data, cmd, uuid]
		}
	)
	# Returning UUID to user
	return JSONResponse(
        status_code=202,
        content={
			"detail":"Request accepted. You can get result in /get_result by UUID",
			"uuid": uuid
		}
    )

# TODO Add  functions
# Function that creats request for creating record in DB about new bot
@app.post("/new")
def new(data: schemas.New):
	return post("new", data)

# Function that starts up definite bot
@app.post("/run")
def run(data: schemas.Run):
	return post("run", data)

# Function that sends messege from definite bot
@app.post("/send")
def send(data: schemas.Send):
	return post("send", data)


# TODO Logging
# Function that returns result of previous request
@app.get("/get_result")
def get_result(uuid: str):
	# Processing and saving results
	while not resQ.empty():
		res = resQ.get()
		results[res[0]] = [res[1], res[2]]

	# Checking validity of UUID
	try:
		result = results[uuid]
	except:
		return JSONResponse(
			status_code=404,
			content={"detail":"Wrong UUID. No such request"}
		)
	
	# Checking completeness of request
	if result:
		# Deleting returned result
		results.pop(uuid)
		# Returning responce
		return JSONResponse(
			status_code=result[0],
			content={ "detail": result[1] }
		)
	else:
		return JSONResponse(
			status_code=202,
			content={"detail":"Request accepted. Result is not ready. Try again later"}
		)



# 
# MAIN
# 

if __name__ == "__main__":
	# Getting all arguments
	args = utils.get_args()
	# Dictionary of sessions running
	running = dict()
	# Starting main loop process, and initialising queues to "talk" with it
	q = Queue()
	resQ = Queue()
	p = Process(target=mainloop, args=((q),(resQ),(running)))
	p.start()
	# Starting API
	uvicorn.run(app, host=args.host, port=args.port)
