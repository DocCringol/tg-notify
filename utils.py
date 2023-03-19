import argparse
from multiprocessing import Queue


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
                        prog='tg-notify',
                        # TODO write description
                        description='API interface for you to send messages throught telegram bot')
    parser.add_argument('-H', '--host', default="127.0.0.1")
    parser.add_argument('-p', '--port', default=8000)
    args = parser.parse_args()
    return args

def raiseError(q: Queue, status_code: int = 404, detail: str = "Error"):
    q.put(
        {
			"status": "error",
			"status_code": status_code,
			"detail": detail
		}
    )


if __name__ == "__main__":
    print("\nThis is a module for tg-notify, don't try to run it as a script\n")
    args = vars(get_args())
    args = [(key, args[key]) for key in args]
    print("Args test:")
    print(*[f'{args[i][0]} - {args[i][1]};' for i in range(len(args))])
    print("\nError test")
    d = dict()
    raiseError(d, "213")
    print(d["213"])