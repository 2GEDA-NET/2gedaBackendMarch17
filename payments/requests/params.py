from pydantic import BaseModel, EmailStr, validator
from typing import Optional


class IntializeTransaction(BaseModel):
    email: EmailStr
    amount: int
    callback_url: Optional[str] = None

    @validator("amount")
    def amount_multiplier(cls, value):
        return value * 100


class PromotionPlanMetaData(BaseModel):
    post: int
    plan:int
    description: Optional[str] = None
    user: int
    type: Optional[str] = "promote_post"


class PromotionPlanIntializeTransaction(IntializeTransaction):

    metadata: Optional[PromotionPlanMetaData]
