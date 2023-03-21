from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Session
import schemes

engine = create_engine('sqlite:///db/sessions.db')
DBSession = sessionmaker(bind=engine)
db = DBSession()
Base.metadata.create_all(engine)

# Constants
NOT_EXIST = None
NO_SUCH_SESSION = False
SESSION_ALREADY_EXIST = False
OK = True



def db_row_to_dict(row):
    return {key: value for key, value in row.__dict__.items() if not key.startswith('_')}

def print_db_row(row):
	if row is NOT_EXIST:
		print("NO SUCH SESSION")
	else:
		print(*db_row_to_dict(row).values())

# def dict_to_db_row(model, dictionary):
#     return model(**dictionary)



def create_session(data: schemes.CreateSession):
	session = get_session(data.session_name)

	if session is NOT_EXIST:
		user = Session(
			session_name=data.session_name, api_id=data.api_id, api_hash=data.api_hash, 
			bot_token=data.bot_token, default_user=data.default_user
		)
		db.add(user)
		db.commit()
		return OK
	
	return SESSION_ALREADY_EXIST

	
def get_session(session_name: str):
	return db.query(Session).filter_by(session_name=session_name).first()


def update_session(data: schemes.UpdateSession):
	session = get_session(data.session_name)
	if session is NOT_EXIST:
		return NO_SUCH_SESSION
	
	# TODO iterate
	if data.api_id is not None:
		session.api_id = data.api_id
	if data.api_hash is not None:
		session.api_hash = data.api_hash
	if data.bot_token is not None:
		session.bot_token = data.bot_token
	if data.default_user is not None:
		session.default_user = data.default_user

	db.commit()
	return OK


def remove_session(data: schemes.RemoveSession):
	session = get_session(data.session_name)
	if session is NOT_EXIST:
		return NO_SUCH_SESSION
	
	db.delete(session)
	db.commit()
	return OK


if __name__ == "__main__":
	create_session(schemes.CreateSession(session_name="Test", api_id=324, api_hash="324324", bot_token="342324"))
	print_db_row(get_session("Test"))

	if update_session(schemes.UpdateSession(session_name="Test", api_id=123)) is OK:
		print_db_row(get_session("Test"))

	if remove_session(schemes.RemoveSession(session_name="Test", api_id=123)) is OK:
		print_db_row(get_session("Test"))