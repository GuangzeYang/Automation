

import threading
import time



def func_1():
    for i in range(100):
        time.sleep(0.01)

def func_2():
    for i in range(100):
        time.sleep(0.05)


if __name__ == '__main__':
    thread_1 = threading.Thread(target=func_1)
    thread_2 = threading.Thread(target=func_2)
    thread_1.start()
    thread_2.start()
    pass