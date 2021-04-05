import os

from server import engine, Base, s3_bucket


cwd = os.getcwd()

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

objs = s3_bucket.objects.all()
for obj in objs:
    obj.delete()

with open(os.path.join(cwd, 'server', 'dev', 'inserts.sql')) as inserts:
    for insert in inserts:
        engine.execute(insert)
