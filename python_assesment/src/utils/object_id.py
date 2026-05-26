from bson import ObjectId
from bson.errors import InvalidId

from fastapi import HTTPException


def validate_object_id(document_id: str):

    try:
        return ObjectId(document_id)

    except InvalidId:
        raise HTTPException(
            status_code=400,
            detail="Invalid document id"
        )