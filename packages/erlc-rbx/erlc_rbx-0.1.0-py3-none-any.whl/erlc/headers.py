def make_auth_headers(server_key: str, global_key: str | None = None):
    """
    internal function to generate the authentication headers
    :param server_key: the server API key
    :param global_key: (USUALLY NOT REQUIRED!) the global API key
    :return: a dictionary with the authentication headers
    """
    headers = {"Server-Key": server_key}

    if global_key:
        headers["Authorization"] = f"Bearer {global_key}"

    return headers
