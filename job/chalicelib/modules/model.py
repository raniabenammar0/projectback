from enum import Enum
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class JobType(str, Enum):
    Review = "REVIEW"
    Verify = "VERIFY"

class UserModel(BaseModel):
    userId:str

class LicenseModel(BaseModel):
    licenseId: Optional[str] = None

class MergeRequestModel(BaseModel):
    mrDataBaseId: str
    mrPlatformId: Optional[int] = None
    title: Optional[str] = None
    author: str
    webUrl: str

class ReviewModel(BaseModel):
    commentPlatformId: int


class ProjectModel(BaseModel):
    projectDataBaseId: str
    projectPlatformId: str
    projectName: str

class JobModel(BaseModel):
    user: UserModel
    mergeRequest: MergeRequestModel
    review: ReviewModel
    project: ProjectModel
    status:Optional[str]= None
    jobType:JobType
    license: Optional[LicenseModel] = None
    createdAt: datetime = datetime.now()
    updatedAt: Optional[datetime] = datetime.now()
    deletionDate: Optional[datetime] = None
