import multiprocessing
import string
import threading
import logging
import random
import time
from datetime import datetime

import httpx
import json
import os

rand_str = lambda n: ''.join([random.choice(string.ascii_lowercase) for i in range(n)])

"""
тут хотел на асинхронке написать, но чет забил
"""
# async def async_request(i):
#     async with httpx.AsyncClient() as client:
#         #print('start', i)
#         params = {
#             'a': random.randint(1, 100),
#             'b': 'world'
#         }
#         response = await client.get(config.get('url'), params=params, timeout=config.get('clientTimeout') / 1000)
#         print('end', i, response.elapsed)
#
#
# async def worker():
#     for _ in range(1):
#         pool = []
#         for i in range(config.get('concurrency')):
#             task = asyncio.create_task(async_request(i))
#             pool.append(task)
#         for i in pool:
#             await i
#         time.sleep(config.get('batchDelay') / 1000)

def request(url, timeout):
    try:
        logging.basicConfig(filename=".log", level=logging.INFO)
        with httpx.Client() as client:
            params = {
                'a': rand_str(random.randint(1, 200)),
                'b': rand_str(random.randint(1, 200))
            }
            response = client.get(url, params=params, timeout=timeout)
            logging.info(f'{response.elapsed.microseconds / 1000}ms;{response.status_code};{response.text}')
    except:
        pass


def worker(config):
    for _ in range(50):
        pool = []
        for _ in range(config.get('concurrency')):
            task = threading.Thread(target=request, args=(config.get('url'), config.get('clientTimeout') / 1000,))
            task.start()
            pool.append(task)
        for t in pool:
            t.join()
        time.sleep(config.get('batchDelay') / 1000)


def get_config():
    with open('config.json', 'r') as file:
        return json.loads(file.read())


if __name__ == '__main__':
    logging.basicConfig(filename=".log")
    processors = os.cpu_count()
    config = get_config()
    print('Concurrency: ', config.get('concurrency'))
    print('Worker pool: ', processors)
    print('Resulting batch size: ', config.get('concurrency') * processors)

    time.sleep(config.get('pause') / 1000)

    procs = []
    print('Started:', datetime.now())

    for i in range(processors):
        proc = multiprocessing.Process(target=worker, args=(config,))
        proc.start()
        procs.append(proc)

    for proc in procs:
        proc.join()

    time.sleep(config.get('pause') / 1000)

    print('Ended:', datetime.now())
