import requests


class Connection:
    def __init__(self, url, api_key):
        self.url = url
        self.api_key = api_key

    def junction_request(self, service, query, cargo):
        headers = {"x-api-key": self.api_key}
        payload = {
            "service": service,
            "query": query,
            "cargo": cargo
        }
        response = requests.post(self.url, json=payload, headers=headers)
        if response.status_code != 200:
            raise JunctionError(f"received bad status code: <{response.status_code}> for payload: {payload}")
        wrapper = response.json()

        if wrapper["success"] is False:
            error = wrapper["error"]
            raise JunctionError(f"error: {error}")

        return wrapper["content"]


class JunctionError(Exception):
    pass
