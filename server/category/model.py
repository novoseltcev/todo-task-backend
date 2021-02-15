from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from server.initialize_db import Base, engine, DB_config


category_name_len = DB_config['category_name_len']


class Category(Base):
    __default = 1
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String(category_name_len), unique=True)
    tasks = relationship('Task', backref=__tablename__, order_by='Task.id')

    def change_name(self, new_name):
        self.name = new_name


Base.metadata.create_all(bind=engine)
