#NOTE: Drop the address & user_account tables before running this script
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer, Text, Time
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import select
# GYM -> ClasesOffered
#DB Connection:
engine = create_engine("postgresql+psycopg2://postgres:########@localhost/Phase3")

#Define Classes/Tables
class Base(DeclarativeBase):
    pass

class Gym(Base):
    __tablename__ = "gym"
    
    gymId: Mapped[int] = mapped_column(Integer, primary_key=True)
    capacity: Mapped[int] = mapped_column(Integer)
    buildingNo: Mapped[str] = mapped_column(String(10))
    streetName: Mapped[str] = mapped_column(String(100))
    state: Mapped[str] = mapped_column(String(50))
    zipCode: Mapped[str] = mapped_column(String(10))
    # Leaving out manager becase I am not implementing employee
    classesOffered: Mapped[List["ClassesOffered"]] = relationship(
        back_populates="gym", cascade="all, delete-orphan"
    )
    
    def __repr__(self) -> str: #represents the object as a string 
        return f"Gym(id={self.gymId!r}, capacity={self.capacity!r}, buildingNo={self.buildingNo!r}, streetName={self.streetName!r}, state={self.state!r}, zipCode={self.zipCode!r})"

class ClassesOffered(Base):
    __tablename__ = "classesOffered"
    
    classId: Mapped[int] = mapped_column(Integer, primary_key=True)
    cName: Mapped[str] = mapped_column(String(100))
    # Ask about text and time and if I need gymID and teacher
    Description: Mapped[str] = mapped_column(Text)
    StartTime: Mapped[str] = mapped_column(Time)
    EndTime: Mapped[str] = mapped_column(Time)
    gym: Mapped["Gym"] = relationship(back_populates="classesOffered")
    
    def __repr__(self) -> str:
        return f"ClassesOffered(classId={self.classId!r}, cName={self.cName!r}, Description={self.Description!r}, StartTime={self.StartTime!r}, EndTime={self.EndTime!r})"

#Create Tables
Base.metadata.create_all(engine)