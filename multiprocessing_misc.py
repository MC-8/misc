from multiprocessing import Queue, Process, Value, Pipe
from multiprocessing.connection import Connection

from numpy.random import randint
from collections import namedtuple
from queue import Empty as qEmpty
from time import sleep

mydata = namedtuple('mydata',
            ['one','two','three'])

def get_random_data():
    return mydata(one = randint(0, 10),
                  two = randint(-100, 100),
                  three = randint(-1000,1000, size = 10000).tolist())

empty_data = mydata(one=0, two=0, three=[0,0,0])

def Qconsumer_fcn(Q: Queue, loopCondition: Value):
    flag = True
    counter = 0
    while flag:
        try:
            _ = Q.get(timeout = 0.1)
            counter +=1
        except qEmpty:
            flag = bool(loopCondition.value)
    print(f"Consumer msg: Received: {counter} messages\n")

def Qproducer_fcn(Q: Queue, loopCondition: Value):
    while loopCondition.value == 1:
        data = get_random_data()
        Q.put(data)

def Pconsumer_fcn(Pconn: Connection, loopCondition: Value):
    counter = 0
    while loopCondition.value == 1:
        if Pconn.poll(0.1):
            _ = Pconn.recv()
            counter +=1
    Pconn.close()
    print(f"Consumer msg: Received: {counter} messages\n")

def Pproducer_fcn(Pconn: Connection, loopCondition: Value):
    while loopCondition.value == 1:
        data = get_random_data()
        Pconn.send(data)

if __name__ == '__main__':
    t_experiment = 3
    for _ in range(3):
        print(f"Using Queue")
        mainQ = Queue()
        loopCondition = Value('b')
        loopCondition.value = 1
        producer = Process(target=Qproducer_fcn, args=(mainQ, loopCondition))
        consumer = Process(target=Qconsumer_fcn, args=(mainQ, loopCondition))
        producer.daemon = True
        consumer.daemon = True
        producer.start()
        consumer.start()
        sleep(t_experiment)
        loopCondition.value = 0
        consumer.join()

        print(f"Using Pipe")
        cons_conn, prod_conn = Pipe(duplex=False)
        loopCondition = Value('b')
        loopCondition.value = 1
        producer = Process(target=Pproducer_fcn, args=(prod_conn, loopCondition))
        consumer = Process(target=Pconsumer_fcn, args=(cons_conn, loopCondition))
        producer.daemon = True
        consumer.daemon = True
        producer.start()
        consumer.start()
        sleep(t_experiment)
        loopCondition.value = 0
        consumer.join()

    print("Done.")