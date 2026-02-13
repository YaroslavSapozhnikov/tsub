import threading
import time
import random

try:
    from pyiArduinoI2Cexpander import *
    test_mode = False
except ModuleNotFoundError:
    test_mode = True


class FlashI2C(object):
    def __init__(self, addr, lock: threading.Lock, sens_list: list[int]):
        self.__shutdown = False
        self.addr = addr
        self.result = []
        self.lock = lock
        self.cnt = 0
        self.sens_list: list[int] = sens_list

        if test_mode:
            return

        exp = pyiArduinoI2Cexpander(addr)
        for i in self.sens_list:
            exp.pinMode(i, INPUT, ANALOG)

    def shutdown(self):
        self.__shutdown = True

    def read(self):
        result = [None] * 8
        if test_mode:
            for i in range(len(self.sens_list)):
                with self.lock:
                    time.sleep(0.01)
                    result[self.sens_list[i]] = self.cnt
                    self.cnt += 1
                    if self.cnt >= 4096:
                        self.cnt = 0
        else:
            for i in self.sens_list:
                with self.lock:
                    result[self.sens_list[i]] = (exp.analogReader(self.sens_list[i]))
        return result

    def run(self):
        self.result = self.read()
        time.sleep(1)


if __name__ == '__main__':
    sens = FlashI2C(0x0a)
    print(sens.read())
