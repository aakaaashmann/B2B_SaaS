import httpx
from fastapi import Depends, HTTPException, Request, status
from clerk_backend_api.security import AuthenticateRequestOptions
from app.core.clerk import clerk
from app.core.config import settings
from typing import List

class AuthUser: #RBAC(role based access control) implementation
    def __init__(self,user_id:str,org_id:str,org_permissions:List):
        self.user_id = user_id #who is the user
        self.org_id = org_id #which organization the user belongs to
        self.org_permissions = org_permissions #what permissions the user has within the organization

    
    def  has_permission(self,permission:str) -> bool:
        return permission in self.org_permissions #check if the user has a specific permission
    

    @property
    def can_view(self) -> bool:
        return self.has_permission("org:tasks:view") #if the user has the "org:tasks:view" permission, they can view tasks
    
    @property
    def can_create(self) -> bool:
        return self.has_permission("org:tasks:create") #they can create tasks
    
    @property
    def can_delete(self) -> bool:
        return self.has_permission("org:tasks:delete") #they can delete tasks
    
    @property
    def can_edit(self) -> bool:
        return self.has_permission("org:tasks:edit") #they can edit tasks

#Clerk expects an httpx.Request.But FastAPI gives a Request so this function converts a FastAPI Request to an httpx.Request that Clerk can understand.
# It extracts the method, url, and headers from the FastAPI Request and creates a new httpx.Request with that information.
def convert_to_httpx_request(fastapi_request: Request) -> httpx.Request:
    return httpx.Request(
        method = fastapi_request.method,
        url = str(fastapi_request.url),
        headers = dict(fastapi_request.headers) #Without headers, authentication fails
    )

#This function is used as a dependency in FastAPI routes to get the current authenticated user.
#It uses the Clerk SDK to authenticate the incoming request and extract the user's information and permissions.
async def get_current_user(request: Request) -> AuthUser:
    httpx_request = convert_to_httpx_request(request)

    request_state = clerk.authenticate_request(
        httpx_request,
        AuthenticateRequestOptions(authorized_parties=[settings.FRONTEND_URL])
    ) #verifies JWT, checks signature, and ensures the token is valid and not expired. 
    #confirms request is from an authorized party (the frontend URL), extracts claims

    #if invalid JWT, missing claims, or unauthorized party, raise exceptions
    if not request_state.is_signed_in:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    #Extract user information and permissions from the claims in the JWT.
    claims = request_state.payload #The claims contain details about the user, their organization, and their permissions within that organization.
    user_id = claims.get("sub") #The "sub" claim typically contains the user's unique identifier. This is used to identify who the user is.
    org_id = claims.get("org_id") #The "org_id" claim indicates which organization the user belongs to. This is important for multi-tenant applications where users are associated with specific organizations.
    org_permissions = claims.get("org_permissions") or  claims.get("permissions") or [] #Role based access control (RBAC) implementation. 

#If the user is not authenticated or if there are any issues with the authentication.
# it raises an HTTPException with the appropriate status code and message.
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    if not org_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No organization selected"
        )
    #The function returns an instance of the AuthUser class.
    return AuthUser(user_id=user_id,org_id=org_id,org_permissions=org_permissions)

#Helper functions to enforce permissions on routes.
#These functions are used as dependencies in FastAPI routes to ensure that 
#the authenticated user has the necessary permissions to perform 
#certain actions (view, create, delete, edit).
def require_view(user: AuthUser = Depends(get_current_user)) -> AuthUser:
    if not user.can_view:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="View permission required"
        )
    return user

def require_create(user: AuthUser = Depends(get_current_user)) -> AuthUser:
    if not user.can_create:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Create permission required"
        )
    return user

def require_delete(user: AuthUser = Depends(get_current_user)) -> AuthUser:
    if not user.can_delete:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Delete permission required"
        )
    return user

def require_edit(user: AuthUser = Depends(get_current_user)) -> AuthUser:
    if not user.can_edit:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Edit permission required"
        )
    return user

