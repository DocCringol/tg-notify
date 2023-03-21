# tg-notify

## Installation

Required Python 3.10 and above

Tested on Python 3.10.10

```
pip install -r requirements.txt
```
## Usage

```
python main.py -h 
# or --help for list of commands

# Example of usage
python main.py -H <host> -p <port> -c <config-dir>
```

## API

### /create - add new session (one session - one bot)
```
data:
    session_name: str
    api_id: str
    api_hash: str
    bot_token: str
	default_user: str | None = None
```

### /start - start definite session
```
data:
    session_name: str
```

### /send - send message from definite bot to defenite user 
User defines only by username for now
```
data:
    session_name: str
    username: str
    msg: str
```

## To-do

-	Add the rest of the functions: change, remove, stop
-	Configure logging
-	Add more comments
-	Write example client script
