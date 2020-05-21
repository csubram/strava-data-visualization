from activities_data_fetcher import ActivitiesDataFetcher
import pandas as pd
import matplotlib.pyplot as plt
from isoweek import Week
import calendar
import unit_utils
import graph_utils


class DistancePlotter:

    def __init__(self, activity_type):
        plt.rcParams.update({'figure.autolayout': True})

        graph_utils.create_output_directory()
        self.distance_dataframe = self._create_distance_tracker_dataframe(activity_type)

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
        date_obj = unit_utils.get_datetime_from_iso8601_string(activity['start_date'])

        activity_distance = {
            'date': date_obj,
            'date_year': date_obj.isocalendar()[0],
            'date_month': date_obj.month,
            'date_week': date_obj.isocalendar()[1],
            'distance': unit_utils.convert_meters_to_miles(activity['distance'])
        }

        return activity_distance

    def _get_weekly_x_axis_ticks(self, weekly_totals):
        weekly_ticks = []

        for week_tuple in weekly_totals.index:
            start_date_of_week = Week(*week_tuple).monday()
            weekly_ticks.append(start_date_of_week)

        return weekly_ticks

    def _get_monthly_x_axis_ticks(self, monthly_totals):
        monthly_ticks = []

        for year_val, month_val in monthly_totals.index:
            abbreviated_month_name = calendar.month_abbr[month_val]
            month_label = '{0} {1}'.format(abbreviated_month_name, year_val)
            monthly_ticks.append(month_label)

        return monthly_ticks

    def _generate_graph_object(self, interval_totals, make_x_tick_labels):
        graph = interval_totals.plot(kind='bar', legend=None)

        graph.set(xlabel='', ylabel='Distance in miles')
        x_axis_ticks = make_x_tick_labels(interval_totals)
        graph.set_xticklabels(x_axis_ticks, rotation=45)

    def _divide_dataframe_by_interval(self, interval):
        interval_groups = self.distance_dataframe.groupby(
            [self.distance_dataframe['date_year'], self.distance_dataframe[interval]])

        sum_total_per_interval = interval_groups['distance'].sum()
        return sum_total_per_interval

    def plot_distance_per_week(self):
        weekly_totals = self._divide_dataframe_by_interval('date_week')

        self._generate_graph_object(weekly_totals, self._get_weekly_x_axis_ticks)
        graph_utils.save_graph(filename='distance_per_week.png')

    def plot_distance_per_month(self):
        monthly_totals = self._divide_dataframe_by_interval('date_month')

        self._generate_graph_object(monthly_totals, self._get_monthly_x_axis_ticks)
        graph_utils.save_graph(filename='distance_per_month.png')


if __name__ == '__main__':
    cg = DistancePlotter(activity_type='Run')
    cg.plot_distance_per_week()
    cg.plot_distance_per_month()
