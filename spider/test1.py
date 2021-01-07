# -*- coding: utf-8 -*-
import json
import time, datetime
from concurrent.futures.thread import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=2)


def test_executor(id):
    print('start id: {}'.format(id))
    time.sleep(10)
    print('end id: {}'.format(id))


def test(num):
    list_test = (1, '2', 1)
    # list_test.append(1)
    # list_test.append('2')
    # list_test.append(1)
    num = 3
    list_test_coder = []
    list_test_coder.append(1)
    list_test_coder.append(3)
    list_test_coder.append(1)

    return list_test_coder, list_test


if __name__ == '__main__':
    executor.submit(test_executor, 1)
    print('主线程执行完成')
