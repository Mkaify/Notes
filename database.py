from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class Note(Base):
    __tablename__ = "note"
    id = Column(Integer, primary_key=True)
    text = Column(String(1000), nullable=False)
    x = Column(Integer, nullable=False, default=0)
    y = Column(Integer, nullable=False, default=0)


engine = create_engine("sqlite:///notes.db")

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()