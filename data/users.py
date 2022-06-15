import datetime
import sqlalchemy
import random
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, index=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    start_session = sqlalchemy.Column(sqlalchemy.String,
                                      default=datetime.datetime.now().strftime('%m/%d/%Y'))
    acces_level = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    message_counter = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    code = sqlalchemy.Column(sqlalchemy.Integer, default=random.randint(1000000, 10000000))

    def __repr__(self):
        return ' '.join([str(self.id), self.name,
                         str(self.start_session),
                         str(self.message_counter),
                         str(self.code),
                         str(self.acces_level)])
