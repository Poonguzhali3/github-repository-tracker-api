from sqlalchemy import Column, Integer, String, DateTime, func
from app.database import Base


class Repository(Base):
    __tablename__ = "repositories"

    id = Column(Integer, primary_key=True, index=True)
    owner = Column(String, nullable=False)
    repo_name = Column(String, nullable=False)
    stars = Column(Integer, nullable=False, default=0)
    language = Column(String, nullable=True)
    description = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
