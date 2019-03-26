if __name__ == "__main__":
    import wneus
    import thingspeak
    from datetime import datetime

    # measure and store result locally
    timestamp = datetime.utcnow()
    data = wneus.measure()
    wneus.log_data_to_csv(timestamp, data)

    # sync local data with thingspeak
    timestamp = thingspeak.read_most_recent_timestamp()
    data = wneus.load_csv_data(since=timestamp)
    thingspeak.bulk_write(data)
