from pydantic import BaseModel
from typing import Optional
from enum import Enum
import datetime


class Project(BaseModel):
    projectId: str
    projectName: str
    projectPlateformId: str | int

class Author(BaseModel):
    userName: str
    avatarUrl: str

class MergeRequest(BaseModel):
    mergeTitle: str
    plateformId: str | int
    state: str
    author: Author
    assignedTo: str
    changesNumber: int
    link: str
    sourceBranch: str
    project: Project
    createdAt: Optional[datetime.datetime] = datetime.datetime.now()
    updatedAt: Optional[datetime.datetime] = datetime.datetime.now()
    deletionDate: Optional[datetime.datetime] = None
