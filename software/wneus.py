import Adafruit_ADS1x15
import os
import csv
import pandas as pd
from datetime import datetime


def measure():
    adc = Adafruit_ADS1x15.ADS1115()
    values = [adc.read_adc(i, gain=1) for i in range(2)]
    return values


def log_data_to_csv(timestamp, data):
    t = timestamp
    path ='/home/pi/wneus/%d/%d/%d/' % (t.year, t.month, t.day)
    os.makedirs(path, exist_ok=True)
    name = path + 'log_%d%02d%02d.csv' % (t.year, t.month, t.day)
    row = [t.isoformat(), data[0], data[1]]
    with open(name, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(row)


def load_csv_data(since=None, path=None):
    if path is None:
        path ='/home/pi/wneus'

    if since is None:
        t0 = None
    else:
        t0 = datetime(since.year, since.month, since.day)

    frames = []
    for dirpath, dirnames, filenames in os.walk(path):

        if not filenames:
            continue

        if t0:
            year, month, day = [int(x) for x in dirpath.split('/')[-3:]]
            if (datetime(year, month, day) < t0):
                continue

        for f in filenames:
            fname = os.path.join(dirpath, f)
            frame = pd.read_csv(fname, index_col=0, sep=' ', header=None).dropna()
            frame.index = pd.to_datetime(frame.index)
            frames.append(frame)

    frame = pd.concat(frames).sort_index()
    frame = frame.loc[pd.notnull(frame.index)]
    if since:
        frame = frame[frame.index > since]
    return frame
