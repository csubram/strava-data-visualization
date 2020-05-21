import dateutil.parser


def convert_meters_to_miles(distance):
    return distance * 0.000621371


def convert_meters_per_second_to_minutes_per_mile(average_speed):
    miles_per_second = convert_meters_to_miles(average_speed)
    seconds_per_mile = 1 / miles_per_second
    minutes_per_mile = seconds_per_mile * (1 / 60)
    return minutes_per_mile


def get_datetime_from_iso8601_string(datetime_string):
    datetime_object = dateutil.parser.parse(datetime_string)
    return datetime_object
