from pydantic import BaseModel
from fastapi import File, UploadFile

class Default(BaseModel):
    session_name: str
    api_id: str | None = None
    api_hash: str | None = None
    bot_token: str | None = None
    msg: str | None = None

class New(BaseModel):
    session_name: str
    api_id: str
    api_hash: str
    bot_token: str
    
class Change(BaseModel):
    session_name: str
    api_id: str | None = None
    api_hash: str | None = None
    bot_token: str | None = None
    
class Remove(BaseModel):
    session_name: str

class Run(BaseModel):
    session_name: str
    
class Stop(BaseModel):
    session_name: str
    
class Send(BaseModel):
    session_name: str
    msg: str

if __name__ == "__main__":
    print("\nThis is a module for tg-notify, don't try to run it as a script\n")
