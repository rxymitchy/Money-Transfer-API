from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.services import transfer_funds
from app.database import SessionLocal
from app.models import Account
from fastapi.responses import RedirectResponse


app = FastAPI()

class TransferFundsRequest(BaseModel):
    from_account_id: int
    to_account_id: int
    amount: float

class AccountCreateRequest(BaseModel):
    balance: float

@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Money Transfer API!",
        "available_routes": [
            "/accounts - Create and view accounts",
            "/transfer - Transfer funds between accounts"
        ]
    }

@app.get("/favicon.ico")
def favicon():
    return RedirectResponse(url="/static/favicon.ico")

@app.post("/transfer")
def transfer_funds_endpoint(request: TransferFundsRequest):
    db = SessionLocal()
    try:
        transfer_funds(db, request.from_account_id, request.to_account_id, request.amount)
        return {"message": "Transfer successful"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()

@app.post("/accounts")
def create_account(account: AccountCreateRequest):
    db = SessionLocal()
    db_account = Account(balance=account.balance)
    try:
        db.add(db_account)
        db.commit()
        db.refresh(db_account)
        return {"id": db_account.id, "balance": db_account.balance}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        db.close()
