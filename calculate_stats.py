import datetime
import json
import math
import sys


TS_FORMAT = r'%Y-%m-%dT%H:%M:%SZ'


def percentile(sorted_items, p):
    idx = (len(sorted_items) - 1) * p / 100
    idx_1 = math.floor(idx)
    idx_2 = math.ceil(idx)
    if idx_1 == idx_2:
        return sorted_items[idx_1]
    return (idx_2 - idx) * sorted_items[idx_1] + (idx - idx_1) * sorted_items[idx_2]


def get_stats(items):
    sorted_items = sorted(items)
    avg = sum(sorted_items) / len(sorted_items)
    p50 = percentile(sorted_items, 50)
    p90 = percentile(sorted_items, 90)
    p95 = percentile(sorted_items, 95)
    return (avg, p50, p90, p95)


def get_data_for_hour(T_h):
    success_list = []
    response_time_list = []
    try:
        with open('data/raw/{}.log'.format(T_h), 'r') as f:
            for line in f:
                T_m, success, response_time = line.strip().split(' ')
                success = int(success)
                response_time = float(response_time)
                success_list.append(success)
                response_time_list.append(response_time)
    except Exception:
        pass
    return success_list, response_time_list


def get_data_for_day(T_d):
    success_list = []
    response_time_list = []
    for h in range(24):
        if h < 10:
            hh = '0{}'.format(h)
        else:
            hh = '{}'.format(h)
        T_h = '{}-{}'.format(T_d, hh)
        success_list_h, response_time_list_h = get_data_for_hour(T_h)
        success_list.extend(success_list_h)
        response_time_list.extend(response_time_list_h)
    return success_list, response_time_list


def get_all_stats(success_list, response_time_list):
    success_rate = sum(success_list) / len(success_list) * 100
    avg, p50, p90, p95 = get_stats(response_time_list)
    return (
        success_rate,
        avg, p50, p90, p95,
    )


def store_stats_for_hour(T):
    T_d = T.strftime(r'%Y%m%d')
    T_h = T.strftime(r'%Y%m%d-%H')
    success_list, response_time_list = get_data_for_hour(T_h)
    if len(success_list) == 0:
        return
    success_rate, avg, p50, p90, p95 = get_all_stats(success_list, response_time_list)
    with open('data/stats/hourly/{}.log'.format(T_d), 'a') as f:
        f.write('{} {} {} {} {} {}\n'.format(
            T_h, success_rate, avg, p50, p90, p95,
        ))
    print(T_h, success_rate, avg, p50, p90, p95)


def store_stats_for_day(T):
    T_y = T.strftime(r'%Y')
    T_d = T.strftime(r'%Y%m%d')
    success_list, response_time_list = get_data_for_day(T_d)
    if len(success_list) == 0:
        return
    success_rate, avg, p50, p90, p95 = get_all_stats(success_list, response_time_list)
    with open('data/stats/daily/{}.log'.format(T_y), 'a') as f:
        f.write('{} {} {} {} {} {}\n'.format(
            T_d, success_rate, avg, p50, p90, p95,
        ))
    print(T_d, success_rate, avg, p50, p90, p95)


def store_stats_for_last_24_hours(T):
    T_d_1 = (T - datetime.timedelta(days=1)).strftime(r'%Y%m%d')
    T_d_2 = T.strftime(r'%Y%m%d')
    data = []
    for T_d in [T_d_1, T_d_2]:
        try:
            with open('data/stats/hourly/{}.log'.format(T_d), 'r') as f:
                for line in f:
                    T_h, success_rate, avg, p50, p90, p95 = line.strip().split(' ')
                    T_ts = datetime.datetime.strptime(T_h, r'%Y%m%d-%H').strftime(TS_FORMAT)
                    data.append({
                        'timestamp': T_ts,
                        'success_rate': float(success_rate),
                        'avg': float(avg),
                        'p50': float(p50),
                        'p90': float(p90),
                        'p95': float(p95),
                    })
        except FileNotFoundError:
            pass
    with open('static/data/hours.json', 'w') as f:
        json.dump(data[-24:], f, sort_keys=True, indent=4)


def store_stats_for_last_91_days(T):
    T_y_2 = T.strftime(r'%Y')
    T_y_1 = str(int(T_y_2) - 1)
    data = []
    for T_y in [T_y_1, T_y_2]:
        try:
            with open('data/stats/daily/{}.log'.format(T_y), 'r') as f:
                for line in f:
                    T_d, success_rate, avg, p50, p90, p95 = line.strip().split(' ')
                    T_ts = datetime.datetime.strptime(T_d, r'%Y%m%d').strftime(TS_FORMAT)
                    data.append({
                        'timestamp': T_ts,
                        'success_rate': float(success_rate),
                        'avg': float(avg),
                        'p50': float(p50),
                        'p90': float(p90),
                        'p95': float(p95),
                    })
        except FileNotFoundError:
            pass
    with open('static/data/days.json', 'w') as f:
        json.dump(data[-91:], f, sort_keys=True, indent=4)


def main():
    if len(sys.argv) == 2 and sys.argv[1] == 'd':
        T_last_day = datetime.datetime.utcnow() - datetime.timedelta(days=1)
        store_stats_for_day(T_last_day)
        store_stats_for_last_91_days(T_last_day)
    else:
        T_last_hour = datetime.datetime.utcnow() - datetime.timedelta(hours=1)
        store_stats_for_hour(T_last_hour)
        store_stats_for_last_24_hours(T_last_hour)


if __name__ == '__main__':
    main()
