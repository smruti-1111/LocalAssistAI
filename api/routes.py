from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.db import SessionLocal
from services.ticket_service import create_ticket

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/tickets")
def create_new_ticket(ticket: dict, db: Session = Depends(get_db)):
    return create_ticket(db, ticket["user_query"])
