import datetime
import glob
import time

from config import base_dir


def get_ds18b20_paths():
    ds = []
    sensor_id = []
    device_folders = glob.glob(base_dir + '28*')
    device_folders_slave = [p + '/w1_slave' for p in device_folders]

    for path in device_folders_slave:
        ds.append(path)
        sensor_id.append(path.split('/')[-2])
    return list(zip(sensor_id, ds))


def read_temp_raw(path):
    try:
        f = open(path, 'r')
        lines = f.readlines()
        f.close()
        return lines
    except Exception as e:
        print(e)
        return None


def read_temp(path):
    currentDT = datetime.datetime.now()
    lines = read_temp_raw(path)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw(path)
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos + 2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f, str(currentDT)