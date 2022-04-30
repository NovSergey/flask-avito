from sqlalchemy import Table, Column, ForeignKey, Integer
import datetime
import sqlalchemy
from sqlalchemy import orm
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin


from .db_session import SqlAlchemyBase

# association_table = sqlalchemy.Table(
#     'association',
#     SqlAlchemyBase.metadata,
#     sqlalchemy.Column('goods', sqlalchemy.Integer,
#                       sqlalchemy.ForeignKey('goods.id')),
#     sqlalchemy.Column('category', sqlalchemy.Integer,
#                       sqlalchemy.ForeignKey('category.id'))
# )
#
# class Category(SqlAlchemyBase):
#     __tablename__ = 'category'
#     id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True,
#                            autoincrement=True)
#     name = sqlalchemy.Column(sqlalchemy.String, nullable=True)



association_table = Table('association', SqlAlchemyBase.metadata,
                          Column('goods', ForeignKey('goods.id')),
                          Column('category', ForeignKey('category.id'))
                          )

class Category(SqlAlchemyBase):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(sqlalchemy.String, nullable=True)
    def __repr__(self):
        return f"Category ({self.id}, {self.name})"

