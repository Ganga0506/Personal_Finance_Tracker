from app.database import Base, engine
from app import models  # This ensures your models are imported and registered with Base

def create_tables():
    Base.metadata.create_all(bind=engine)
    print("Tables created!")

if __name__ == "__main__":
    create_tables()
