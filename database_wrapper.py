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
    def __init__(self):
        self.engine = create_engine('sqlite:///vkinder.db', echo=True)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def save_user(self, user):
        self.session.add(user)
        self.session.commit()

    def get_user(self, user_id):
        return self.session.query(User).filter_by(id=user_id).first()

    def find_matching_users(self, user):
        matching_users = self.session.query(User).\
            filter_by(age=user.get_age(), sex=user.get_sex(), city=user.get_city(),
                      relationship_status=user.get_relationship_status()).\
            filter(User.id != user.get_id()).all()
        return matching_users
