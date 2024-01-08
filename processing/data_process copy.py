import os
import csv
import json
from datetime import timedelta, datetime
import pprint

pp = pprint.PrettyPrinter(indent=4, depth=10)

dirname = os.path.dirname
SITE_ROOT = os.path.realpath(dirname(dirname(__file__)))
DATA_ROOT = os.path.join(SITE_ROOT, 'data')
TARGET_ROOT = os.path.join(DATA_ROOT, '230217')

# data_path = os.path.join(TARGET_ROOT, '230217.json')
data_path = os.path.join(TARGET_ROOT, 'data0327_r1.csv')

record_list = []
record_dict = {}

user_id_list = []
equip_list = []
user_id_record_dict = {}


def get_workout_matrix_info(data):
    target_user_id_list = data['user_id_list']

    # 우선 무조건 한 개라고 생각하고 진행
    target_user_id = target_user_id_list[0]

    target_record_list = user_id_record_dict[target_user_id]
    min_dt = datetime.max
    max_dt = datetime.min

    for r in target_record_list:
        start_time = r['start']
        date_time_obj = datetime.strptime(start_time, '%Y-%m-%d %H:%M')

        if min_dt > date_time_obj:
            min_dt = date_time_obj

        if max_dt < date_time_obj:
            max_dt = date_time_obj

    min_dt = min_dt.replace(hour=0, minute=0, second=0)
    max_dt = max_dt.replace(hour=0, minute=0, second=0)
    day_list = []
    day_equip_dict = {}
    dates = [min_dt + timedelta(days=x) for x in range((max_dt - min_dt).days + 1)]
    for date_time_obj in dates:
        d_str = date_time_obj.strftime('%Y-%m-%d')
        day_list.append(d_str)
        day_equip_dict[d_str] = set()

    day_equip_count_dict = {}
    for d_str in day_list:
        for e_id in equip_list:
            de_id = '{}-{}'.format(d_str, e_id)
            day_equip_count_dict[de_id] = 0

    for r in target_record_list:
        count = r['count']
        equip_id = r['equip']
        start_time = r['start']
        date_time_obj = datetime.strptime(start_time, '%Y-%m-%d %H:%M')
        d_str = date_time_obj.strftime('%Y-%m-%d')
        de_id = '{}-{}'.format(d_str, equip_id)
        day_equip_count_dict[de_id] += count
        day_equip_dict[d_str].add(equip_id)

    new_dict = {}
    for k, v in day_equip_dict.items():
        new_dict[k] = list(v)
    day_equip_dict = new_dict

    packet = {
        'day_list': day_list,
        'day_equip': day_equip_dict,
        'day_equip_count': day_equip_count_dict
    }

    return packet


def preprocess():

    global record_list, record_dict
    with open(data_path, "r", encoding='UTF-8') as read_file:
        # record_list = json.load(read_file)
        record_list = csv.reader(read_file)
        # for row in record_list:
        #     print(row)

    global user_id_list, equip_list, user_id_record_dict
    e_set = set()
    # print(record_list)
    for rec in record_list:
        record_dict[rec['id']] = rec

        user_id = rec['user']
        if user_id not in user_id_record_dict:
            user_id_record_dict[user_id] = []
        user_id_record_dict[user_id].append(rec)

        equip_id = rec['equip']
        e_set.add(equip_id)

    user_id_list = list(user_id_record_dict.keys())
    print(user_id_list)
    print('Number of Users : {}'.format(len(user_id_record_dict)))

    equip_list = list(e_set)
    print('Number of Equipments : {}'.format(len(equip_list)))
