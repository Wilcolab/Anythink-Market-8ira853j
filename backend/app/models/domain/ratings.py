from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.models.domain.profiles import Profile


class Rating(BaseModel):
    id_: int = Field(..., alias="id")
    value: int
    item_id: int  
    user: Profile
    comment: Optional[str] = ""
    created_at: datetime
    updated_at: datetime
    
    class Config:
        allow_population_by_field_name = True
