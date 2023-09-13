from pydantic import BaseModel
from errors import HttpError
from typing import Union


class CreateOrUpdateShare(BaseModel):
    secid: str
    last: Union[float, None]
    valtoday: Union[float, None]
    systime: str


def validate_create_or_update_share(json_data):
    try:
        share_schema = CreateOrUpdateShare(**json_data)
        return share_schema.dict()
    except ValueError as er:
        raise HttpError(status_code=400, message=er.errors())
