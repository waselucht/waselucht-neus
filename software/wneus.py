import Adafruit_ADS1x15
from urllib.request import urlopen


def measure():
    adc = Adafruit_ADS1x15.ADS1115()
    values = [adc.read_adc(i, gain=1) for i in range(2)]
    return values


def write_to_thingspeak(write_api_key, fields):
    """write channel fields to thingspeak"""
    base_url = 'https://api.thingspeak.com/update?api_key=%s' % write_api_key
    fields_url = '&field1=%d&field2=%d' % fields
    conn = urlopen(base_url + fields_url)
    conn.close()


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

    # don`t care if this fails
    write_api_key = os.environ["THINGSPEAK_WRITE_API_KEY"]
    write_to_thingspeak(write_api_key, tuple(data))
