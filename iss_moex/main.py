import json
import requests

from urllib import parse
from sysconfig import get_path


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
        json_data = response.json()
        return json_data

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


def convert_to_two_dimensional_array(json_data, blockname):
    """
    Transforms json object to two-dimensional array

    :param json_data: json object from Moscow Exchange
    :param blockname: ISS Queries
    read more at https://iss.moex.com/iss/reference/
    :return: list of dicts with all info about securities
    """
    json_data = get_json_data(blockname)
    if json_data and blockname in json_data:
        list_of_dicts_securities = [
            {column: row[index] for index, column in enumerate(json_data[blockname]["columns"])}
            for row in json_data[blockname]["data"]
        ]
        # in the future it maybe necessary to use 'yield'
        return list_of_dicts_securities



if __name__ == "__main__":
    # List of securities traded on the Moscow stock exchange
    # https://iss.moex.com/iss/reference/5
    json_data = get_json_data("securities")
    f = convert_to_two_dimensional_array(json_data, "securities")

    print(f)
