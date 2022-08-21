
import glob
from sqlalchemy import create_engine, MetaData, Table, and_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
import os
from dotenv import load_dotenv
import sys
from sqlalchemy import create_engine
from utils.models import Iscritto
from sqlalchemy_utils import database_exists, create_database
import base64
import uuid
from alembic.command import upgrade
from alembic.config import Config

load_dotenv()


class dbConnector():
    def __init__(self, database, table):
        self.table = table
        self.db_connect(database)

    def db_connect(self, database):
        engine = create_engine(self.create_postgres_url(
            database), poolclass=NullPool)
        metadata = MetaData(schema='ball')
        self.model = Table(self.table, metadata, autoload=True,
                           autoload_with=engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def search_for_fiscal_code(self, codice_fiscale):
        return self.session.query(self.model).filter(self.model.c.codice_fiscale == codice_fiscale).first()

    def insert_parameters_to_iscritto(self, iscritto: Iscritto):
        obj = self.model.insert().values(
            id = base64.urlsafe_b64encode(uuid.uuid4().bytes)[:22].decode("utf-8"),
            nome= iscritto.nome,
            cognome= iscritto.cognome,
            data_nascita= iscritto.data_nascita,
            comune_id= iscritto.luogo_di_nascita,
            provincia= iscritto.provincia,
            codice_fiscale= iscritto.codice_fiscale,
            data_iscrizione= iscritto.data_iscrizione
        )
        self.session.execute(obj)
        self.session.commit()

    @classmethod
    def create_postgres_url(cls, database):
        url = 'postgresql+psycopg2://'
        url += os.getenv('POSTGRES_USER') + ':'
        url += os.getenv('POSTGRES_PASSWORD') + '@'
        url += os.getenv('POSTGRES_URL') + '/'
        url += database
        return url

    @classmethod
    def create_database_if_not_exists(cls,database):
        engine = create_engine(cls.create_postgres_url(database))
        if not database_exists(engine.url):
            create_database(engine.url)

    
    @classmethod
    def run_migration(cls,database: str):
        config = Config(glob.glob('**/alembic.ini', recursive=True)[0])
        config.set_main_option("sqlalchemy.url", cls.create_postgres_url(database))
        upgrade(config, "head")
