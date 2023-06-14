from bson.objectid import ObjectId
from pymongo.database import Database
from fastapi import Response


class ShanyrakRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_shanyrak(self, input: dict):
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
        req_id = str(result.inserted_id)
        return req_id

    def get_shanyrak(self, user_id: str, shanyrak_id: str):
        shanyrak = self.database["shanyraks"].find_one(
            {
                "_id": ObjectId(shanyrak_id),
            }
        )

        if (shanyrak['user_id'] == user_id):
            return shanyrak

    def update_shanyrak(self, id: str, data: dict):
        self.database['shanyraks'].update_one(
            filter={"_id": ObjectId(id)},
            update={
                "$set": data
            }
        )

    def delete_shanyrak(self, user_id: str, shanyrak_id: str):
        shanyrak = self.database["shanyraks"].find_one(
            {
                "_id": ObjectId(shanyrak_id),
            }
        )
        if (user_id == shanyrak['user_id']):
            self.database["shanyraks"].delete_one(
                filter={"_id": ObjectId(shanyrak_id)},
            )   
            return Response(status_code=200)
        return Response(status_code=404)