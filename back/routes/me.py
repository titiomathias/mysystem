from fastapi import APIRouter

router = APIRouter()

# Get user info
@router.get("/")
async def get_me():
    return {"user": "me"}


# Update user info
@router.put("/profile")
async def update_me(user: dict):
    return {"updated_user": user}


# Delete user account
@router.delete("/")
async def delete_me():
    return {"message": "User account deleted"}


# Change user password
@router.post("/change-password")
async def change_password(passwords: dict):
    return {"message": "Password changed successfully"}

