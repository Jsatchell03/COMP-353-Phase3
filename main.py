#NOTE: Drop the address & user_account tables before running this script
from typing import List
from typing import Optional
import datetime
from sqlalchemy import ForeignKey
from sqlalchemy import String, Integer, Text, Time, Date, Float
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import select
# GYM -> ClasesOffered
#DB Connection:
engine = create_engine("postgresql+psycopg2://postgres:#ManILoveSports2003@localhost/Phase3")



class Base(DeclarativeBase):
    pass

# Gym class created by Chidera and Jaedon

class Gym(Base):
    __tablename__ = "gym"
    gymId: Mapped[str] = mapped_column(String, primary_key=True)
    capacity: Mapped[int] = mapped_column(Integer)
    buildingNo: Mapped[str] = mapped_column(String(10))
    streetName: Mapped[str] = mapped_column(String(100))
    state: Mapped[str] = mapped_column(String(50))
    zipCode: Mapped[str] = mapped_column(String(10))
    # Leaving out manager because it is 1 - 1
    classesOffered: Mapped[List["ClassesOffered"]] = relationship(back_populates="gym", cascade="all, delete-orphan")
    members: Mapped[List["IsMemberOf"]] = relationship(back_populates="gym", cascade="all, delete-orphan")
    employees: Mapped[List["Employee"]] = relationship(back_populates="gym", cascade="all, delete-orphan")
    def __repr__(self) -> str: #represents the object as a string 
        return f"Gym(id={self.gymId!r}, capacity={self.capacity!r}, buildingNo={self.buildingNo!r}, streetName={self.streetName!r}, state={self.state!r}, zipCode={self.zipCode!r})"

# Member and IsMemberOf classes created by Nick

class Member(Base): 
    __tablename__ = "member" 
    memberId: Mapped[str] = mapped_column(String, primary_key=True) 
    mFirstName: Mapped[str] = mapped_column(String(40)) 
    mLastName: Mapped[str] = mapped_column(String(40)) 
    mBirthday: Mapped[Date] = mapped_column(Date) 
    mPhone: Mapped[str] = mapped_column(String(15)) 
    mEmail: Mapped[str] = mapped_column(String(40)) 
    guests: Mapped[List["Guest"]] = relationship(back_populates="member", cascade="all, delete-orphan")
    def __repr__(self) -> str: 
        return (f"Member(memberid={self.memberId!r}, mFirstName={self.mFirstName!r}, " 
                f"mLastName={self.mLastName!r}, mBirthday={self.mBirthday!r}, " 
                f"mPhone={self.mPhone!r}, mEmail={self.mEmail!r})") 

class IsMemberOf(Base): 
    __tablename__ = "isMemberOf" 
    gym: Mapped["Gym"] = relationship(back_populates="members")
    gymId: Mapped[str] = mapped_column(String, ForeignKey("gym.gymId")) 
    memberId: Mapped[str] = mapped_column(String, ForeignKey("member.memberId"), primary_key=True) 
    gymId: Mapped[str] = mapped_column(String, ForeignKey("gym.gymId")) 
    membershipStart: Mapped[Date] = mapped_column(Date) 
    membershipEnds: Mapped[Date] = mapped_column(Date) 
    membershipPrice: Mapped[float] = mapped_column(Float)  
    def __repr__(self) -> str: 
        return (f"isMemberOf(gymid={self.gymid!r}, memberId={self.memberId!r}, membershipStart={self.membershipStart!r}, membershipEnds={self.membershipEnds!r}, membershipPrice={self.membershipPrice!r})") 

# Employee class created by David and Chidera

