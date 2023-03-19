import json
import schemas
from telethon.sync import TelegramClient
from multiprocessing import Process, Queue


# def bot(q: Queue, config_file: str):
# 	cfg = DotMap(json.load(open(config_file)))
# 	client = TelegramClient(cfg.NAME, cfg.API_ID, cfg.API_HASH)
# 	client.start()
# 	client.run_until_disconnected()
# 	while True:
# 		try:
# 			client.send_message(cfg.ADMIN, q.get())
# 		except:
# 			client.send_message(cfg.ADMIN, "НЕУДАЧНАЯ ПОПЫТКА ОТПРАВКИ СООБЩЕНИЯ")

def new(q: Queue, data: schemas.New):
	print('DICK')
	q[data.session_name].put(
		{
			"detail": "test"
		}
	)
	# try:
	# 	bot = TelegramClient(
	# 		data.session_name, 
	# 		data.api_id, 
	# 	    data.api_hash
	# 	).start(bot_token=data.bot_token)
	# except:
	# 	pass
	# cfg_data = {
	# 	"api_id": data.api_id,
	# 	"api_hash": data.api_hash,
	# 	"bot_token": data.bot_token
	# }
	# json_cfg = json.dumps(cfg_data)
	# with open(f"Configs/{data.session_name}.json", "w") as cfg:
	# 	cfg.write(json_cfg)

# def run_bot(q: Queue, config_file: str):
# 	print(q, config_file)
# 	# q = Queue()
# 	# p = Process(target=main_loop, args=((q)))
# 	# p.daemon = True
# 	# p.start()
# 	# uvicorn.run(app, host=args.host, port=args.port))



if __name__ == "__main__":
	print("\nThis is a module for tg-notify, don't try to run it as a script\n")