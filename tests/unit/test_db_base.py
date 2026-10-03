from sqlalchemy.orm import DeclarativeBase

from app.db.base import Base

def test_base_is_declaravtive_base():
    assert issubclass(Base, DeclarativeBase)
