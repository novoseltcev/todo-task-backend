from ._serviceABC import FileService
from .schema import FileSchema
from .response import FileResponse
from .model import File
from ._repositoryABC import Files


class FileLogic(FileService):
    @classmethod
    def get(cls, schema: FileSchema) -> FileResponse:
        file = Files.load(schema.id)
        assert file.id_user == schema.id_user
        return FileResponse.dump(file)

    @classmethod
    def get_all(cls, schema: FileSchema) -> FileResponse:
        files = Files.load_by_task(schema.id_task)
        if len(files) > 0:
            assert files[0].id_user == schema.id_user
        return FileResponse.dump(files, many=True)

    @classmethod
    def pin(cls, schema: FileSchema) -> FileResponse:
        file = File(id_user=schema.id_user, name=schema.name, path=schema.path, id_task=schema.id_task)
        Files.save(file)
        return FileResponse.success()
        # tmp_path = os.path.join(os.getcwd(), 'server', 'tmp', path)
        # with open(tmp_path, 'wb') as fp:
        #     fp.write(data)
        # return id

    @classmethod
    def unpin(cls, schema: FileSchema) -> FileResponse:
        file = Files.load(schema.id)
        assert file.id_user == schema.id_user
        Files.delete(schema.id)
        return FileResponse.success()

# def s3_download(name, path):
#     s3_file = s3_bucket.Object(key=path)
#     tmp_path = os.path.join(os.getcwd(), 'server', 'tmp', path)
#     with open(tmp_path, 'wb') as data:
#         s3_file.download_fileobj(data)
#
#     result = send_file(tmp_path, attachment_filename=name, as_attachment=True)
#
#     # os.remove(tmp_path)  # TODO
#     return result


# def generate_path(name):
#     path = str(uuid4()) + os.path.splitext(name)[-1]
#     return path


# def check_uploading(id_user, id, path, uuid):
#     result = AsyncResult(uuid)
#     tmp_path = os.path.join(os.getcwd(), 'server', 'tmp', path)
#     if result.failed():
#         FileRepository.delete(id_user, id)
#
#     if result.successful() or result.failed():
#         os.remove(tmp_path)
#
#     return result.status


# @listens_for(File, 'before_delete')
# def clear_s3_bucket(mapper, connection, target):
#     s3_file = s3_bucket.Object(key=target.path)
#     s3_file.delete()

