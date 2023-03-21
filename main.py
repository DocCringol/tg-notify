import sys
import uuid as UUID
import uvicorn
import schemas
import utils
import tasks
from multiprocessing import Process, Queue
from fastapi import FastAPI
from fastapi.responses import JSONResponse



#
# MAIN LOOP
#

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
			tasks.processRequest(q, qRes["data"], botQDict, resQ, running)
		elif not qRes["fromAPI"]:
			tasks.processResponce(resQ, qRes, running)
		else:
			sys.exit()



# 
# API Functions
# 

app = FastAPI()

# Dictionary for results of requests (key - UUID)
results = dict()

# Function, that transfers all post request to mainloop
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
