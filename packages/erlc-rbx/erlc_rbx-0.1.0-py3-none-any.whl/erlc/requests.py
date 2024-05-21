import requests
from erlc import BASE_URL
from erlc.headers import make_auth_headers


def make_get_request(endpoint: str, server_key: str, global_key: str | None = None):
    """internal method to make a get request to the API
    :param global_key: (USUALLY NOT NEEDED) the global API key
    :param server_key: the server API key
    :param endpoint: the endpoint to send the request to

    :returns: the JSON data or None if the request failed.
    """

    headers = make_auth_headers(server_key, global_key)

    try:
        response = requests.get(f"{BASE_URL}/{endpoint}", headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as exception:
        print(f"[ERROR] get request failed: {exception}")
        return None


def make_post_request(
    endpoint: str, data: str, server_key: str, global_key: str | None = None
):
    """internal method to make a post request to the API
    :param global_key: (USUALLY NOT NEEDED) the global API key
    :param server_key: the server API key
    :param endpoint: the endpoint to send the request to
    :param data: JSON data to send with the request

    :returns: the JSON data or None if the request failed.
    """
    headers = make_auth_headers(server_key, global_key)
    try:
        response = requests.post(f"{BASE_URL}/{endpoint}", json=data, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as exception:
        print(f"[ERROR] post request failed: {exception}")
