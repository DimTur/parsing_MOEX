import pandas as pd
pd.set_option("display.max_columns", 55)

import json
import requests

from urllib import parse
from datetime import datetime


def get_json_data(method: str, **kwargs):
    """
    Sens a requests to ISS MOEX and return json object
    with list of securities traded on the Moscow Exchange

    :param method: a string representing the API method to be called
    :param kwargs: additional keyword arguments to include in the request
    read more at https://iss.moex.com/iss/reference/
    :return: json object
    """
    try:
        url = "https://iss.moex.com/iss/%s.json" % method
        if kwargs:
            url += "?" + parse.urlencode(kwargs)
        response = requests.get(url)
        json_obj = response.json()
        return json_obj

    except requests.exceptions.ConnectionError as e:
        print("Connection error: %s" % str(e))
        return None

    except requests.exceptions.HTTPError as e:
        print("HTTP error: %s" % str(e))
        return None

    except json.decoder.JSONDecodeError as e:
        print("JSON decoding error: %s" % str(e))
        return None

    except Exception as e:
        print("Unhandled error: %s" % str(e))
        return None


def convert_to_two_dimensional_array(json_obj, blockname):
    """
    Transforms json object to two-dimensional array

    :param json_obj: json object from Moscow Exchange
    :param blockname: ISS Queries
    read more at https://iss.moex.com/iss/reference/
    :return: list of dicts with all info about securities
    """
    if json_obj and blockname in json_obj:
        list_of_dicts_securities = [
            {str.lower(column): row[index] for index, column in enumerate(json_obj[blockname]["columns"])}
            for row in json_obj[blockname]["data"]
        ]
        # in the future it maybe necessary to use 'yield'
        return list_of_dicts_securities


def get_shares(page=1, limit=10):
    # List of securities traded on the Moscow stock exchange
    # params for method "securities" at https://iss.moex.com/iss/reference/5
    json_obj = get_json_data(
        "securities",
        group_by="group",
        group_by_filter="stock_shares",
        limit=limit,
        start=((page-1) * limit),
    )
    list_of_dicts = convert_to_two_dimensional_array(
        json_obj,
        "securities",
    )
    return list_of_dicts


def get_shares_by_board_id():
    # get a table of shares by board
    # https://iss.moex.com/iss/reference/32
    engine = "stock"
    market = "shares"
    boardid = "TQBR"
    method = f"/engines/{engine}/markets/{market}/boards/{boardid}/securities/"
    json_obj = get_json_data(
        method=method,
        iss_only="iss.only=marketdata",
    )
    list_of_dicts = convert_to_two_dimensional_array(
        json_obj,
        "marketdata"
    )
    new_list_of_dicts = []
    for d in list_of_dicts:
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        new_dict = {
            "secid": d["secid"],
            "last": d["last"],
            "valtoday": d["valtoday"],
            "date_time": formatted_datetime,
        }
        new_list_of_dicts.append(new_dict)
    return new_list_of_dicts


def get_last_price_and_valtoday(secid: str):
    engine = "stock"
    market = "shares"
    boardid = "TQBR"
    method = f"/engines/{engine}/markets/{market}/boards/{boardid}/securities/{secid}/"
    json_obj = get_json_data(
        method=method,
        iss_only="iss.only=marketdata",
    )
    dict_with_new_price_and_valtoday = convert_to_two_dimensional_array(
        json_obj,
        "marketdata"
    )
    return {
        "last": dict_with_new_price_and_valtoday[0]["last"],
        "valtoday": dict_with_new_price_and_valtoday[0]["valtoday"]
    }


if __name__ == "__main__":
    # f = get_shares()
    f = get_shares_by_board_id()
    # f = get_last_price_and_valtoday("SBER")
    # print(f)
    print(pd.DataFrame(f))
