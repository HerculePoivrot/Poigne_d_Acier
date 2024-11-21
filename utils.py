from sqlmodel import Session, select
from init_db import engine

def add_instance(instance_object:object):
    with Session(engine) as sessionsql:
        sessionsql.add(instance_object)
        sessionsql.commit()

def update_instance(instance_object:object, focus, new_value):
    with Session(engine) as sessionsql:
        statement = select(instance_object).where(instance_object.focus == new_value)
        results = sessionsql.exec(statement)
        my_object = results.one()
        print(f"{type(my_object)=} : {my_object}")

def del_instance(instance_object:object, id):
    with Session(engine) as sessionsql:
        statement = select(instance_object).where(instance_object.id == id)
        results = sessionsql.exec(statement)
        focus_object = results.one()    
        sessionsql.delete(focus_object)
        sessionsql.commit()

