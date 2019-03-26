import thingspeak
import wneus
from datetime import datetime


class TestThingSpeak:
    def test_write(self):
        thingspeak.write((1000, 2000))

    def test_read_most_recent_timestamp(self):
        print(thingspeak.read_most_recent_timestamp())

    def test_bulk_write(self):
        path = '../measurements/trial000/wneus'
        data = wneus.load_csv_data(path=path)
        print(len(data))
        codes = thingspeak.bulk_write(data)
        print(codes)


class TestWneus:
    def test_load_csv_data(self):
        timestamp = datetime(2019, 2, 12, 16, 2, 0)
        path = '../measurements/trial000/wneus'
        df = wneus.load_csv_data(timestamp, path)
        print(df)
