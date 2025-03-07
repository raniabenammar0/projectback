from pydantic import BaseModel,Field
from typing import Optional
from enum import Enum
import datetime

class Role(str, Enum):
    OWNER = "OWNER"
    MAINTAINER = "MAINTAINER"
    DEV = "DEV"

class Status(str, Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"

class UserModel(BaseModel):
    userId: str
    userName: str
    email: str

class ProjectModel(BaseModel):
    projectDataBaseId : str
    projectId: str
    projectName: str
    platform: str
    gitUrl: str

class TeamMember(BaseModel):
    project: ProjectModel
    user: UserModel
    userToken: str
    role: Role
    status: Status
    createdAt: Optional[datetime.datetime] = datetime.datetime.now()
    updatedAt: Optional[datetime.datetime] = datetime.datetime.now()
    deletedAt: Optional[datetime.datetime] = None
