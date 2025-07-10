from sqlalchemy import Column, Integer, String, Float, Date, Enum
from app.database import Base
import enum

class CategoryEnum(enum.Enum):
    FOOD = "Food"
    TRANSPORT = "Transport"
    FUN = "Fun"
    UTILITIES = "Utilities"
    MISC = "Misc"

class Transaction(Base): 
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(Enum(CategoryEnum), nullable=False)
    date = Column(Date, nullable=False)

    def __repr__(self):
        return f"<Transaction(id={self.id}, name='{self.name}', amount={self.amount}, category='{self.category}', date={self.date})>"
    
class Income(Base):
    __tablename__ = "income"

    id =  Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    date = Column(Date, nullable=False)

    def __repr__(self):
        return f"<Income(id={self.id}, amount={self.amount}, date={self.date})>"