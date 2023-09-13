from iss_moex.db import Session
from iss_moex.get_data import get_shares_by_board_id
from iss_moex.models import Share
from iss_moex.schema import validate_create_or_update_share


def post_to_db():
    json_data = get_shares_by_board_id()
    for jd in json_data:
        json_data = validate_create_or_update_share(jd)
        with Session() as session:
            new_share = Share(**json_data)
            session.add(new_share)
            session.commit()
