import requests
from secrets import access_token
import json


class ActivitiesDataFetcher:

    def __init__(self):
        pass

    def _get_next_page(self, page_number):
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

        return response.json()

    def get_all(self):
        page_number = 1
        all_activities = []

        while True:
            activities = self._get_next_page(page_number)

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


if __name__ == '__main__':
    fetcher = ActivitiesDataFetcher()
    runs = fetcher.get_all_of_type('Run')
