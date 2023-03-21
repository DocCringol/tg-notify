<style>
	.attention {
		font-size: 1.5rem;
		font-weight: 1000;
	}
</style>

# tg-notify

## About project

This is basically a "telegram bot manager" for simply sending messages, such as notifications.

Later could be extensions of posibilities of bot itself.

### Example of Usage

Imagine you have a program that you need to extract information from and send it somewhere else. For example, a parser for a news site or school Olympiad that sends notifications when new news is uploaded. We'll call this program the "client".

A really good option for you is to send a message to yourself through Telegram. To do this, you need to write code that will run the bot and send the message. But instead of that, you could just use tg-notify. You'll only need to write a couple of lines of code to send requests to the tg-notify API.

1. Run tg-notify.
2. Run the client.
3. The client should send requests to the local tg-notify API.
    1. /create a bot session with the given arguments: api_id, api_hash, bot_token.
    2. /run this bot session.
    3. /send a message through this session to a specific user for as long as you want.
    4. /stop this bot session if you need to.

And you could run as many sessions as you want for as many clients as you want. All you have to do is run only one instance of tg-notify and create a new Telegram bot with its own token for each session.

All of runs in parallel using multiprocessing.

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

### /update - update session 
<span class="attention">
	MAJOR ISSUES with /update<br>
	Better use /remove and /create for now
</span>

###

```
data:
    session_name: str
    api_id: str | None = None
    api_hash: str | None = None
    bot_token: str | None = None
	default_user: str | None = None
```

### /remove - delete session
```
data:
    session_name: str
```

### /start - start definite session
```
data:
    session_name: str
```

### /stop - stop definite session
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

-	Configure logging
-	Refactoring
-	Write example client script
-	Transfer some "global" variables to database
-	Add better global exceprion catching
-	Add support of default user for session
-	Add check - if bot is running elsewhere (not in tg-notify)
