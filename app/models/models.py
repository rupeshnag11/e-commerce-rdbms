from sqlalchemy import Integer, String, Column
from app.database.database import Base
class User_role(Base):
    __tablename__ = "users_role"

    user_id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)