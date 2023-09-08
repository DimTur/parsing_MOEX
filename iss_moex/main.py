import pandas as pd
pd.set_option("display.max_columns", 15)

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


if __name__ == "__main__":
    # List of securities traded on the Moscow stock exchange
    # params for method "securities" at https://iss.moex.com/iss/reference/5
    # method = "securities"
    # json_data = get_json_data(method)
    # json_data = get_json_data(method, q="AAPL")
    # json_data = get_json_data(method, group_by="type", group_by_filter="corporate_bond", limit=10)
    # json_data = get_json_data(method, q="втб", group_by="type", group_by_filter="corporate_bond", limit=10)
    # f = convert_to_two_dimensional_array(json_data, "securities")


    #Get tool specification
    #https://iss.moex.com/iss/reference/13
    secid = "RU000A1032P1"
    method = "securities/%s" % secid
    json_data = get_json_data(method)
    f = convert_to_two_dimensional_array(json_data, "description")

    print(pd.DataFrame(f))
