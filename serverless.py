from time import sleep
from flask import Flask
from multiprocessing import Queue, Process, Value, active_children, Semaphore, Pipe

app = Flask(__name__)
total_idle_workers = Value('i', 0)
total_handled_requests = Value('i', 0)
data_queue = Queue()
data_sem = Semaphore(0)
    
@app.route('/sleep_and_sum/<int:x>+<int:y>', methods=['GET'])
def dispatcher(x: int, y: int):
    '''Dispatching sleep_and_sum tasks to worker processes.

    Args: x, y - two integers
    Returns: The sum of x+y as an HTTP response.
    '''

    # produce data to queue
    receive_conn, send_conn = Pipe(duplex=False)
    data = (x, y, send_conn)
    data_queue.put(data)

    # determine if a new worker needs to be created
    with total_idle_workers.get_lock():
        if 0 == total_idle_workers.value:
            new_worker = Process(target=sleep_and_sum, 
                                 args=(data_sem, data_queue, total_idle_workers), 
                                 daemon=True)
            new_worker.start()
        else:
            total_idle_workers.value -= 1
    data_sem.release()

    # get the proccessed data back from the worker.
    result = receive_conn.recv()
    with total_handled_requests.get_lock():
        total_handled_requests.value += 1
    return str(result);

def sleep_and_sum(data_sem: Semaphore, data_queue: Queue, total_idle_workers: Value) -> None:
    '''Worker's process function, processing data and sending back the result
    to the router. 
    If the worker has been idle for more than `max_time_idle` seconds it'll be terminated.
    '''
    max_time_idle = 6.0
    while (1):
        # waiting for new work, until timeout
        if (False == data_sem.acquire(timeout=max_time_idle)):
            with total_idle_workers.get_lock():
                total_idle_workers.value -= 1
            return
        
        # handling the request
        data = data_queue.get()
        send_conn = data[2]
        sum = data[0] + data[1]

        sleep(3.0);
        send_conn.send(sum)

        # setting up for the next request
        with total_idle_workers.get_lock():
            total_idle_workers.value += 1

@app.route('/active_processes', methods=['GET'])
def active_processes():
    '''List PIDs of all workers'''
    active_workers = [worker.pid for worker in active_children()]
    return active_workers;

@app.route('/request_counter', methods=['GET'])
def request_counter():
    '''Responding with the total number of handled requests'''
    with total_handled_requests.get_lock():
        return "total handled requests: " + str(total_handled_requests.value);

if '__main__' == __name__:
    app.run(debug=True)