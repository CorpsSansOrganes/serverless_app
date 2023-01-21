import requests
from threading import Thread

def make_sleep_and_sum_request():
    requests.get("http://127.0.0.1:5000/sleep_and_sum/1+1")

if __name__ == '__main__':
    n = 10
    req_list = []
    for i in range(n):
        req_list.append(Thread(target=make_sleep_and_sum_request))
        req_list[i].start()
    for i in range(n):
        req_list[i].join()
    print("done")
