import time
import threading
import flash_i2c
import configparser
import math
from pynput import keyboard
import uuid
from srv import Srv


__shutdown = False


def kbd_f12():
    global __shutdown
    # В этом блоке будет работать слушатель событий.
    with keyboard.Events() as events:
        for event in events:
            if event.key == keyboard.Key.f12:
                __shutdown = True
                break


def shutdown():
    global __shutdown
    __shutdown = True


def get_id(name: str = 'tsub'):
    return int(str(uuid.uuid1()).split('-')[4], 16)


def main():
    config = configparser.ConfigParser()
    config.read('tsub.ini', encoding='utf-8')
    all_sections = config.sections()

    # Clear screen
    lock = threading.Lock()
    exps = []
    sensors = []
    for sect in all_sections:
        try:
            addr = int(sect)
            if 9 < addr < 128:
                sens_list = []
                options = config.options(sect)
                for opt in options:
                    try:
                        sens = int(opt)
                        if 0 <= sens < 8:
                            sens_list.append(sens)
                            sensors.append({'name': config.get(sect, opt),
                                            'addr': addr,
                                            'input': sens,
                                            'readout': "0.0"})
                    except ValueError:
                        continue
                exps.append(flash_i2c.FlashI2C(addr, lock, sens_list=sens_list))
        except ValueError:
            continue

    facility = {
        "id": get_id(),
        "name": config.get("DEFAULT", "FacilityName"),
        "addr": config.get("DEFAULT", "Address"),
        "sensors": sensors,
        "update_time": None
    }

    server = Srv(config.get('DEFAULT', 'Server'),
                 int(config.get('DEFAULT', 'Port')))

    readouts_num = int(config.get('DEFAULT', 'ReadoutsNum'))

    time.sleep(2)

    while True:
        for i, sens in enumerate(sensors):
            avrg = 0
            avrg2 = 0
            exp_in = sens['input']
            for _ in range(readouts_num):
                readout = exps[0].read(exp_in)
                avrg += readout
                avrg2 += readout ** 2
            # Уравнение прямой: y = 1.0949 * x
            facility["sensors"][i]["readout"] = str(round((avrg/(readouts_num/2))*0.187, 1))
        server.request(facility)


if __name__ == '__main__':
    main()
