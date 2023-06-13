from app.utils import AppModel
from . import router
from ..service import Service, get_service
from fastapi import Depends, Response
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data

class UpdateAccountRequest(AppModel):
    phone: str
    name: str
    city: str

@router.patch("/users/me", status_code = 200, response_model = UpdateAccountRequest)
def update_account(input: UpdateAccountRequest, 
                   jwt_data: JWTData = Depends(parse_jwt_user_data), 
                   svc: Service = Depends(get_service)
) -> dict[str, str]:
        svc.repository.update_account(jwt_data.user_id, input.dict())
        return Response(status_code = 200)