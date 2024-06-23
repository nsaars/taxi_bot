import logging
from datetime import datetime
from typing import List, Dict

import requests

from functions.driver_crud import get_all_drivers, update_driver
from data.config import API_KEY, CLIENT_ID, PARK_ID


class ScoreCounter:
    API_URL = "https://fleet-api.taxi.yandex.net/v1/parks/orders/list"

    HEADERS = {
        'X-API-Key': API_KEY,
        'X-Client-ID': CLIENT_ID,
        'Content-Type': 'application/json'
    }

    @classmethod
    def fetch_orders(cls, yandex_id: str, from_time: str, to_time: str = None, limit: int = 500) -> List:
        """
        Fetch orders from Yandex API for a given driver and time range.

        :param yandex_id: Yandex driver ID
        :param from_time: Start time for fetching orders
        :param to_time: End time for fetching orders
        :param limit: Limit of quantity to fetch
        :return: JSON response from the API
        """
        payload = {
            "limit": limit,
            "query": {
                "park": {
                    "id": PARK_ID,
                    "driver_profile": {
                        "id": yandex_id
                    },
                    "order": {
                        "booked_at": {
                            "from": datetime.strptime(from_time, "%Y-%m-%dT%H:%M:%S").strftime(
                                "%Y-%m-%dT%H:%M:%S+00:00"),
                            "to": to_time or datetime.now().strftime("%Y-%m-%dT%H:%M:%S+00:00")
                        },
                    },
                },
            }
        }
        try:
            response = requests.post(cls.API_URL, headers=cls.HEADERS, json=payload)
            response.raise_for_status()
            return response.json().get('orders')
        except requests.exceptions.RequestException as e:
            logging.error(f"HTTP request failed: {e}")
            return []
        except ValueError as e:
            logging.error(f"JSON decoding failed: {e}")
            return []

    @staticmethod
    def calculate_score(orders: List[Dict]) -> float:
        """
        Calculate the score based on the orders' statuses.

        :param orders: List of orders
        :return: Calculated score
        """
        score = 0

        for order in orders:
            events = order.get("events", [])
            statuses = [event["order_status"] for event in events]
            if 'complete' in statuses:
                score += 1
            elif statuses == ['driving', 'waiting', 'cancelled']:
                score += 0.5
        return score

    @classmethod
    def get_driver_new_scores(cls, driver):
        yandex_id = driver.get('yandex_id')
        from_time = driver.get('scores_updated_at')
        limit = 500
        all_orders = last_orders = cls.fetch_orders(yandex_id, from_time, limit=limit)

        if last_orders:
            while len(last_orders) % limit == 0:
                last_orders = cls.fetch_orders(yandex_id, from_time, to_time=last_orders[-1]['booked_at'], limit=limit)
                all_orders.extend(last_orders)

        return cls.calculate_score(all_orders)

    @classmethod
    def update_all_drivers_scores(cls):
        drivers = get_all_drivers()
        for driver in drivers:
            new_scores = cls.get_driver_new_scores(driver)
            update_driver(driver['id'], {'scores': driver['scores'] + new_scores})


