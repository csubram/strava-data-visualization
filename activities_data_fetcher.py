import requests
from secrets import access_token
import json
import logging
from exceptions import AccessTokenError


class ActivitiesDataFetcher:

    def __init__(self):
        pass

    def _attempt_to_get_page(self, page_number):
        try:
            next_page = self._get_page(page_number)
            return next_page
        except AccessTokenError as e:
            logging.error(e.message)

    def _get_page(self, page_number):
        query = 'https://www.strava.com/api/v3/activities'
        response = requests.get(
            query,
            headers={
                'Content-Type': 'application/json',
                'Authorization': 'Bearer {}'.format(access_token)
            },
            params={
                'page': page_number
            }
        )

        self._verify_query_response_is_ok(response)
        return response.json()

    def _verify_query_response_is_ok(self, response):
        if response.status_code != 200:
            raise AccessTokenError(response.json()['message'])

    def get_all(self):
        page_number = 1
        all_activities = []

        while True:
            activities = self._attempt_to_get_page(page_number)

            if not activities:
                break

            all_activities.extend(activities)
            page_number += 1

        return all_activities

    def get_all_of_type(self, activity_type):
        all_activities = self.get_all()
        filtered_activities = list(
            filter(lambda x: (x['type'] == activity_type), all_activities))
        return filtered_activities

    def get_by_id(self, activity_id):
        query = 'https://www.strava.com/api/v3/activities/{}'.format(activity_id)
        response = requests.get(
            query,
            headers={
                'Content-Type': 'application/json',
                'Authorization': 'Bearer {}'.format(access_token)
            }
        )

        self._verify_query_response_is_ok(response)
        return response.json()


if __name__ == '__main__':
    fetcher = ActivitiesDataFetcher()
    runs = fetcher.get_all_of_type('Run')

    specific_activity = fetcher.get_by_id(3436366608)
