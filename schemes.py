from pydantic import BaseModel

class Default(BaseModel):
    session_name: str
    api_id: str | None = None
    api_hash: str | None = None
    bot_token: str | None = None
    default_user: str | None = None
    msg: str | None = None

class CreateSession(BaseModel):
    session_name: str
    api_id: str
    api_hash: str
    bot_token: str
    default_user: str | None = None
    
class UpdateSession(BaseModel):
    session_name: str
    api_id: str | None = None
    api_hash: str | None = None
    bot_token: str | None = None
    default_user: str | None = None
    
class RemoveSession(BaseModel):
    session_name: str
    
class StartSession(BaseModel):
    session_name: str
    
class StopSession(BaseModel):
    session_name: str
    
class SendMessage(BaseModel):
    session_name: str
    user: str | None = None
    msg: str

if __name__ == "__main__":
    print("\nThis is a module for tg-notify, don't try to run it as a script\n")
