
import time
import threading

class watchdog(threading.Thread):
    def __init__(self,timeout,callback):
        threading.Thread.__init__(self)
        self.timeout = timeout
        self.callback = callback
        self.status = 'TIMEOUT'
        self._timer = None

    def start(self):
        self._timer = threading.Timer(self.timeout,self._callback)
        self._timer.start()
    def restart(self):
        self._timer.cancel()
        self.start()

    def cancel(self):
        self._timer.cancel()

    def _callback(self):
        self.callback(self.status)


class dummy(object):
    def __init__(self):
        pass

    def callback(self,value):
        print('Event',value)

if __name__ == "__main__":
    d = dummy()
    w = watchdog(5,d.callback)
    w.start()
    while True:
        time.sleep(1)
        print('.',end='',flush=True)