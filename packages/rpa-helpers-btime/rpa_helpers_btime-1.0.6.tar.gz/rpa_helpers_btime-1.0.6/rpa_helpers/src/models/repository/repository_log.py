from datetime import datetime
from rpa_helpers.src.models.configs.connection import DBConnectionHandler
from rpa_helpers.src.models.entities.log import Logs
from sqlalchemy import text


class LogRepository:
    def __init__(self) -> None:
        self.create_table()
        self.date = datetime.now()

    def create_table(self):
        with DBConnectionHandler() as db:
            query = text(
                """
                CREATE TABLE IF NOT EXISTS logs
                (id INTEGER PRIMARY KEY, message TEXT, status TEXT, description TEXT, start_date DATETIME, end_date DATETIME, rpa_id INTEGER)
                """
            )

            db.session.execute(query)
            db.session.commit()

    def insert(self, message, status, description, start_date, end_date, rpa_id):
        start_date = datetime.strptime(start_date, "%d/%m/%Y %H:%M:%S")
        end_date = datetime.strptime(end_date, "%d/%m/%Y %H:%M:%S")

        with DBConnectionHandler() as db:
            data_insert = Logs(
                message=message,
                status=status,
                description=description,
                start_date=start_date,
                end_date=end_date,
                rpa_id=rpa_id,
            )

            db.session.add(data_insert)
            db.session.commit()
