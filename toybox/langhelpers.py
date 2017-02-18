import re


def normalize(name, ignore_rx=re.compile("[^0-9a-zA-Z_]+")):
    return ignore_rx.sub("", name.replace("-", "_"))
