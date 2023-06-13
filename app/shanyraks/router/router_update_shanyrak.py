from app.utils import AppModel
from . import router
from ..service import Service, get_service
from fastapi import Depends, Response
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data


class UpdateShanyrakResponse(AppModel):
    _id: str
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str
    user_id: str

@router.patch("/{id}", status_code=200, response_model=UpdateShanyrakResponse)
def update_shanyrak(id: str, input: UpdateShanyrakResponse, svc: Service = Depends(get_service)) -> dict[str, str]:
    svc.repository.update_shanyrak(id, input.dict())
    return Response(status_code=200)