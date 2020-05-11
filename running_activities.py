import requests
from secrets import access_token
import json


class RunningActivities:

    def __init__(self):
        pass

    def _get_next_page_of_50_activities(self, page_number):
        query = 'https://www.strava.com/api/v3/activities'

        response = requests.get(
            query,
            headers={
                'Content-Type': 'application/json',
                'Authorization': 'Bearer {}'.format(access_token)
            },
            params={
                'per_page': 50,
                'page': page_number
            }
        )

        return response.json()

    def get_all_activities(self):
        page = 1
        all_activities = []

        while True:
            activities = self._get_next_page_of_50_activities(page)

            if not activities:
                break

            all_activities.extend(activities)
            page += 1

        return all_activities

    def get_all_activities_of_type(self, activity_type):
        all_activities = self.get_all_activities()
        running_activities = list(
            filter(lambda x: (x['type'] == activity_type), all_activities))


if __name__ == '__main__':
    runs = RunningActivities()
    runs.get_all_activities_of_type('Run')
