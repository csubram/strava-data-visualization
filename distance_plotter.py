from activities_data_fetcher import ActivitiesDataFetcher
import pandas as pd
import dateutil.parser
import matplotlib.pyplot as plt
import os
from isoweek import Week
import calendar

OUTPUT_DIRECTORY = 'graphs'


class DistancePlotter:

    def __init__(self, activity_type):
        plt.rcParams.update({'figure.autolayout': True})

        self._create_output_directory()
        self.distance_dataframe = self._create_distance_tracker_dataframe(activity_type)

    def _create_output_directory(self):
        if not os.path.exists(OUTPUT_DIRECTORY):
            os.makedirs(OUTPUT_DIRECTORY)

    def _create_distance_tracker_dataframe(self, activity_type):
        fetcher = ActivitiesDataFetcher()
        matching_activities = fetcher.get_all_of_type(activity_type)

        column_names = ['date', 'date_week', 'date_month', 'date_year', 'distance']
        dist_dataframe = pd.DataFrame(columns=column_names)

        for activity in matching_activities:
            activity_distance = self._get_distance_and_date_from_activity(activity)
            dist_dataframe = dist_dataframe.append(activity_distance, ignore_index=True)

        return dist_dataframe

    def _get_distance_and_date_from_activity(self, activity):
        date_obj = self._getDateTimeFromISO8601String(activity['start_date'])

        activity_distance = {
            'date': date_obj,
            'date_year': date_obj.isocalendar()[0],
            'date_month': date_obj.month,
            'date_week': date_obj.isocalendar()[1],
            'distance': self._convert_meters_to_miles(activity['distance'])
        }

        return activity_distance

    def _getDateTimeFromISO8601String(self, datetime_string):
        datetime_object = dateutil.parser.parse(datetime_string)
        return datetime_object

    def _convert_meters_to_miles(self, distance):
        return distance * 0.000621371

    def _save_graph(self, interval_size):
        output_file_location = os.path.join(
            OUTPUT_DIRECTORY, 'distance_per_{}.png'.format(interval_size))

        plt.savefig(output_file_location)

    def _get_weekly_x_labels(self, weekly_totals):
        week_labels = []

        for week_tuple in weekly_totals.index:
            start_date_of_week = Week(*week_tuple).monday()
            week_labels.append(start_date_of_week)

        return week_labels

    def _get_monthly_x_labels(self, monthly_totals):
        month_labels = []

        for month_tuple in monthly_totals.index:
            abbreviated_month_name = calendar.month_abbr[month_tuple[1]]
            year = month_tuple[0]
            month_label = '{0} {1}'.format(abbreviated_month_name, year)
            month_labels.append(month_label)

        return month_labels

    def _generate_graph_object(self, interval_totals, make_x_tick_labels):
        graph = interval_totals.plot(kind='bar', legend=None)
        graph.set(xlabel='', ylabel='Distance in miles')
        x_labels = make_x_tick_labels(interval_totals)
        graph.set_xticklabels(x_labels, rotation=45)

    def _sum_distance_within_interval(self, interval_grouping):
        sum_total_per_interval = interval_grouping['distance'].sum()
        return sum_total_per_interval

    def _divide_dataframe_by_interval(self, interval):
        interval_groups = self.distance_dataframe.groupby(
            [self.distance_dataframe['date_year'], self.distance_dataframe[interval]])
        return interval_groups

    def plot_distance_per_week(self):
        weeks = self._divide_dataframe_by_interval('date_week')
        weekly_totals = self._sum_distance_within_interval(weeks)

        self._generate_graph_object(weekly_totals, self._get_weekly_x_labels)
        self._save_graph('week')

    def plot_distance_per_month(self):
        months = self._divide_dataframe_by_interval('date_month')
        monthly_totals = self._sum_distance_within_interval(months)

        self._generate_graph_object(monthly_totals, self._get_monthly_x_labels)
        self._save_graph('month')


if __name__ == '__main__':
    cg = DistancePlotter(activity_type='Run')
    cg.plot_distance_per_week()
    cg.plot_distance_per_month()
