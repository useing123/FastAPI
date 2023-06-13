from fastapi import Depends, Response, HTTPException, status
from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel

from ..service import Service, get_service
from . import router

@router.delete("/shanyraks/{id}")
def delete_advertisement(
    id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> Response:
    user_id = jwt_data.user_id

    # Use the repository method to check and delete the advertisement
    shanyrak = svc.repository.get_shanyrak(user_id, id)
    if not shanyrak:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="You don't have permission to delete this advertisement",
        )

    svc.repository.delete_shanyrak(user_id, id)

    return Response(status_code=status.HTTP_200_OK)
