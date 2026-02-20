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

    def read_all(self):
        if test_mode:
            for i in range(len(self.sens_list)):
                with self.lock:
                    time.sleep(0.01)
                    self.result[self.sens_list[i]] = 100 * (i + 1) + random.randint(-10, 10)
        else:
            for i in range(len(self.sens_list)):
                with self.lock:
                    self.result[self.sens_list[i]] = (self.exp.analogRead(self.sens_list[i]))
        return self.result

    def read(self, sens):
        if test_mode:
            with self.lock:
                time.sleep(0.01)
                self.result[sens] = 100 * (sens + 1) + random.randint(-10, 10)
        else:
             with self.lock:
                self.result[sens] = (self.exp.analogRead(sens))
        return self.result[sens]


    def run(self):
        self.read_all()


if __name__ == '__main__':
    exp = FlashI2C(0x0a)
    print(exp.read_all())
