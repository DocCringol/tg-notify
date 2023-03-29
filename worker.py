import os
import utils
import schemes
from crud import *
from telethon.sync import TelegramClient
from multiprocessing import Process, Queue



def bot_(qIn: Queue, qOut: Queue, session_name: str, run_uuid: str):
	session = get_session(session_name)
	print(session)
	if session is NOT_EXIST:
		qOut.put(
			utils.returnResponce(run_uuid, "run", session_name, 404, 
				"No such session. At first /create a new one")
		)
		return

	try:
		bot = TelegramClient(
				f"Sessions/{session_name}", 
				session.api_id,
				session.api_hash,
		)
		bot.start(bot_token=session.bot_token)
	except:
		qOut.put(
			utils.returnResponce(run_uuid, "start", session_name, 400, 
				"Error while starting bot. Please, check internet connection")
		)
		return
	
	qOut.put(
		utils.returnResponce(run_uuid, "start", session_name, 200, 
			"Bot is running")
	)

	while True:
		request = qIn.get()
		cmd = request[0]
		if cmd == "send":
			_, user, msg, uuid = request
			try:
				bot.send_message(user, msg)
				qOut.put(
					utils.returnResponce(uuid, cmd, session_name, 200, 
						"Message sent successfully")
				)
			except:
				qOut.put(
					utils.returnResponce(uuid, cmd, session_name, 400, 
						"Error while trying to send message. Check validity of contact data")
				)
				continue
		elif cmd == "stop":
			_, uuid = request
			break
	qOut.put(
		utils.returnResponce(uuid, cmd, session_name, 200, 
			"Bot is stopped")
	)


def create(q: Queue, data: schemes.CreateSession, uuid: str):
	session_name = data.session_name
	# Testing data (could we run bot with this data?)
	try:
		TelegramClient(
			f"Sessions/{session_name}", 
			data.api_id, 
		    data.api_hash
		).start(bot_token=data.bot_token)
	except:
		q.put(
			utils.returnResponce(uuid, "create", session_name, 400, 
				"Invalid app/bot data")
		)
		return
	
	if create_session(data) is SESSION_ALREADY_EXIST:
		q.put(
			utils.returnResponce(uuid, "create", session_name, 409, 
				f"Session already exist. At first /remove session with name: {session_name}. Or /update it, if you want to change data")
		)
		return
	
	q.put(
		utils.returnResponce(uuid, "create", session_name, 200, 
			"Bot added and tested successfully")
	)


def update(q: Queue, data: schemes.UpdateSession, uuid: str):
	session_name = data.session_name
	session = get_session(session_name)
	if session is NOT_EXIST:
		q.put(
			utils.returnResponce(uuid, "update", session_name, 404, 
				"Session doesn't exist. At first /create it")
		)
		return
	
	os.remove(f"Sessions/{session_name}.session")
	update_session(data)
	# new_session = get_session(session_name)
	# TODO valid testing of corect data
	# try:
	# 	TelegramClient(
	# 		f"Sessions/{session_name}", 
	# 		new_session.api_id, 
	# 	    new_session.api_hash
	# 	).start(bot_token=new_session.bot_token)
	# except:
	# 	remove_session(session_name)
	# 	data = schemes.CreateSession(session_name=session_name, api_id=session.api_id,
	# 		       api_hash=session.api_hash, bot_token=session.bot_token)
	# 	print('\n\n')
	# 	print(data)
	# 	print(create_session(data))
	# 	print('\n\n')
	# 	q.put(
	# 		utils.returnResponce(uuid, "update", session_name, 400, 
	# 			"Invalid app/bot data")
	# 	)
	# 	return
	
	q.put(
		utils.returnResponce(uuid, "update", session_name, 200, 
			"Session updated and tested successfully")
	)

def remove(q: Queue, session_name: str, uuid: str):
	if remove_session(session_name) is NO_SUCH_SESSION:
		q.put(
			utils.returnResponce(uuid, "remove", session_name, 404, 
				"Session doesn't exist. At first /create it")
		)
		return
	os.remove(f"Session/{session_name}.session")
	q.put(
		utils.returnResponce(uuid, "remove", session_name, 200, 
			"Succesfully removed session")
	)
	

def start(q: Queue, botQin: Queue, botQout: Queue, session_name: str, uuid: str):
	p = Process(target=bot_, args=((botQin),(botQout),(session_name),(uuid)))
	p.start()
	q.put(botQout.get())


def stop(q: Queue, botQin: Queue, botQout: Queue, uuid: str):
	botQin.put(["stop", uuid])
	q.put(botQout.get())


def send(q: Queue, botQin: Queue, botQout: Queue, data: schemes.SendMessage, uuid: str):
	botQin.put(["send", data.user, data.msg, uuid])
	q.put(botQout.get())



if __name__ == "__main__":
	print("\nThis is a module for tg-notify, don't try to run it as a script\n")

	print("\nTest\n")
	q = Queue()
	botQin = Queue()
	botQout = Queue()
	session_name = input("\nInput session name:\n")
	data = schemes.SendMessage(session_name=session_name, user=input("\nInput nickname with @:\n"), msg=input("\nInput message:\n"))
	uuid = "test"

	start(q, botQin, botQout, session_name, "test")
	print(q.get())

	send(q, botQin, botQout, data, "test")
	print(q.get())