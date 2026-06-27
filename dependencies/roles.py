from fastapi import Depends , HTTPException ,status
from dependencies.auth import get_current_user
from constants.roles import UserRole

def required_role(required_role: UserRole):

    def role_checker(current_user=Depends(get_current_user)):
        if current_user.role!=required_role.value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN ,
                detail="you do not have permission"
            )
        return current_user
    
    return role_checker