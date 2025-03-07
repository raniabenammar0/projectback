from pydantic import BaseModel
from typing import Optional
from enum import Enum
import datetime

class PlatformEnum(str, Enum):
    GITLAB = "GITLAB"
    GITHUB = "GITHUB"
    BITBUCKET = "BITBUCKET"

class Project(BaseModel):
    userId: str
    projectName: str
    projectPlateformId: str
    gitUrl: str
    gitToken: str
    platform: PlatformEnum
    gptKey: str
    deactivated: bool
    createdAt: Optional[datetime.datetime] = datetime.datetime.now()
    updatedAt: Optional[datetime.datetime] = datetime.datetime.now()
    deletionDate: Optional[datetime.datetime] = None
