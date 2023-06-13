from app.utils import AppModel
from . import router
from ..service import Service, get_service
from fastapi import Depends, Response
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data

class GetShanyrakRequest(AppModel):
    _id: str

class GetShanyrakResponse(AppModel):
    _id: str
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str
    user_id: str

@router.get("/{id}", response_model=GetShanyrakResponse)
def get_shanyrak(
    shanyrak_id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service)
):
    shanyrak = svc.repository.get_shanyrak(jwt_data.user_id, shanyrak_id)
    if (shanyrak):
        return shanyrak
    else:
        return Response(status_code=401)