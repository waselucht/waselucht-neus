import Adafruit_ADS1x15


def measure():
    adc = Adafruit_ADS1x15.ADS1115()
    values = [adc.read_adc(i, gain=1) for i in range(2)]
    return values


if __name__ == "__main__":
    from datetime import datetime
    import os
    import csv

    t = datetime.utcnow()
    data = measure()
    path ='/home/pi/wneus/%d/%d/%d/' % (t.year, t.month, t.day)
    os.makedirs(path, exist_ok=True)
    name = path + 'log_%d%02d%02d.csv' % (t.year, t.month, t.day)
    row = [t.isoformat(), data[0], data[1]]
    with open(name, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(row)
