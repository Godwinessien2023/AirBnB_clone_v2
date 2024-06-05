#!/usr/bin/python3
"""
Define new engine BD Storage
"""
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from models.base_model import Base, BaseModel
from models.state import State
from models.city import City
from models.review import Review
from models.amenity import Amenity
from models.place import Place
from models.user import User


class DBStorage:
    """
    define class for DB storage
    """
    __engine = None
    __sessions = None

    def __init__(self):
        """
        define public instance method
        and engine must be linked to the DB
        """
        username = getenv('HBNB_MYSQL_USER')
        password = getenv()
        host = getenv()
        db_name = getenv()

        db_url = "mysql+mysqldb://{}:{}@{}/{}".format(username,
                                                      password, host, db_name)

        self.__engine = create_engine(db_url, pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        define all method
        """
        objs_list = []
        if cls:
            if isinstance(cls, str):
                try:
                    cls = globals()[cls]
                except KeyError:
                    pass
            if issubclass(cls, Base):
                objs_list = self.__session.query(cls).all()
        else:
            for subclass in Base.__subclasses__():
                objs_list.extend(self.__session.query(subclass).all())
        obj_dict = {}
        for obj in objs_list:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            try:
                del obj._sa_instance_state
                obj_dict[key] = obj
            except Exception:
                pass
        return obj_dict

    def new(self, obj):
        """
        add object  to the current database session
        """
        self.__session.add(obj)

    def save(self):
        """
        commits all changes of the current database.
        """
        self.__session.commit()

    def delete(self):
        """
        delete from the session of the current database if not None
        """
        self.__session.delete(obj)

    def reload(self):
        """
        define reload method to ensure that the database
        schema is syncronized with the current state of the
        sqlalchemy models and also provide fresh database session
        """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        session = scoped_session(sec)
        self.__session = session()

    def close(self):
        """
        define close method to call reload method
        """
        self.__session.close()
