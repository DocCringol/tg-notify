import json
import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from telethon.sync import TelegramClient
from multiprocessing import Process, Queue
from dotmap import DotMap

app = FastAPI()
q = Queue()

def bot(q: Queue):
	# CFG tg
	cfg = DotMap(json.load(open("config.json")))
	client = TelegramClient("Me", cfg.API_ID, cfg.API_HASH)
	client.start()
	while True:
		try:
			client.send_message(cfg.ADMIN, q.get())
		except:
			client.send_message(cfg.ADMIN, "НЕУДАЧНАЯ ПОПЫТКА ОТПРАВКИ СООБЩЕНИЯ")
	# TODO exit

# TODO HTTPExceptions
@app.post("/")
def send_message(msg: str):
	q.put(msg)
	return 0

if __name__ == "__main__":
	p = Process(target=bot, args=((q),))
	p.daemon = True
	p.start()
	uvicorn.run(app, host="127.0.0.1", port=8001)