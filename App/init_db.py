from app.database import Base, engine
from app.models import Transaction

"""
Initializes the database by creating all tables defined in the models.
Should be run once during setup.
"""

Base.metadata.create_all(bind=engine)