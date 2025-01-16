from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models import Account

def create_account(db: Session, balance: float) -> Account:
    account = Account(balance=balance)
    db.add(account)
    db.commit()
    db.refresh(account)
    return account

def get_account(db: Session, account_id: int) -> Account:
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Account with id {account_id} not found"
        )
    return account

def transfer_funds(db: Session, from_account_id: int, to_account_id: int, amount: float):
    from_account = get_account(db, from_account_id)
    to_account = get_account(db, to_account_id)

    if from_account.balance < amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient funds"
        )

    from_account.balance -= amount
    to_account.balance += amount

    db.commit()
    db.refresh(from_account)
    db.refresh(to_account)
