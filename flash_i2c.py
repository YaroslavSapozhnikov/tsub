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
        self.result = [None] * 8
        self.lock = lock
        self.cnt = 0
        self.sens_list: list[int] = sens_list

        if test_mode:
            return

        self.exp = pyiArduinoI2Cexpander(addr)
        for i in self.sens_list:
            self.exp.pinMode(i, INPUT, ANALOG)
#            self.exp.pinPull(i, PULL_DOWN)
        self.exp.analogAveraging(0)


    def shutdown(self):
        self.__shutdown = True

    def read(self):
        if test_mode:
            for i in range(len(self.sens_list)):
                with self.lock:
                    time.sleep(0.01)
                    self.result[self.sens_list[i]] = self.cnt
                    self.cnt += 1
                    if self.cnt >= 4096:
                        self.cnt = 0
        else:
            for i in self.sens_list:
                with self.lock:
                    self.result[self.sens_list[i]] = (self.exp.analogRead(self.sens_list[i]))
        # return result

    def run(self):
        self.read()
        if test_mode:
            time.sleep(0.1)


if __name__ == '__main__':
    sens = FlashI2C(0x0a)
    print(sens.read())
