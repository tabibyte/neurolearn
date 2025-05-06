from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class LearningResource(Base):
    """Learning resources that can be adapted for neurodivergent learners."""
    __tablename__ = "learning_resources"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    resource_type = Column(String(50), nullable=False) 
    difficulty_level = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_sample = Column(Boolean, default=False)
    
    has_visual_aids = Column(Boolean, default=False)
    has_audio = Column(Boolean, default=False)
    has_simplified_text = Column(Boolean, default=False)
    
    def __repr__(self):
        return f"<LearningResource {self.title}>"