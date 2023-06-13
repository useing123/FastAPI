from app.utils import AppModel
from fastapi import Depends
from ..service import Service, get_service
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data

from . import router

class CreateShanyrakRequest(AppModel):
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str

class CreateShanyrakResponse(AppModel):
    _id: str 

@router.post("/", response_model=CreateShanyrakResponse)
def create_shanyrak(
    req: CreateShanyrakRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service)
):
    shanyrak = req.dict()
    shanyrak['user_id'] = jwt_data.user_id

    svc.repository.create_shanyrak(shanyrak)
    return CreateShanyrakResponse(_id=jwt_data.user_id)