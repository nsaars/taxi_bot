import requests
from typing import Any, Dict, List, Optional
from data.config import API_BASE_URL


class ApiClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def _request(self, method: str, endpoint: str, params: Optional[Dict[str, Any]] = None,
                 json: Optional[Dict[str, Any]] = None) -> Any:
        url = f"{self.base_url}/{endpoint}/"
        response = requests.request(method, url, params=params, json=json)
        response.raise_for_status()
        return response.json()

    def get_items(self, endpoint: str, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self._request("GET", endpoint, params=filters)

    def create_item(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        return self._request("POST", endpoint, json=data)

    def patch_item(self, endpoint: str, item_id: int, data: Dict[str, Any]) -> Dict[str, Any]:

        return self._request("PATCH", f"{endpoint}/{item_id}", json=data)

    def delete_items(self, endpoint: str, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self._request("DELETE", endpoint, params=filters)


api_client: ApiClient = ApiClient(API_BASE_URL)

