from datetime import datetime
from rpa_helpers.src.models.configs.connection import DBConnectionHandler
from rpa_helpers.src.models.entities.rpa import Rpa
from sqlalchemy import text


class RpaRepository:
    def __init__(self) -> None:
        self.create_table()
        self.date = datetime.now()

    
    def create_table(self):
        with DBConnectionHandler() as db:
            query = text(
                """
                    CREATE TABLE IF NOT EXISTS rpa
                    (id INTEGER PRIMARY KEY, name TEXT)
                """
            )

            db.session.execute(query)
            db.session.commit()


    def insert(self, name):
        with DBConnectionHandler() as db:
            data_insert = Rpa(
                name = name
            )
            
            db.session.add(data_insert)
            db.session.commit()

    def update(self):
        ...