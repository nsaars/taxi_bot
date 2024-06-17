import requests

from data.config import API_KEY, CLIENT_ID, PARK_ID


class YandexFleetAPI:
    BASE_URL = "https://fleet-api.taxi.yandex.net"

    HEADERS = {
        'X-API-Key': API_KEY,
        'X-Client-ID': CLIENT_ID,
        'Content-Type': 'application/json'
    }

    @classmethod
    def get_driver_by_number(cls, number: str, limit: int = 10, offset: int = 0):
        endpoint = f"{cls.BASE_URL}/v1/parks/driver-profiles/list"
        payload = {
            "query": {
                "park": {
                    "id": PARK_ID
                },
                "limit": limit,
                "offset": offset,
                "text": number,
            }
        }

        response = requests.post(endpoint, json=payload, headers=cls.HEADERS)

        if response.status_code == 200:
            drivers = response.json()
            if not drivers['driver_profiles']:
                return []
            if len(drivers['driver_profiles']) > 1:
                return next(d for d in drivers['driver_profiles'] if d['driver_profile']['work_status'] == 'working')
            return drivers['driver_profiles'][0]
        else:
            response.raise_for_status()

