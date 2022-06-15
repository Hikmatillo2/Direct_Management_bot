import sqlalchemy
from .db_session import SqlAlchemyBase


class BannedUser(SqlAlchemyBase):
    __tablename__ = 'bannedusers'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, index=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    def __repr__(self):
        return ' '.join([str(self.id), self.name + ' '])
