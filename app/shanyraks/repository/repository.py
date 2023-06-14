from typing import Optional
from bson.objectid import ObjectId
from fastapi import Depends, HTTPException, Response
from pymongo.database import Database
from fastapi import APIRouter

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from ..service import Service, get_service
from app.utils import AppModel

router = APIRouter()


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
    svc: Service = Depends(get_service),
):
    shanyrak = req.dict()
    shanyrak['user_id'] = jwt_data.user_id

    shanyrak_id = svc.repository.create_shanyrak(shanyrak)
    return CreateShanyrakResponse(_id=str(shanyrak_id))


class ShanyrakRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_shanyrak(self, input: dict) -> ObjectId:
        payload = {
            "type": input['type'],
            "price": input['price'],
            "address": input['address'],
            "area": input['area'],
            "rooms_count": input['rooms_count'],
            "description": input['description'],
            "user_id": input['user_id']
        }

        result = self.database['shanyraks'].insert_one(payload)
        return result.inserted_id

    def get_shanyrak(self, user_id: str, shanyrak_id: str):
        shanyrak = self.database["shanyraks"].find_one(
            {
                "_id": ObjectId(shanyrak_id),
            }
        )

        if shanyrak and shanyrak.get('user_id') == user_id:
            return shanyrak
        else:
            raise HTTPException(status_code=404, detail="Shanyrak not found")

    def update_shanyrak(self, shanyrak_id: str, data: dict):
        self.database['shanyraks'].update_one(
            filter={"_id": ObjectId(shanyrak_id)},
            update={
                "$set": data
            }
        )

    def delete_shanyrak(self, user_id: str, shanyrak_id: str):
        shanyrak = self.get_shanyrak(user_id, shanyrak_id)

        if shanyrak and shanyrak.get('user_id') == user_id:
            self.database["shanyraks"].delete_one(
                filter={"_id": ObjectId(shanyrak_id)},
            )
            return Response(status_code=200)
        else:
            raise HTTPException(status_code=404, detail="Shanyrak not found")
