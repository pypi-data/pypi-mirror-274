from flask import Flask
from logging import INFO, DEBUG

from flask_sqlalchemy.model import Model
from sqlalchemy import Engine, text, MetaData
from sqlalchemy.ext.declarative import declarative_base as _declarative_base
from sqlalchemy.orm import sessionmaker


class DBCareEngine:
    def __init__(self, db_engine: Engine, declarative_base: Model = None, flask_app: Flask = None):
        self.base = declarative_base or _declarative_base()
        self.engine = db_engine
        self.__flask_app = flask_app

    def __enter__(self):
        self.session = sessionmaker(bind=self.engine)()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
        return False

    def _log(self, message, level=INFO):
        if self.__flask_app:
            self.__flask_app.logger.log(level, message)

    def _find_models(self):
        models = list()

        def find_subclasses(cls):
            for subclass in cls.__subclasses__():
                find_subclasses(subclass)
                models.append(subclass)

        find_subclasses(self.base)
        return models

    def _find_tables(self):
        metadata = MetaData()
        metadata.reflect(bind=self.engine)
        return metadata.tables

    def treat_tables(self):
        all_models = self._find_models()
        all_tables = self._find_tables()

        for model in all_models:
            if not hasattr(model, "__tablename__"):
                self._log(f"Table {model.__name__} has no name. Might be abstract. Skipping...", DEBUG)
                continue
            elif model.__tablename__ not in all_tables:
                self._log(f"Table {model.__tablename__} not found in database. Skipping...", DEBUG)
                continue
            else:
                table = all_tables.get(model.__tablename__)
                existing_columns = table.columns.keys()
                model_columns = model.__table__.columns.keys()

                missing_columns = set(model_columns) - set(existing_columns)
                extra_columns = set(existing_columns) - set(model_columns)

                self._log(f"Missing columns for {model.__tablename__}: {missing_columns}", DEBUG)
                self._log(f"Extra columns for {model.__tablename__}: {extra_columns}", DEBUG)

                for column in missing_columns:
                    column = model.__table__.columns.get(column)
                    with self.engine.connect() as conn:
                        column_definition = f'{column.name} {column.type.compile(dialect=self.engine.dialect)}'
                        alter_table_sql = f'ALTER TABLE {model.__tablename__} ADD COLUMN {column_definition}'
                        conn.execute(text(alter_table_sql))

                        self._log(f"Column {column.name} added to {model.__tablename__}")

                for column in extra_columns:
                    with self.engine.connect() as conn:
                        conn.execute(text(
                            f"ALTER TABLE {model.__tablename__} DROP COLUMN {column}"
                        ))

                        self._log(f"Column {column} dropped from {model.__tablename__}")
