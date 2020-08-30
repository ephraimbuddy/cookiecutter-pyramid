from typing import Optional

from passlib.hash import bcrypt

from pyramid.security import ALL_PERMISSIONS, Allow, Everyone, Authenticated

from sqlalchemy import (
    Column,
    Index,
    Integer,
    ForeignKey,
    Table,
    Enum
)
from sqlalchemy.types import String, UnicodeText
from sqlalchemy.orm import relationship

from {{cookiecutter.app_name}}.models.meta import Base

user_group = Table('user_group', Base.metadata,
                   Column('user_id', Integer, ForeignKey("user.id", onupdate='CASCADE', ondelete='CASCADE')),
                   Column('group_id', Integer, ForeignKey("group.id", onupdate='CASCADE', ondelete='CASCADE')))

# need to create Unique index on (user_id,group_id)
Index('user_group_index', user_group.c.user_id, user_group.c.group_id)


class Group(Base):
    """
    Authentication group
    """
    __tablename__ = 'group'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    description = Column(String(255), default='')
    permission_name = Column(String(255))
    users = relationship('User', secondary=user_group,
                         back_populates='groups')

    def __repr__(self):
        return u'%s' % self.name


class User(Base):
    """ User Entity class"""
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    groups = relationship("Group", secondary=user_group, back_populates="users")
    username = Column(String(100), unique=True, nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    email = Column(String(100), unique=True, nullable=False)
    password = Column(UnicodeText, nullable=False)

    def __init__(self,
                 username: str,
                 email: str,
                 password: str,
                 first_name: Optional[str] = None,
                 last_name: Optional[str] = None,
                 ):
        self.username = username
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.set_password(password)

    @property
    def __acl__(self):
        """Object level authentication"""
        return [
            (Allow, self.id, 'edit'),
        ]

    def verify_password(self, password):
        """Veify a given password. Encrypt it if the password is plaintext"""
        # is it cleartext?
        if password == self.password:
            self.set_password(password)

        return bcrypt.verify(password, self.password)

    def set_password(self, password):
        password_hash = bcrypt.hash(password)
        self.password = password_hash

    @classmethod
    def by_id(cls, dbsession, user_id):
        user = dbsession.query(cls).get(user_id)
        return user

    @classmethod
    def by_email(cls, dbsession, email):
        user = dbsession.query(User).filter_by(email=email).first()
        return user

    @classmethod
    def by_username(cls, dbsession, username):
        user = dbsession.query(User).filter_by(username=username).first()
        return user


class UserFactory(object):
    __acl__ = [
        (Allow, 'g:admin', ALL_PERMISSIONS),
    ]

    def __init__(self, request):
        self.request = request

    def __getitem__(self, userid):
        user = User.by_id(self.request.dbsession, userid)
        user.__parent__ = self
        user.__name__ = userid
        return user

class RootFactory(Base):
    """ Defines the ACLs"""
    __tablename__ = 'root'
    id = Column(Integer, primary_key=True)

    def __init__(self, request):
        self.request = request
        if self.request.matchdict:
            self.__dict__.update(self.request.matchdict)

    @property
    def __acl__(self):
        return [
            (Allow, Everyone, 'view'),
            (Allow, Authenticated, 'post'),
            (Allow, 'g:editors', 'edit'),
            (Allow, 'g:admin', ALL_PERMISSIONS)
        ]

