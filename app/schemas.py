from pydantic import BaseModel, Field
from typing import Optional

class AccountCreate(BaseModel):
    balance: float = Field(..., gt=0, description="Initial balance must be greater than 0")
    description: Optional[str] = Field(None, description="Optional description for the account")

class AccountResponse(BaseModel):
    id: int
    balance: float
    description: Optional[str] = None  # Make description optional in response

    class Config:
        orm_mode = True

class Transfer(BaseModel):
    from_account: int = Field(..., gt=0, description="ID of the sending account (must be greater than 0)")
    to_account: int = Field(..., gt=0, description="ID of the receiving account (must be greater than 0)")
    amount: float = Field(..., gt=0, description="Transfer amount must be greater than 0")
