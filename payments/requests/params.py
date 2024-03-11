from pydantic import BaseModel, EmailStr
from typing import Optional


class IntializeTransaction(BaseModel):
    email: EmailStr
    amount: int





class PromotionPlanMetaData(BaseModel):
    post_id: int


class PromotionPlanIntializeTransaction(IntializeTransaction):

    metadata: Optional[PromotionPlanMetaData]






