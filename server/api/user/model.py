from sqlalchemy import Column, Integer, String, Date, Enum, Boolean
from sqlalchemy.orm import relationship

from server import Base
from server.api.user.schema import Role


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)

    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    reg_date = Column(Date, nullable=False)
    role = Column(Enum(Role), default=Role.customer)
    confirmed_email = Column(Boolean, default=False, nullable=False)

    categories = relationship('Category', order_by='Category.id')
    tasks = relationship('Task', order_by='Task.id')
    files = relationship('File', order_by='File.id')
