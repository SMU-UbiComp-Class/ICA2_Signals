import serial
import ringbuffer
import numpy as np
import time
import threading


BUFFER_SIZE = 128
data = ringbuffer.RingBuffer(BUFFER_SIZE)

serial_port = serial.Serial('/dev/cu.usbmodem1422', baudrate=9600, timeout=1)
serial_port.flush()


def read_serial_forever():
    global data
    while True:
        try:
            values = serial_port.read(10)
        except:
            print('Exiting thread')
            break
            
        if values:
            tmp = np.array(list(values))

            data.insert_new(tmp.astype(np.int))
            print(np.sum(tmp),end=", ")

        time.sleep(0.01)

t = threading.Thread(target=read_serial_forever, args=())
t.start()

for i in range(0, 10):
    time.sleep(1)
    print ("sleeping", i)

serial_port.close() # will cause error, forcing close of thread
t.join() # wait for thread to exit