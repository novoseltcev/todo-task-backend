from sqlalchemy import Column, Integer, String, Date, Enum
from sqlalchemy.orm import relationship

from server import Base
from server.user.schema import Role


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)

    login = Column(String(85), unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    reg_date = Column(Date, nullable=False)
    role = Column(Enum(Role))

    categories = relationship('Category', order_by='Category.id')
    tasks = relationship('Task', order_by='Task.id')
    files = relationship('File', order_by='File.id')
