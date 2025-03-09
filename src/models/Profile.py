from typing import Optional

from pydantic import BaseModel

class Profile(BaseModel):
    name: str
    header: str
    picture: str
    pattern_bg: Optional[str] = None
    generated_poster: Optional[str] = None
