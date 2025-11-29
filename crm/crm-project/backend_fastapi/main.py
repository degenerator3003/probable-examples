from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, Session
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://crm_user:crm_password@db:5432/crm")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class CustomerDB(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=True)


def init_db():
    Base.metadata.create_all(bind=engine)


app = FastAPI(title="CRM API")

@app.on_event("startup")
def on_startup():
    init_db()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class CustomerCreate(BaseModel):
    name: str
    email: EmailStr | None = None


class CustomerOut(BaseModel):
    id: int
    name: str
    email: str | None

    class Config:
        orm_mode = True


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/customers", response_model=list[CustomerOut])
def list_customers(db: Session = Depends(get_db)):
    return db.query(CustomerDB).all()


@app.post("/customers", response_model=CustomerOut)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    # simple unique email check
    if customer.email:
        existing = db.query(CustomerDB).filter(CustomerDB.email == customer.email).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already exists")

    obj = CustomerDB(name=customer.name, email=customer.email)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

