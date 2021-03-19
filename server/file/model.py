from sqlalchemy import Column, Integer, String, ForeignKey

from server import Base, config


class File(Base):
    __tablename__ = 'files'
    id = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey('users.id'), nullable=False)
    id_task = Column(Integer, ForeignKey('tasks.id'), nullable=False)
    name = Column(String(config.filename_len), nullable=False)
    path = Column(String(config.files_dir_len + config.filename_len), unique=True, nullable=False)
