from sqlalchemy import Column, Integer, String, Float, Date, Enum
from app.database import Base
import enum

class CategoryEnum(enum.Enum):
    """
    Enum representing available transaction categories.
    """
    FOOD = "Food"
    TRANSPORT = "Transport"
    FUN = "Fun"
    UTILITIES = "Utilities"
    MISC = "Misc"

class Transaction(Base): 
    """
    SQLAlchemy model for a financial transaction.

    Attributes:
        id (int): Primary key.
        name (str): Name or description of the transaction.
        amount (float): Amount of the transaction.
        category (CategoryEnum): Category of the transaction.
        date (date): Date of the transaction.
    """
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(Enum(CategoryEnum), nullable=False)
    date = Column(Date, nullable=False)
    
class Income(Base):
    """
    SQLAlchemy model for recording income.

    Attributes:
        id (int): Primary key.
        amount (float): Income amount.
        date (date): Date of income.
    """
    __tablename__ = "income"

    id =  Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    date = Column(Date, nullable=False)