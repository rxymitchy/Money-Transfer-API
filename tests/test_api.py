import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal, Base
from app.models import Account
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create a test database engine
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Initialize the database
Base.metadata.create_all(bind=engine)

client = TestClient(app)

# Fixture to set up the database before tests
@pytest.fixture(scope="module")
def setup_database():
    # Setup: Create test accounts
    db = TestingSessionLocal()
    account1 = Account(balance=100.0)
    account2 = Account(balance=50.0)
    db.add(account1)
    db.add(account2)
    db.commit()
    db.refresh(account1)
    db.refresh(account2)

    yield db  # Provide the test database to the test

    # Teardown: Clean up after tests
    db.query(Account).delete()
    db.commit()

def test_create_account(setup_database):
    response = client.post("/accounts", json={"balance": 100.0})
    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["balance"] == 100.0

def test_transfer_funds(setup_database):
    # Assuming you have valid account ids (1 and 2 created in the fixture)
    from_account_id = 1
    to_account_id = 2
    amount = 50.0
    
    response = client.post("/transfer", json={
        "from_account_id": from_account_id,
        "to_account_id": to_account_id,
        "amount": amount
    })
    
    assert response.status_code == 200
    assert response.json()["message"] == "Transfer successful"
