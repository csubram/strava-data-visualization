from activities_data_fetcher import ActivitiesDataFetcher
import pandas as pd
import matplotlib.pyplot as plt
import calendar
import unit_utils
import graph_utils


class PacePlotter:

    def __init__(self, activity_type):
        plt.rcParams.update({'figure.autolayout': True})
        graph_utils.create_output_directory()
        self.pace_dataframe = self._create_pace_tracker_dataframe(activity_type)

    def _create_pace_tracker_dataframe(self, activity_type):
        fetcher = ActivitiesDataFetcher()
        matching_activities = fetcher.get_all_of_type(activity_type)

        column_names = ['date_month', 'date_year', 'pace']
        pace_dataframe = pd.DataFrame(columns=column_names)

        for activity in matching_activities:
            activity_pace = self._get_pace_from_activity(activity)
            pace_dataframe = pace_dataframe.append(activity_pace, ignore_index=True)

        return pace_dataframe

    def _get_pace_from_activity(self, activity):
        date_obj = unit_utils.get_datetime_from_iso8601_string(activity['start_date'])

        activity_pace = {
            'date': date_obj,
            'date_year': date_obj.isocalendar()[0],
            'date_month': date_obj.month,
            'pace': unit_utils.convert_meters_per_second_to_minutes_per_mile(activity['average_speed'])
        }

        return activity_pace

    def _format_y_axis_ticks(self, y_ticks):
        pace_str_ticks = []

        for tick_value in y_ticks:
            num_minutes = int(tick_value)
            num_seconds = int((tick_value - num_minutes) * 60)
            pace_str = '{}:{:02d} /mi'.format(num_minutes, num_seconds)
            pace_str_ticks.append(pace_str)

        return pace_str_ticks

    def _format_x_axis_ticks(self, x_ticks):
        monthly_ticks = []

        for tick_value in x_ticks:
            tick_text = tick_value.get_text()
            tick_text_without_parentheses = tick_text[1:-1]
            (year_val, month_val) = tick_text_without_parentheses.split(',')

            month_name = calendar.month_abbr[int(month_val)]
            month_label = '{0} {1}'.format(month_name, year_val)
            monthly_ticks.append(month_label)

        return monthly_ticks

    def _beautify_graph_axes(self, graph):
        graph.set(xlabel='')
        plt.suptitle('')

        y_tick_labels = self._format_y_axis_ticks(graph.get_yticks())
        graph.set_yticklabels(y_tick_labels)

        x_tick_labels = self._format_x_axis_ticks(graph.get_xticklabels())
        graph.set_xticklabels(x_tick_labels, rotation=45)

    def plot_pace_each_month(self):
        graph = self.pace_dataframe.boxplot(
            by=['date_year', 'date_month'], column=['pace'], grid=False)

        self._beautify_graph_axes(graph)
        graph_utils.save_graph(filename='pace_each_month.png')


if __name__ == '__main__':
    pp = PacePlotter('Run')
    pp.plot_pace_each_month()
