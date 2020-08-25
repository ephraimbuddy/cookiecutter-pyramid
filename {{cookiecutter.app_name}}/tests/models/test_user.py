import unittest

import transaction
from {{cookiecutter.app_name}}.models.user import User, Group
from pyramid import testing


class BaseTest(unittest.TestCase):

    def setUp(self):
        from {{cookiecutter.app_name}}.models import get_tm_session
        self.config = testing.setUp(settings={
            'sqlalchemy.url': 'sqlite:///:memory:'
        })
        self.config.include('{{cookiecutter.app_name}}.models')
        self.config.include('{{cookiecutter.app_name}}.routes')

        session_factory = self.config.registry['dbsession_factory']
        self.session = get_tm_session(session_factory, transaction.manager)

        self.init_database()

    def init_database(self):
        from {{cookiecutter.app_name}}.models.meta import Base
        session_factory = self.config.registry['dbsession_factory']
        engine = session_factory.kw['bind']
        Base.metadata.create_all(engine)

    def tearDown(self):
        testing.tearDown()
        transaction.abort()

    def create_user(self, username, email, password, first_name=None, last_name=None):

        user = User(username=username, email=email, password=password,
                    first_name=first_name, last_name=last_name)
        self.session.add(user)
        self.session.flush()
        return user

    def create_group(self, name, description):
        group = Group(name=name, description=description)
        self.session.add(group)
        self.session.flush()
        return group


class TestUser(BaseTest):

    def test_password_is_hashed(self):
        user = self.create_user(username='foo',
                                email="foo@bar.com",
                                password='testpassword')
        self.assertNotEqual(user.password, 'testpassword')

    def test_correct_password(self):
        user = self.create_user(username='foo',
                                email="foo@bar.com",
                                password='testpassword')
        self.assertTrue(user.verify_password('testpassword'))

    def test_incorrect_password(self):
        user = self.create_user(username='foo',
                                email="foo@bar.com",
                                password='testpassword')
        self.assertFalse(user.verify_password('wrongpassword'))


    def test_by_id(self):
        user = self.create_user(username='foo',
                                email="foo@bar.com",
                                password='testpassword')
        user2 = User.by_id(self.session, 1)
        self.assertEqual(user, user2)

    def test_by_email(self):
        user = self.create_user(username='foo',
                                email="foo@bar.com",
                                password='testpassword')
        user2 = User.by_email(self.session, "foo@bar.com")
        self.assertEqual(user, user2)


    def test_user_in_group(self):
        user = self.create_user(username='foo',
                                email="foo@bar.com",
                                password='testpassword')
        group = self.create_group(name='admin', description='Admin')
        user.groups.append(group)
        assert group.name == user.groups[0].name
