from sqlmodel import Session
from init_db import engine
def add_instance(instance_object:object):
    with Session(engine) as sessionsql:
        sessionsql.add(instance_object)
        sessionsql.commit()

    