from sqlalchemy import Column, Integer, String, ForeignKey

from server import Base
from server.config import BaseConfig


class File(Base):
    __tablename__ = 'files'
    id = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey('users.id'), nullable=False)
    id_task = Column(Integer, ForeignKey('tasks.id'), nullable=False)
    name = Column(String(BaseConfig.filename_len), nullable=False)
    path = Column(String(BaseConfig.files_dir_len + BaseConfig.filename_len), unique=True, nullable=False)
