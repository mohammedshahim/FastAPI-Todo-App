from typing import Annotated
from passlib.context import CryptContext
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, Path, APIRouter, Request
from ..models import Users
from ..database import SessionLocal
from starlette import status
from .auth import get_current_user
from .todos import redirect_to_login
from fastapi.templating import Jinja2Templates

SECRET_KEY = 'randomtext'
ALGORITHM = 'HS256'

router = APIRouter(
    prefix="/user",
    tags=["user"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
templates = Jinja2Templates(directory="TodoApp/templates")

class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)

# Pages
@router.get("/change-password-page")
async def render_change_password_page(request: Request):
    user = await get_current_user(request.cookies.get('access_token'))
    if user is None:
        return redirect_to_login()
    return templates.TemplateResponse("change-password.html", {"request": request, 'user': user})

# Endpoints
@router.get('/', status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")

    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    return user_model

@router.put('/password', status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: db_dependency, user_verification: UserVerification):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")

    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Error on password change")

    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()


@router.put('/phonenumber/{phone_number}', status_code=status.HTTP_204_NO_CONTENT)
async def change_phone_number(user: user_dependency, db: db_dependency, phone_number: str):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")

    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    user_model.phone_number = phone_number
    db.add(user_model)
    db.commit()