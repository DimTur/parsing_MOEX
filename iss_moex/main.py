import json
import requests

from urllib import parse
from sysconfig import get_path


def get_json_data(method: str, **kwargs):
    """
    Sens a requests to ISS MOEX and return json object
    with list of securities traded on the Moscow Exchange

    :param method:
    :param kwargs:
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


def convert_to_two_demensional_array(json_data, blockname):
    json_data = get_json_data(blockname)
    if json_data and blockname in json_data:
        columns = json_data[blockname]["columns"]
        for row in json_data[blockname]["data"]:
            dict_securities = {column: value for column, value in zip(columns, row)}
            # в будущем, возможно, имеет смысл применить yield
            return dict_securities


if __name__ == "__main__":
    # Список бумаг торгуемых на московской бирже
    # https://iss.moex.com/iss/reference/5
    json_data = get_json_data("securities")
    f = convert_to_two_demensional_array(json_data, "securities")

    print(f)
