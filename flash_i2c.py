import time

try:
    from pyiArduinoI2Cexpander import *
    test_mode = False
except ModuleNotFoundError:
    test_mode = True


class FlashI2C(object):

    def __init__(self, addr):
        self.result = []

        if test_mode:
            return

        exp = pyiArduinoI2Cexpander(addr)
        for i in range(8):
            exp.pinMode(i, INPUT, ANALOG)

    def read(self):
        if test_mode:
            return [2048]*8
        result = []
        for i in range(8):
            result.append(exp.analogReader(i))
        return result

    def run(self):
        self.result = self.read()
        time.sleep(1)


if __name__ == '__main__':
    sens = FlashI2C(0x0a)
    print(sens.read())
