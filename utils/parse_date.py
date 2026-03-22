import re
import pandas as pd


def parse_date(data):
    if re.match(r'^\d{4}-\d{2}-\d{2}$', str(data)):
        return pd.to_datetime(data, format='%Y-%m-%d')
    elif re.match(r'^\d{2}-\d{2}-\d{4}$', str(data)):
        return pd.to_datetime(data, format='%d-%m-%Y')
    return pd.NaT
