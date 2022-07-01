from datetime import timedelta


def dt(string):
    h, m, s = map(int, string.split(':', maxsplit=3))
    return timedelta(hours=h, minutes=m, seconds=s)
