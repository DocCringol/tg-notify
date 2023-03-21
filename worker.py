import time
import json
import utils
import schemes
from dotmap import DotMap
from telethon.sync import TelegramClient, events
from multiprocessing import Process, Queue



def bot_(qIn: Queue, qOut: Queue, session_name: str, run_uuid: str):
	try:
		cfg = DotMap(json.load(open(f"Configs/{session_name}.json")))
		bot = TelegramClient(
				f"Sessions/{session_name}", 
				cfg.api_id,
				cfg.api_hash
		)
		bot.start()
		qOut.put(
			utils.returnResponce(run_uuid, "start", session_name, 200, 
				"Bot is running")
		)
		
	except:
		qOut.put(
			utils.returnResponce(run_uuid, "start", session_name, 200, 
				"Something wrong. Maybe, wrong session")
		)
		return

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


def create(q: Queue, data: schemes.CreateSession, uuid: str):
	session_name = data.session_name
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
	cfg_data = {
		"api_id": data.api_id,
		"api_hash": data.api_hash,
		"bot_token": data.bot_token
	}
	json_cfg = json.dumps(cfg_data)
	with open(f"Configs/{session_name}.json", "w") as cfg:
		cfg.write(json_cfg)
	
	q.put(
		utils.returnResponce(uuid, "create", session_name, 200, 
			"Bot added and tested successfully")
	)


def start(q: Queue, botQin: Queue, botQout: Queue, session_name: str, uuid: str):
	p = Process(target=bot_, args=((botQin),(botQout),(session_name),(uuid)))
	p.start()
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
	data = schemes.SendMessage
	data.session_name = session_name
	data.user = input("\nInput nickname with @:\n")
	data.msg = input("\nInput message:\n")
	uuid = "test"
	start(q, botQin, botQout, session_name, "test")
	print(q.get())
	send(q, botQin, botQout, data, "test")
	print(q.get())