# from multiprocessing import Queue
# import models
# import utils

# def create(q: Queue, data: models.CreateModel):
# 	pass

# def main(q: Queue, data: models.DefaultModel, cmd: str):
# 	if not isinstance(q, Queue):
# 		return
# 	if not isinstance(data, models.DefaultModel) \
# 	or not isinstance(cmd, str):
# 		utils.raiseError(q, detail="Incorrect data")
# 		return
	
# 	if cmd == "create":
# 		create(q, data)
# 	elif cmd == "change":
# 		pass
# 	elif cmd == "remove":
# 		pass
# 	elif cmd == "run":
# 		pass

# if __name__ == "__main__":
#     print("\nThis is a module for tg-notify, don't try to run it as a script\n")