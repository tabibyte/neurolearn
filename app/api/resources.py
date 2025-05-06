from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..models.database import get_db
from ..models.models import LearningResource
from pydantic import BaseModel

router = APIRouter()

class LearningResourceSchema(BaseModel):
    id: int = None
    title: str
    content: str
    resource_type: str
    difficulty_level: int = None
    is_sample: bool = False
    has_visual_aids: bool = False
    has_audio: bool = False
    has_simplified_text: bool = False
    
    class Config:
        orm_mode = True

@router.get("/resources/", response_model=List[LearningResourceSchema])
def get_resources(db: Session = Depends(get_db)):
    resources = db.query(LearningResource).all()
    return resources

@router.get("/resources/{resource_id}", response_model=LearningResourceSchema)
def get_resource(resource_id: int, db: Session = Depends(get_db)):
    resource = db.query(LearningResource).filter(LearningResource.id == resource_id).first()
    if resource is None:
        raise HTTPException(status_code=404, detail="Resource not found")
    return resource

@router.post("/resources/", response_model=LearningResourceSchema)
def create_resource(resource: LearningResourceSchema, db: Session = Depends(get_db)):
    db_resource = LearningResource(**resource.dict(exclude={"id"}))
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return db_resource