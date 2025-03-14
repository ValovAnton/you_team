from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr

from database import SessionLocal, engine
import models

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    confirm_password: str


@app.post("/register")
def register_user(user: UserCreate):
    """Регистрирует пользователя, если емейл не занят, если пароли совпадают, ну и если пароль достаточно длинный"""
    db = SessionLocal()

    if len(user.password) < 6:
        """проверяем длину пароля"""
        raise HTTPException(status_code=400, detail="Password too short")


    if user.password != user.confirm_password:
        """проверяем совпадение паролей"""
        raise HTTPException(status_code=400, detail="Passwords do not match")


    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        """проверяем занятость емейла"""
        raise HTTPException(status_code=400, detail="Email is already registered")

    password = hash(user.password) # как будто пароль зашифрован

    new_user = models.User(email=user.email, password=password)
    try:
        db.add(new_user)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error. Error: {e}")
    finally:
        db.close()

    return {"status_code": 201, "details": "OK. User successfully created"}
