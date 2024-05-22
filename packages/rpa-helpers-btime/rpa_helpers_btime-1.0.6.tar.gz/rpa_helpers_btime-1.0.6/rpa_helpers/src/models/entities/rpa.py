from sqlalchemy import Column, String, Integer
from rpa_helpers.src.models.configs.base import Base


class Rpa(Base):

    __tablename__ = "rpa"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

    def __repr__(self):
        return f"Rpa [NAME='(self.name)']"
