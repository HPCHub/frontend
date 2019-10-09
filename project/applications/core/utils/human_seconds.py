"""Convert seconds to human readable interval back and forth."""
from collections import OrderedDict
import re

interval_dict = OrderedDict([("h", 3600),       # 1 hour
                             ("m", 60),         # 1 minute
                             ("s", 1)])         # 1 second


def seconds_to_human(seconds):
    """Convert seconds to human readable format like 1M.

    :param seconds: Seconds to convert
    :type seconds: int

    :rtype: int
    :return: Human readable string
    """
    seconds = int(seconds)
    string = ""
    for unit, value in interval_dict.items():
        subres = round(seconds / value)
        if subres>=1:
            seconds -= value * subres
            string += str(subres) + unit
    return string


def human_to_seconds(string):
    """Convert internal string like 1M, 1Y3M, 3W to seconds.

    :type string: str
    :param string: Interval string like 1M, 1W, 1M3W4h2s...
        (s => seconds, m => minutes, h => hours, D => days, W => weeks, M => months, Y => Years).

    :rtype: int
    :return: The conversion in seconds of string.
    """
    interval_exc = "Bad interval format for {0}".format(string)

    interval_regex = re.compile("^(?P<value>[0-9]+)(?P<unit>[{0}])".format("".join(interval_dict.keys())))
    seconds = 0

    while string:
        match = interval_regex.match(string)
        if match:
            value, unit = int(match.group("value")), match.group("unit")
            if int(value) and unit in interval_dict:
                seconds += value * interval_dict[unit]
                string = string[match.end():]
            else:
                raise Exception(interval_exc)
        else:
            raise Exception(interval_exc)
    return seconds

if __name__ == "__main__":
    assert seconds_to_human(324234) == "3D18h3m54s"
    assert human_to_seconds("3D18h3m54s") == 324234
    assert seconds_to_human(365 * 86400) == "1Y"
    assert human_to_seconds("1Y") == 365 * 86400