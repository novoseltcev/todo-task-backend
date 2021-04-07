import os

from server import engine, Base, s3_bucket


Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

objs = s3_bucket.objects.all()
for obj in objs:
    obj.delete()

cwd = os.getcwd()
inserts_path = os.path.join(cwd, 'server', 'dev', 'inserts.sql')
with open(inserts_path) as inserts:
    for insert in inserts:
        engine.execute(insert)
