# library imports
from fastapi import APIRouter, HTTPException, status

# module imports
from ..schemas import PasswordReset, PasswordResetRequest, db
from ..send_mail import password_reset
from ..oauth2 import create_access_token, get_current_user
from ..utils import get_password_hash

router = APIRouter(
    prefix="/password",
    tags=["Password Reset"]
)


@router.post("/request/", response_description="Password reset request")
async def reset_request(user_email: PasswordResetRequest):
    user = await db["users"].find_one({"email": user_email.email})

    print(user)

    if user is not None:
        token = create_access_token({"id": user["_id"]})

        reset_link = f"http://localhost:8000/reset?token={token}"

        print("Hello")

        await password_reset("Password Reset", user["email"],
            {
                "title": "Password Reset",
                "name": user["name"],
                "reset_link": reset_link
            }
        )
        return {"msg": "Email has been sent with instructions to reset your password."}

    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Your details not found, invalid email address"
        )


@router.put("/reset/", response_description="Password reset")
async def reset(token: str, new_password: PasswordReset):

    request_data = {k: v for k, v in new_password.dict().items()
                    if v is not None}

    # get the hashed version of the password
    request_data["password"] = get_password_hash(request_data["password"])

    if len(request_data) >= 1:
        # use token to get the current user
        user = await get_current_user(token)

        # Update the user's password in the database
        update_result = await db["users"].update_one(
            {"_id": user["_id"]},
            {"$set": {"password": get_password_hash(new_password.password)}}
        )

        if update_result.modified_count == 1:
            # Return the updated user information
            updated_user = await db["users"].find_one({"_id": user["_id"]})
            return {"msg": "Password has been reset successfully", "user": updated_user}

        # If update failed, return the original user
        existing_user = await db["users"].find_one({"_id": user["_id"]})
        if existing_user:
            return {"msg": "Password unchanged", "user": existing_user}


    # Raise error if the user can not be found in the database
    raise HTTPException(status_code=404, detail=f"User not found")