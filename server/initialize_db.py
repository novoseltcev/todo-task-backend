import os

from server import engine, Base


cwd = os.getcwd()

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

with open(os.path.join(cwd, 'server', 'inserts.sql')) as inserts_file:
    for insert in inserts_file:
        engine.execute(insert)
