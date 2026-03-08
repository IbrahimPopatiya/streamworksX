from pydantic import BaseModel,HttpUrl
from typing import List,Dict

class VideoURL(BaseModel):
    url: HttpUrl
    username: str

class GetVideo(BaseModel):
    video_uuid : str   