import argparse
from multiprocessing import Queue


def get_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(
						prog='tg-notify',
						description='API interface for you to send messages throught telegram bots')
	parser.add_argument('-H', '--host', default="127.0.0.1")
	parser.add_argument('-p', '--port', default=8000)
	args = parser.parse_args()
	return args

def returnResponce(uuid: str, request_cmd: str, session_name: str, 
		   		status_code: int = 200, detail: str = "OK"):
	return 	{
				"fromAPI": False,
				"uuid": uuid,
				"request_cmd": request_cmd,
				"session_name": session_name,
				"status_code": status_code,
				"detail": detail
			}


if __name__ == "__main__":
	print("\nThis is a module for tg-notify, don't try to run it as a script\n")

	args = vars(get_args())
	args = [(key, args[key]) for key in args]
	print("Args test:")
	print(*[f'{args[i][0]} - {args[i][1]};' for i in range(len(args))])

	print("\nError test")
	q = Queue()
	uuid = "test"
	request_cmd = "send"
	returnResponce(q, uuid, request_cmd)
	print(q.get())