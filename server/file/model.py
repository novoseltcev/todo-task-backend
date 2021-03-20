from sqlalchemy import Column, Integer, String, ForeignKey

from server import Base
from server.config import Config


class File(Base):
    __tablename__ = 'files'
    id = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey('users.id'), nullable=False)
    id_task = Column(Integer, ForeignKey('tasks.id'), nullable=False)
    name = Column(String(Config.filename_len), nullable=False)
    path = Column(String(Config.files_dir_len + Config.filename_len), unique=True, nullable=False)
