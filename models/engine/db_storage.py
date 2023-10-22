#!/usr/bin/python3

"""database storage class"""

from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError, IntegrityError
import MySQLdb
from models.base_model import Base
from os import getenv
from models.amenity import Amenity
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.review import Review


class DBStorage:
    """class DBStorage
    args:
    __engine: None
    __session: None
    """
    __engine = None
    __session = None

    def __init__(self):
        """linking to mysql database"""
        user = getenv("HBNB_MYSQL_USER")
        password = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        database = getenv("HBNB_MYSQL_DB")
        env = getenv("HBNB_ENV")
        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'
            .format(user, password, host, database),
            pool_pre_ping=True
        )

        # Base.metadata.create_all(self.__engine)

        if env == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current database session"""
        classes = {
            'State': State, 'City': City, 'User': User,
            'Place': Place, 'Review': Review, 'Amenity': Amenity,
        }
        objects = {}
        if (cls is None):
            for items in classes:
                query = self.__session.query(classes[items])
                for obj in query.all():
                    obj_key = '{}.{}'.format(obj.__class__.__name__, obj.id)
                    objects[obj_key] = obj
        else:
            if cls in classes:
                query = self.__session.query(classes[cls])
                for obj in query.all():
                    obj_key = '{}.{}'.format(obj.__class__.__name__, obj.id)
                    objects[obj_key] = obj

        return objects

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """creates all tables in the database"""
        # self.close()
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False
        )
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """ close session """
        self.__session.close()
