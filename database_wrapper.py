from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    age = Column(Integer)
    sex = Column(Integer)
    city = Column(String)
    relationship_status = Column(String)

    def __repr__(self):
        return f"<User(id={self.id}, age={self.age}, sex={self.sex}, city={self.city}, " \
               f"relationship_status={self.relationship_status})>"


class DatabaseWrapper:
    def __init__(self, vk_api_wrapper):
        self.vk_api_wrapper = vk_api_wrapper

    def save_user(self, user):
        # Сохранение пользователя в базе данных

    def get_user(self, user_id):
        # Получение пользователя из базы данных

    def find_matching_users(self, user):
        matching_users = self.vk_api_wrapper.search_users(user.get_age(), user.get_sex(), user.get_city(), user.get_relationship_status())
        return matching_users
