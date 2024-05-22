from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from src.models.configs.base import Base
from src.models.entities.rpa import Rpa


class Logs(Base):

    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    message = Column(String)
    status = Column(String)
    description = Column(String)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    rpa_id = Column(Integer, ForeignKey(Rpa.id))

    def __repr__(self):
        return f"Logs [MESSAGE='(self.message)', STATUS='(self.status)', DESCRIPTION='(self.description)', START_DATE='(self.start_date)', END_DATE='(self.end_date)', RPA_ID='(self.rpa_id)']"
