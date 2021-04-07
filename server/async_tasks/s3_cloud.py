import os

from server import celery, s3_bucket


@celery.task(name='s3_cloud.upload')
def upload(path):
    s3_file = s3_bucket.Object(key=path)
    tmp_path = os.path.join(os.getcwd(), 'server', 'tmp', path)
    with open(tmp_path, 'rb') as fp:
        s3_file.upload_fileobj(fp)
