import datetime
import json
import requests
import time


TIMEOUT = 30
TS_FORMAT = r'%Y-%m-%dT%H:%M:%SZ'


def check_kt_status():
    '''
    Returns (success, response_time)
    '''
    start_time = time.time()
    try:
        r = requests.get('https://kritikustomeg.org', timeout=TIMEOUT)
    except requests.exceptions.Timeout:
        return (0, TIMEOUT)
    except requests.exceptions.ConnectionError:
        return (0, time.time() - start_time)
    t = r.elapsed.total_seconds()
    if r.status_code != 200:
        return (0, t)
    return (1, t)


def main():
    T = datetime.datetime.utcnow()
    T_ts = T.strftime(TS_FORMAT)
    T_h = T.strftime(r'%Y%m%d-%H')
    T_m = T.strftime(r'%Y%m%d-%H%M')
    success, response_time = check_kt_status()
    with open('data/raw/{}.log'.format(T_h), 'a') as f:
        f.write('{} {} {}\n'.format(
            T_m, success, response_time,
        ))
    with open('static/data/current.json', 'w') as f:
        json.dump({
            'timestamp': T_ts,
            'success': success,
            'response_time': response_time,
        }, f, sort_keys=True, indent=4)
    print(T_m, success, response_time)


if __name__ == '__main__':
    main()
