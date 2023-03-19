import os
import sys
import uuid as UUID
import uvicorn
import schemas
import utils
import worker
from multiprocessing import Process, Queue
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse


# 
# MAIN LOOP
# 

# Function that performs reqested operations in parallel with API
def mainloop(q: Queue):
	while True:
		# Waiting for new request and or exiting in case of fatal error with queue
		try:
			qRes = q.get()
		except:
			# TODO log
			print('\nExiting...\n')
			sys.exit()

		# Checking validity of recieved data
		try:
			data: schemas.Default = qRes[0]
			cmd: str = qRes[1]
			uq: Queue = qRes[2]
		except:
			utils.raiseError(uq, 
				detail="Something wrong with query or data")
			continue

		# Completing received task
		if cmd == "new":
			# Checking existence of session
			# TODO DB
			if os.path.exists(f"Configs/{data.session_name}.json"):
				utils.raiseError(uq, 
					detail="Such session is already exist. Make new one with another name or delete the old one first")
				continue
			worker.new(uq, data)


		elif cmd == "change":
			pass
		elif cmd == "remove":
			pass
		elif cmd == "run":
			pass



# 
# API Functions
# 

app = FastAPI()

# Dictionary with unique queues - one queue for each post requests
uqDict = dict()

# TODO new, change, remove, run, stop, send
# Function that creats request for creating record in DB about new bot
@app.post("/new")
def new(data: schemas.New):
	# Making UUID for client to get result of operation
	uuid = str(UUID.uuid1())
	# Creating new queue for request
	uqDict[uuid] = Queue()
	# Sending request to complete the task
	q.put((data, "new", uqDict[uuid]))
	# Returning UUID to user
	return JSONResponse(
        status_code=202,
        content={
			"detail":"Request accepted. You can get result in /get_result by UUID",
			"uuid": uuid
		}
    )


# TODO Logging for every return or HTTP Exception
# TODO add deleting uq
# Function that returns result of previous request
@app.get("/get_result")
def get_result(uuid: str):
	# Checking validity of UUID
	try:
		uq = uqDict[uuid]
	except:
		raise HTTPException(
			status_code=404,
			detail="Wrong UUID. No such request"
			)
	
	# Checking completeness of request
	try:
		result = uq.get_nowait()
	except uq.Empty:
		return JSONResponse(
			# TODO Set another status code
			status_code=200,
			content={"detail":"Request accepted. Result is not ready. Try again later"}
		)
	
	# Returning error or result
	if result["status"] == "error":
		raise HTTPException(
			status_code=result["status_code"],
			detail=result["detail"]
			)
	else:
		return JSONResponse(
			status_code=200,
			content={result}
		)

@app.get("/test")
def test(msg: str):
	return JSONResponse(
		status_code=200,
		content={"message": msg}
	)



# 
# MAIN
# 

if __name__ == "__main__":
	# Getting all arguments
	args = utils.get_args()
	# Starting main loop process, and initialising queue to "talk" with it
	q = Queue()
	p = Process(target=mainloop, args=((q),))
	p.daemon = True
	p.start()
	# Starting API
	uvicorn.run(app, host=args.host, port=args.port)
