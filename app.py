import time
from flask import Flask, Response, stream_with_context
from multiprocessing import Process
from threading import Thread
import uuid
import random

app = Flask(__name__)


def process_function(wait_time):
    i=0
    while i<wait_time:
        i = i+1
        print("loop running %d" % i)
        time.sleep(1)
    print(True)
    return True


# Run multi-processing by this url(multiple thread run in same memory, data sharing is easy)
@app.route("/process")
def multi_process():
    global p
    p = Process(target=process_function, args=(15,))
    p.start()
    return "Multi-process run!"


# Run multi-processing by this url (Allocate different cpu or memory to each process)
@app.route("/thread")
def multi_thread():
    global t
    t = Thread(target=process_function, args=(15,))
    t.start()
    return "Multi-thread run!"


# API to create data for pipe line
@app.route("/data/<int:rowcount>", methods=["GET"])
def get_large_request(rowcount):
    """retunrs N rows of data"""
    def f():
        """The generator of mock data"""
        for _i in range(rowcount):
            time.sleep(.01)
            txid = uuid.uuid4()
            print(txid)
            uid = uuid.uuid4()
            amount = round(random.uniform(-1000, 1000), 2)
            yield f"('{txid}', '{uid}', {amount})\n"
    return Response(stream_with_context(f()))


if __name__ == "__main__":
    app.run()