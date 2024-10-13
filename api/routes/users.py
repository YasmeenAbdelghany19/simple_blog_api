from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
import secrets
import email
from email.policy import HTTP


from api import oauth2
from ..schemas import User, db, UserResponse
from ..utils import get_password_hash
from ..send_mail import send_register_email

router = APIRouter(
    # prefix="/user_route",
    tags=["User Route"],
    responses={404: {"description": "Not found"}},
)

@router.post("/registration", response_description="Add new user", response_model=UserResponse)
async def create_user(user: User):
    user = jsonable_encoder(user)
    
    username_found = await db["users"].find_one({"name": user["name"]})
    email_found = await db["users"].find_one({"email": user["email"]})
    
    if username_found:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists")
    if email_found:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")
    
    user["password"] = get_password_hash(user["password"])
    user["api_key"] = secrets.token_hex(32)
    
    new_user = await db["users"].insert_one(user)
    created_user = await db["users"].find_one({"_id": new_user.inserted_id})
    
    # send email
    await send_register_email("Registration successful", user["email"],
        {
            "title": "Registration successful",
            "name": user["name"]
        }
    )
    
    return created_user

@router.post("/details", response_description="Get user details", response_model=UserResponse)
async def details(current_user=Depends(oauth2.get_current_user)):
    user = await db["users"].find_one({"_id": current_user["_id"]})
    return user