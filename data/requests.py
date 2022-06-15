import sqlalchemy
from .db_session import SqlAlchemyBase


class Request(SqlAlchemyBase):
    __tablename__ = 'requests'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, index=True)
    clicks = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    money = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    site = sqlalchemy.Column(sqlalchemy.Float, default=0.03)
    manager = sqlalchemy.Column(sqlalchemy.Float, default=0.1)
    traffic = sqlalchemy.Column(sqlalchemy.Float, default=0.62)

    def __repr__(self):
        return ' '.join([str(self.clicks),
                         str(self.money),
                         str(self.site),
                         str(self.manager),
                         str(self.traffic)])
