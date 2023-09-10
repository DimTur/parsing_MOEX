import pandas as pd
pd.set_option("display.max_columns", 27)

import json
import requests

from urllib import parse


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
            {column: row[index] for index, column in enumerate(json_obj[blockname]["columns"])}
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


def get_shares_by_board_id(iss_only):
    # get a table of shares by board
    # https://iss.moex.com/iss/reference/32
    engine = "stock"
    market = "shares"
    boardid = "TQBR"
    method = f"/engines/{engine}/markets/{market}/boards/{boardid}/securities/"
    json_obj = get_json_data(
        method=method,
        iss_only=iss_only,
    )
    list_of_dicts = convert_to_two_dimensional_array(
        json_obj,
        "marketdata"
    )
    return list_of_dicts


if __name__ == "__main__":
    # f = get_shares()
    f = get_shares_by_board_id("iss.only=marketdata")
    print(pd.DataFrame(f))


    # Get tool specification
    # https://iss.moex.com/iss/reference/13
    # secid = "RU000A1032P1"
    # method = "securities/%s" % secid
    # json_data = get_json_data(method)
    # f = convert_to_two_dimensional_array(json_data, "description")

    # get volume today in last session
    # https://iss.moex.com/iss/reference/823
    # engine = "stock"
    # market = "shares"
    # tradingsession = 3
    # boardid = "TQBR"
    # securities = "SBER,TTLK"  # we need to indicate like that, because this is requires of Moscow stock exchange
    # method = f"/engines/{engine}/markets/{market}/secstats/"
    # json_data = get_json_data(method, tradingsession=tradingsession, securities=securities, boardid=boardid)
    # f = convert_to_two_dimensional_array(json_data, "secstats")
    #
    # print(pd.DataFrame(f))
    # print(json_data)

    # Get data on the specified instrument on the selected trading mode
    # https://iss.moex.com/iss/reference/53
    # engine = "stock"
    # market = "shares"
    # boardid = "TQBR"
    # secid = "SBER"
    # method = f"/engines/{engine}/markets/{market}/boards/{boardid}/securities/{secid}"
    # json_data = get_json_data(method)
    # list_1 = convert_to_two_dimensional_array(json_data, "securities")
    #
    # print(pd.DataFrame(list_1))
    # print(json_data)
