# app.py
from init_db import engine, SQLModel


echo = SQLModel.metadata.create_all(engine)
print(echo)