class Employee(Base): 
    __tablename__ = "employee" 
    eId: Mapped[str] = mapped_column(String, primary_key=True) 
    eFirstName: Mapped[str] = mapped_column(String(40)) 
    eLastName: Mapped[str] = mapped_column(String(40)) 
    startedWorking: Mapped[Date] = mapped_column(Date) 
    eEmail: Mapped[str] = mapped_column(String(40)) 
    ePhone: Mapped[str] = mapped_column(String(15))     
    gymId: Mapped[str] = mapped_column(String, ForeignKey("gym.gymId")) 
    gym: Mapped["Gym"] = relationship(back_populates="employees")
    classes: Mapped[List["ClassesOffered"]] = relationship(back_populates="employee", cascade="all, delete-orphan") 
    def __repr__(self) -> str: 
        return (f"Employee(eId={self.eId!r}, eFirstName={self.eFirstName!r}, " 
        f"eLastName={self.eLastName!r}, startedWorking={self.startedWorking!r}, " 
        f"eEmail={self.eEmail!r}, ePhone={self.ePhone!r})") 

# ClassesOffered class created by David and Jaedon

class ClassesOffered(Base):
    __tablename__ = "classesOffered"
    classId: Mapped[str] = mapped_column(String, primary_key=True)
    cName: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(Text)
    startTime: Mapped[str] = mapped_column(Time)
    endTime: Mapped[str] = mapped_column(Time)
    eId: Mapped[str] = mapped_column(String, ForeignKey("employee.eId")) 
    employee: Mapped["Employee"] = relationship(back_populates="classes")
    gymId: Mapped[str] = mapped_column(String, ForeignKey("gym.gymId")) 
    gym: Mapped["Gym"] = relationship(back_populates="classesOffered")
    def __repr__(self) -> str:
        return f"ClassesOffered(classId={self.classId!r}, cName={self.cName!r}, Description={self.Description!r}, StartTime={self.StartTime!r}, EndTime={self.EndTime!r})"

# Guest class created by Jaedon

class Guest(Base):
    __tablename__ = "guest"
    guestId: Mapped[str] = mapped_column(String, primary_key=True)
    gFirstName: Mapped[str] = mapped_column(String(40)) 
    gLastName: Mapped[str] = mapped_column(String(40)) 
    gEmail: Mapped[str] = mapped_column(String(40)) 
    vistDate: Mapped[Date] = mapped_column(Date) 
    memberId: Mapped[str] = mapped_column(String, ForeignKey("member.memberId")) 
    member: Mapped["Member"] = relationship(back_populates="guests")
    def __repr__(self) -> str: 
        return (f"Guest(memberid={self.memberId!r}, gFirstName={self.gFirstName!r}, " 
                f"gLastName={self.gLastName!r}, gEmail={self.gEmail!r})") 


#Create Tables
Base.metadata.create_all(engine)

# Add Data

