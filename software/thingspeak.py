import urllib
from urllib.request import urlopen, Request
from urllib.error import HTTPError
import json
import datetime
import os
import json
import time


def _get_default_write_api_key():
    return os.environ["THINGSPEAK_WRITE_API_KEY"]


def _get_default_channel_id():
    return int(os.environ["THINGSPEAK_CHANNEL"])


def write(fields, timestamp=None, write_api_key=None):
    """write channel fields to thingspeak"""
    if write_api_key is None:
        write_api_key = _get_default_write_api_key()
    base_url = 'https://api.thingspeak.com/update?api_key=%s' % write_api_key
    url = base_url + '&field1=%d&field2=%d' % fields
    if timestamp:
        url = url + '&created_at='
        url = url + datetime.datetime.strftime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
    conn = urlopen(url)
    conn.close()


def _dump(data):
    dump = []
    for t, (field1, field2) in data.iterrows():
        message = {}
        message['created_at'] = str(t)
        message['field1'] = int(field1)
        message['field2'] = int(field2)
        dump.append(message)
    return dump


def bulk_write(data, write_api_key=None, channel=None, max_size=600, interval=15):
    """Bulk write data to thingspeak channel.

    data is pandas dataframe
    
    Returns url code(s)
        - A 202 indicates that the server has accepted the request
        - multiple codes are returned in case data size > max_size
    """
    if write_api_key is None:
        write_api_key = _get_default_write_api_key()
    if channel is None:
        channel = _get_default_channel_id()

    url = "https://api.thingspeak.com/channels/%d/bulk_update.json" % channel

    codes = []
    for i in range(0, len(data), max_size):
        chunk_data = data[i:i + max_size]
        data_ = json.dumps({'write_api_key': write_api_key,
                            'updates': _dump(chunk_data)}).encode('gbk')
        req = Request(url=url)
        request_headers = {"User-Agent": "mw.doc.bulk-update (Raspberry Pi)",
                           "Content-Type": "application/json",
                           "Content-Length":str(len(chunk_data))}
        for key, val in request_headers.items():
            req.add_header(key, val)
        req.data = data_

        try:
            response = urlopen(req)
            code = response.getcode()
        except HTTPError as e:
            code = e.code

        codes.append(code)

        if (i + max_size) < len(data):
            time.sleep(interval)

    return codes


def read_most_recent_timestamp(channel=None):
    if channel is None:
        channel = _get_default_channel_id()
    url = 'https://api.thingspeak.com/channels/%d/feeds.json?results=1' % channel
    conn = urlopen(url)
    data_string = conn.read().decode('utf-8')
    conn.close()
    data_dict = json.loads(data_string)
    timestamp_string = data_dict['feeds'][0]['created_at']
    timestamp = datetime.datetime.strptime(timestamp_string, '%Y-%m-%dT%H:%M:%SZ')
    return timestamp