with Session(engine) as session:
    # Object creation (data insertion) – Chidera 

    gym1 = Gym(gymId="1", buildingNo="1", streetName="MLK", state="IL", zipCode="60626", capacity=50,) 
    gym2 = Gym(gymId="2", buildingNo="3", streetName="El", state="IL", zipCode="60626", capacity=70,)
    session.add_all([gym1, gym2]) 
    session.commit()  

    employee_alice = Employee(eId="1", eFirstName="Alice", eLastName="Johnson", startedWorking=datetime.date(2013, 10, 28), eEmail="alice@example.com", ePhone="1234567890", gymId="1") 
    employee_bob = Employee(eId="2", eFirstName="Bob", eLastName="Smith", eEmail="bob@example.com", startedWorking=datetime.date(2021, 9, 3), ePhone="9876543210", gymId="1") 
    employee_charlie = Employee(eId="3", eFirstName="Charlie", eLastName="Brown",startedWorking=datetime.date(2020, 2, 15),  eEmail="charlie@example.com", ePhone="5551234567", gymId="2") 
    session.add_all([employee_alice, employee_bob, employee_charlie]) 
    session.commit() 

    # Object creation (data insertion) – Nick

    mary = Member(memberId="4", mFirstName="Mary", mLastName="Joseph", mBirthday=datetime.date(1985, 7, 20), mPhone="3194882832",mEmail="maryj@gmail.com")
    session.add_all([mary])
    session.commit()

    membership = IsMemberOf(memberId=mary.memberId, gymId="2", membershipStart=datetime.date(2024, 1, 1), membershipEnds=datetime.date(2024, 12, 31), membershipPrice=100.0,)
    session.add_all([membership])
    session.commit()

    # Object creation (data insertion) – David 

    employee_john_doe = Employee(eId="4", eFirstName="John", eLastName="Doe", startedWorking=datetime.date(2024, 1, 1), eEmail="john.doe@example.com", ePhone="123456789", gymId="1") 
    employee_Michael_Brown = Employee(eId="5", eFirstName="Michael", eLastName="Brown", startedWorking=datetime.date(2018, 3, 22), eEmail="michael.brown@example.com", ePhone="5553434817", gymId="2") 
    yoga_class = ClassesOffered(classId="1", gymId=employee_john_doe.gymId, cName="Yoga", description="Relaxing yoga class", startTime="09:00:00", endTime="10:00:00", eId=employee_john_doe.eId) 
    spin_class = ClassesOffered(classId="2", cName="Spin", description="High intensity spin class", startTime="09:00:00", endTime="10:00:00", eId=employee_Michael_Brown.eId, gymId=employee_Michael_Brown.gymId) 
    session.add_all([employee_john_doe, employee_Michael_Brown, yoga_class, spin_class]) 
    session.commit() 

    # Object creation (data insertion) – Jaedon
    guestLarry = Guest(guestId="1", gFirstName="Larry", gLastName="Fink", gEmail="lfink@gmail.com", vistDate=datetime.date(2024, 11, 12), memberId=mary.memberId,)
    guestSteve = Guest(guestId="2", gFirstName="Steven", gLastName="Segal", gEmail="ssegal@gmail.com", vistDate=datetime.date(2024, 11, 13), memberId=mary.memberId,)
    guestBob = Guest(guestId="3", gFirstName="Bob", gLastName="Marley", gEmail="bmarley@gmail.com", vistDate=datetime.date(2024, 11, 14), memberId=mary.memberId,)
    session.add_all([guestLarry, guestSteve, guestBob])
    session.commit()
    
# Guest Mary Joseph Has Brought Query- Jaedon

    stmt = (
        select(Guest)
        .join(Member, Guest.memberId == Member.memberId)
        .where(Member.memberId == "4")
        .where(Member.mFirstName == "Mary")
        .where(Member.mLastName == "Joseph")
    )

    maryGuests = session.scalars(stmt).all()
    print("\n## Mary Joseph's Guests ##") 
    for guest in maryGuests: 
        print(f"Guest Id: {guest.guestId}, First Name: {guest.gFirstName}, Last Name: {guest.gLastName}")

# Date that Mary's membership expires Query - Nick
    stmt = ( 
        select(IsMemberOf) 
        .join(Member, IsMemberOf.memberId == Member.memberId) 
        .where(Member.mFirstName == "Mary")
        .where(Member.mLastName == "Joseph") 
    ) 

    membership_details = session.scalars(stmt).one() 
    print(f"\nMary's Membership Expires: {membership_details.membershipEnds}") 

# Current Classes Offered Query - David
    stmt = ( 
        select( 
        ClassesOffered.classId, 
        ClassesOffered.cName, 
        ClassesOffered.description, 
        Employee.eId, 
        Employee.eFirstName, 
        Employee.eLastName 
        ) 
        .join(Employee, ClassesOffered.eId == Employee.eId) 
    ) 

    results = session.execute(stmt).all()
    print("\n## Current Classes Offered ##") 
    for row in results:
        print(f"Class ID: {row.classId}, Name: {row.cName}, "
              f"Description: {row.description}, Taught by: {row.eFirstName} {row.eLastName}")

# Employees at Gym on MLK Street Query - Chidera 
    stmt = ( 
        select(Employee) 
        .join(Gym, Gym.gymId == Employee.gymId) 
        .where(Gym.streetName == "MLK") 
    ) 

    mlk_employees = session.scalars(stmt).all() 
    print("\n## Employees at Gym on MLK Street ##") 

    for employee in mlk_employees: 
        print(f"First Name: {employee.eFirstName}, Last Name: {employee.eLastName}, Email: {employee.eEmail}") 
